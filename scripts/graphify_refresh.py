#!/usr/bin/env python3
"""Refresh Graphify graphs for Hermes source and split theduyvault graphs.

Outputs stay outside the vault:
  /home/hermes/.graphify/hermes/graphify-out/
  /home/hermes/.graphify/theduyvault/graphify-out/          legacy/all vault
  /home/hermes/.graphify/theduyvault-core/graphify-out/     MOCs/Projects/Notes/Tasks
  /home/hermes/.graphify/theduyvault-sources/graphify-out/  Sources/Clippings/Stock Watchlist
  /home/hermes/.graphify/theduyvault-daily/graphify-out/    Daily/AgentMemory/Inbox/System

Designed for a tight container (~2.5Gi cgroup):
  - Hermes extract is scoped to core source dirs (no node_modules/venv/apps)
  - max-workers defaults to 1
  - no --force on daily runs (incremental AST cache)
  - Hermes / per-vault failures are soft: keep prior graph, continue others
"""
from __future__ import annotations

import gc
import json
import os
import shutil
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
BASE = HOME / ".graphify"
HERMES_SRC = HOME / ".hermes" / "hermes-agent"
VAULT = Path("/vault")
HERMES_OUT_ROOT = BASE / "hermes"

# Full-tree extract pulls node_modules/venv/apps (~7.5k files) and gets
# SIGKILL/OOM on the ~2.5Gi cron cgroup. Scope via .graphifyignore in-repo.
HERMES_GRAPHIFYIGNORE = """\
# Managed by graphify_refresh.py — keep Hermes extract under container RAM.
node_modules/
**/node_modules/
venv/
.venv/
apps/
website/
web/
ui-tui/
docs/
tests/
tests-js/
contributors/
docker/
nix/
locales/
assets/
datagen-config-examples/
mcp-research-data/
optional-skills/platforms/
**/.git/
**/dist/
**/build/
**/__pycache__/
**/*.egg-info/
*.egg-info/
package-lock.json
yarn.lock
pnpm-lock.yaml
"""

# Keep workers low on this host. Override with GRAPHIFY_MAX_WORKERS.
MAX_WORKERS = max(1, int(os.environ.get("GRAPHIFY_MAX_WORKERS", "1")))
# Set GRAPHIFY_HERMES_FORCE=1 for a full re-scan of the scoped tree.
HERMES_FORCE = os.environ.get("GRAPHIFY_HERMES_FORCE", "").strip() in {"1", "true", "yes"}
VAULT_GRAPHS = {
    "theduyvault": {
        "description": "legacy/all structural vault graph",
        "include_top": {
            "AgentMemory", "Clippings", "Daily", "Inbox", "MOCs", "Notes", "Projects",
            "Sources", "Stock Watchlist", "System", "Tasks",
        },
    },
    "theduyvault-core": {
        "description": "core life/business/tasks graph",
        "include_top": {"MOCs", "Notes", "Projects", "Tasks"},
        "exclude_prefixes": {"Notes/Claude-Context/"},
    },
    "theduyvault-sources": {
        "description": "research/source/article graph",
        "include_top": {"Sources", "Clippings", "Stock Watchlist"},
    },
    "theduyvault-daily": {
        "description": "daily/session/inbox/system graph",
        "include_top": {"Daily", "AgentMemory", "Inbox", "System", "Notes"},
        "include_prefixes": {"Notes/Claude-Context/"},
    },
}

VAULT_EXCLUDE_PARTS = {
    ".git", ".obsidian", ".stversions", ".trash", ".smart-env", ".stfolder",
    ".superpowers", ".claude", ".code-review-graph", ".zettel-notes", "Attachments",
    "graphify-out", "node_modules",
}


def reexec_with_graphify_if_needed() -> None:
    """Run under the uv tool interpreter so `import graphify` is reliable in cron."""
    if os.environ.get("GRAPHIFY_REFRESH_REEXEC") == "1":
        return
    try:
        import graphify  # noqa: F401
        return
    except Exception:
        pass
    uv = shutil.which("uv")
    if not uv:
        return
    try:
        py = subprocess.check_output(
            [uv, "tool", "run", "--from", "graphifyy", "python", "-c", "import sys; print(sys.executable)"],
            text=True,
        ).strip()
        if py and Path(py).exists():
            env = os.environ.copy()
            env["GRAPHIFY_REFRESH_REEXEC"] = "1"
            os.execve(py, [py, __file__, *sys.argv[1:]], env)
    except Exception:
        return


def run(cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=env, check=True)


def graph_stats(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "path": str(path),
        "nodes": len(data.get("nodes", [])),
        "edges": len(data.get("links", data.get("edges", []))),
        "bytes": path.stat().st_size,
        "mtime": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
    }


def ensure_hermes_graphifyignore() -> Path:
    """Write scoped ignore rules into the Hermes checkout (detect reads scan root)."""
    path = HERMES_SRC / ".graphifyignore"
    desired = HERMES_GRAPHIFYIGNORE.lstrip("\n")
    if path.exists() and path.read_text(encoding="utf-8") == desired:
        print(f"[hermes] .graphifyignore already current at {path}", flush=True)
        return path
    path.write_text(desired, encoding="utf-8")
    print(f"[hermes] wrote scoped .graphifyignore at {path}", flush=True)
    return path


def _hermes_needs_force(out_graph: Path) -> bool:
    """Force when missing, env-forced, empty, or prior graph wasn't scoped-core."""
    if HERMES_FORCE or not out_graph.exists():
        return True
    try:
        if graph_stats(out_graph)["nodes"] == 0:
            return True
    except Exception:
        return True
    meta_path = HERMES_OUT_ROOT / "graphify-out" / "BUILD_META.json"
    if not meta_path.exists():
        # Legacy full-tree graph (~node_modules) must be replaced once.
        return True
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return True
    return meta.get("mode") != "scoped-core"


def build_hermes() -> dict:
    out_dir = HERMES_OUT_ROOT / "graphify-out"
    out_graph = out_dir / "graph.json"
    backup = out_dir / "graph.json.bak"
    HERMES_OUT_ROOT.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    ensure_hermes_graphifyignore()

    # Preserve last good graph so a failed/empty rebuild cannot wipe MCP input.
    if out_graph.exists():
        try:
            if graph_stats(out_graph)["nodes"] > 0:
                shutil.copy2(out_graph, backup)
        except Exception:
            pass
    elif backup.exists() is False:
        legacy = out_dir / "graph.json.pre-scope.bak"
        if legacy.exists():
            shutil.copy2(legacy, backup)

    env = os.environ.copy()
    env["PATH"] = f"{HOME / '.local' / 'bin'}:{env.get('PATH', '')}"
    force = _hermes_needs_force(out_graph)
    cmd = [
        "graphify", "extract", str(HERMES_SRC),
        "--code-only",
        "--out", str(HERMES_OUT_ROOT),
        "--max-workers", str(MAX_WORKERS),
        "--no-cluster",  # cheaper peak RAM; MCP only needs graph.json
    ]
    if force:
        cmd.append("--force")
    run(cmd, env=env)

    if not out_graph.exists():
        if backup.exists():
            shutil.copy2(backup, out_graph)
        raise FileNotFoundError(f"hermes graph missing after build: {out_graph}")

    stats = graph_stats(out_graph)
    if stats["nodes"] == 0:
        if backup.exists() and graph_stats(backup)["nodes"] > 0:
            shutil.copy2(backup, out_graph)
            stats = graph_stats(out_graph)
            stats["restored_backup"] = True
        raise RuntimeError(
            f"hermes extract produced 0 nodes (scoped ignore too aggressive or scan failed); "
            f"restored_prior={stats.get('restored_backup', False)}"
        )

    stats["mode"] = "scoped-core"
    stats["max_workers"] = MAX_WORKERS
    stats["forced"] = force
    (out_dir / "BUILD_META.json").write_text(json.dumps({
        "built_at": datetime.now(timezone.utc).isoformat(),
        "source_repo": str(HERMES_SRC),
        "name": "hermes",
        "mode": "scoped-core",
        "graphifyignore": str(HERMES_SRC / ".graphifyignore"),
        "max_workers": MAX_WORKERS,
        "forced": force,
        "nodes": stats["nodes"],
        "edges": stats["edges"],
        "bytes": stats["bytes"],
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    return stats

def vault_markdown_files(
    include_top: set[str],
    include_prefixes: set[str] | None = None,
    exclude_prefixes: set[str] | None = None,
) -> list[Path]:
    include_prefixes = include_prefixes or set()
    exclude_prefixes = exclude_prefixes or set()
    files: list[Path] = []
    for p in VAULT.rglob("*.md"):
        try:
            rel = p.relative_to(VAULT)
        except ValueError:
            continue
        rel_posix = rel.as_posix()
        parts = set(rel.parts)
        if parts & VAULT_EXCLUDE_PARTS:
            continue
        if any(rel_posix.startswith(prefix) for prefix in exclude_prefixes):
            continue
        prefix_match = any(rel_posix.startswith(prefix) for prefix in include_prefixes)
        top_match = (len(rel.parts) > 1 and rel.parts[0] in include_top) or (
            len(rel.parts) == 1 and "(root)" in include_top
        )
        if not (prefix_match or top_match):
            continue
        files.append(p)
    return sorted(files)


def build_vault_graph(
    name: str,
    include_top: set[str],
    description: str,
    include_prefixes: set[str] | None = None,
    exclude_prefixes: set[str] | None = None,
) -> dict:
    from graphify.analyze import god_nodes, suggest_questions, surprising_connections
    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.export import to_json
    from graphify.extract import extract
    from graphify.report import generate

    out_root = BASE / name
    out = out_root / "graphify-out"
    out.mkdir(parents=True, exist_ok=True)
    paths = vault_markdown_files(include_top, include_prefixes, exclude_prefixes)
    print(f"[{name}] structural markdown extraction on {len(paths)} files (workers={MAX_WORKERS})", flush=True)
    result = extract(paths, cache_root=out_root, root=VAULT, max_workers=MAX_WORKERS)
    (out / ".graphify_extract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    G = build_from_json(result, root=str(VAULT), directed=False)
    if G.number_of_nodes() == 0:
        raise RuntimeError(f"{name} graph is empty")
    communities = cluster(G)
    cohesion = score_all(G, communities)
    labels = {cid: f"{name} Community {cid}" for cid in communities}
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities, labels)
    detection = {
        "total_files": len(paths),
        "total_words": 0,
        "files": {"document": [str(p) for p in paths]},
        "scan_root": str(VAULT),
    }
    # Force is intentional here: split graph scopes can shrink when include/exclude rules change.
    to_json(G, communities, str(out / "graph.json"), force=True)
    report = generate(
        G, communities, cohesion, labels, gods, surprises, detection,
        {"input": 0, "output": 0}, str(VAULT), suggested_questions=questions,
    )
    (out / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    (out / ".graphify_analysis.json").write_text(json.dumps({
        "communities": {str(k): v for k, v in communities.items()},
        "cohesion": {str(k): v for k, v in cohesion.items()},
        "gods": gods,
        "surprises": surprises,
        "questions": questions,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / ".graphify_labels.json").write_text(
        json.dumps({str(k): v for k, v in labels.items()}, indent=2), encoding="utf-8"
    )
    (out / "BUILD_META.json").write_text(json.dumps({
        "built_at": datetime.now(timezone.utc).isoformat(),
        "source": str(VAULT),
        "name": name,
        "description": description,
        "mode": "structural-markdown-local",
        "included_top_level": sorted(include_top),
        "included_prefixes": sorted(include_prefixes or []),
        "excluded_parts": sorted(VAULT_EXCLUDE_PARTS),
        "excluded_prefixes": sorted(exclude_prefixes or []),
        "files": len(paths),
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "communities": len(communities),
        "god_nodes": gods[:20],
        "max_workers": MAX_WORKERS,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    # Drop large in-memory structures before the next vault graph.
    del G, result, communities, cohesion
    gc.collect()
    return graph_stats(out / "graph.json") | {"files": len(paths), "description": description}


def _keep_prior(name: str, err: BaseException) -> dict:
    """On failure, report prior graph stats if present so MCP keeps a working file."""
    path = BASE / name / "graphify-out" / "graph.json"
    payload: dict = {
        "error": f"{type(err).__name__}: {err}",
        "kept_prior": path.exists(),
    }
    if path.exists():
        try:
            payload.update(graph_stats(path))
        except Exception as stats_err:  # noqa: BLE001
            payload["stats_error"] = str(stats_err)
    print(f"[{name}] FAILED: {payload['error']} (kept_prior={payload['kept_prior']})", flush=True)
    traceback.print_exc()
    return payload


def main() -> None:
    reexec_with_graphify_if_needed()
    skip_hermes = "--vault-only" in sys.argv
    only_split = "--split-only" in sys.argv
    hermes_only = "--hermes-only" in sys.argv
    stats: dict[str, dict] = {}
    failures = 0

    if not skip_hermes and not only_split:
        try:
            stats["hermes"] = build_hermes()
        except Exception as err:  # noqa: BLE001 — soft-fail so vault graphs still refresh
            stats["hermes"] = _keep_prior("hermes", err)
            failures += 1
        gc.collect()

    if not hermes_only:
        for name, cfg in VAULT_GRAPHS.items():
            try:
                stats[name] = build_vault_graph(
                    name,
                    cfg["include_top"],
                    cfg["description"],
                    cfg.get("include_prefixes"),
                    cfg.get("exclude_prefixes"),
                )
            except Exception as err:  # noqa: BLE001
                stats[name] = _keep_prior(name, err)
                failures += 1
            gc.collect()

    summary = BASE / "last-refresh.json"
    summary.write_text(json.dumps({
        "refreshed_at": datetime.now(timezone.utc).isoformat(),
        "max_workers": MAX_WORKERS,
        "hermes_force": HERMES_FORCE,
        "failures": failures,
        "stats": stats,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(stats, indent=2, ensure_ascii=False), flush=True)

    # Exit 0 if at least one graph succeeded; exit 1 only if everything failed.
    succeeded = sum(1 for v in stats.values() if "error" not in v)
    if succeeded == 0:
        raise SystemExit(1)
    if failures:
        print(f"completed with {failures} soft failure(s), {succeeded} ok", flush=True)


if __name__ == "__main__":
    main()
