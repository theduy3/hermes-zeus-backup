#!/bin/sh
# Vault-only Graphify refresh.
#
# The full refresh also rebuilds the Hermes source graph, which OOMs (SIGKILL,
# exit -9) on this container's ~2.5Gi cgroup whenever an upgrade invalidates the
# incremental AST cache — a `hermes update` marks every file changed, so all
# ~1750 code files get re-extracted in one run. When that dies it takes the
# vault graphs down with it.
#
# The Hermes graph is not consumed by anything today: mcp_servers."graphify-hermes"
# is enabled: false in config.yaml, while "graphify-vault" is enabled: true.
# So skip it and keep the graphs that are actually used.
#
# To rebuild the Hermes graph by hand (expect high memory, run it when idle):
#   python3 ~/.hermes/scripts/graphify_refresh.py --hermes-only
#
# Re-enable the nightly Hermes graph only after mcp_servers."graphify-hermes"
# is switched back on AND this container has headroom above 2.5Gi.
exec python3 "$HOME/.hermes/scripts/graphify_refresh.py" --vault-only "$@"
