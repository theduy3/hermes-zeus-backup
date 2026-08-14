#!/usr/bin/env python3
"""Refresh Graphify graphs for Hermes source and split theduyvault graphs.

Outputs stay outside the vault:
  /home/hermes/.graphify/hermes/graphify-out/
  /home/hermes/.graphify/theduyvault/graphify-out/          legacy/all vault
  /home/hermes/.graphify/theduyvault-core/graphify-out/     MOCs/Projects/Notes/Tasks
  /home/hermes/.graphify/theduyvault-sources/graphify-out/  Sources/Clippings/Stock Watchlist
  /home/hermes/.graphify/theduyvault-daily/graphify-out/    Daily/AgentMemory/Inbox/System
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
BASE = HOME / ".graphify"
HERMES_SRC = HOME / ".hermes" / "hermes-agent"
VAULT = Path("/vault")
HERMES_OUT_ROOT = BASE / "hermes"

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
    }


def build_hermes() -> dict:
    HERMES_OUT_ROOT.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["PATH"] = f"{HOME / '.local' / 'bin'}:{env.get('PATH', '')}"
    run([
        "graphify", "extract", str(HERMES_SRC), "--code-only", "--out",
        str(HERMES_OUT_ROOT), "--force", "--max-workers", "4",
    ], env=env)
    return graph_stats(HERMES_OUT_ROOT / "graphify-out" / "graph.json")


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
        top_match = (len(rel.parts) > 1 and rel.parts[0] in include_top) or (len(rel.parts) == 1 and "(root)" in include_top)
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
    print(f"[{name}] structural markdown extraction on {len(paths)} files", flush=True)
    result = extract(paths, cache_root=out_root, root=VAULT, max_workers=4)
    (out / ".graphify_extract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    G = build_from_json(result, root=str(VAULT), directed=False)
    if G.number_of_nodes() == 0:
        raise SystemExit(f"{name} graph is empty")
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
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    return graph_stats(out / "graph.json") | {"files": len(paths), "description": description}


def main() -> None:
    reexec_with_graphify_if_needed()
    skip_hermes = "--vault-only" in sys.argv
    only_split = "--split-only" in sys.argv
    stats: dict[str, dict] = {}
    if not skip_hermes and not only_split:
        stats["hermes"] = build_hermes()
    for name, cfg in VAULT_GRAPHS.items():
        stats[name] = build_vault_graph(
            name,
            cfg["include_top"],
            cfg["description"],
            cfg.get("include_prefixes"),
            cfg.get("exclude_prefixes"),
        )
    summary = BASE / "last-refresh.json"
    summary.write_text(json.dumps({
        "refreshed_at": datetime.now(timezone.utc).isoformat(),
        "stats": stats,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(stats, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
