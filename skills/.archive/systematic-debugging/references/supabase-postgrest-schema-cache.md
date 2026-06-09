# Supabase/PostgREST schema-cache debugging

Use this when Supabase JS RPCs fail with PostgREST errors like `PGRST202`.

## Core idea

A function can exist in PostgreSQL and still be invisible to the API if:
- the function was never applied to the target database
- the API schema cache is stale
- the call uses the wrong argument names/order or overload
- the test is pointed at a different database/API host than the one you inspected

## Fast checks

1. Verify the exact error from the client.
   - `PGRST202` usually means PostgREST could not find the RPC in its schema cache.
2. Check the RPC signature in `pg_proc` on the same database the API points at.
3. Confirm the client is calling the same host/port that serves PostgREST, not a direct Postgres port.
4. If DDL just changed, reload the cache:
   - `NOTIFY pgrst, 'reload schema';`
5. If the function was added by a migration, confirm the migration exists in `supabase_migrations.schema_migrations` on that target DB.

## Common gotchas

- `rpc()` parameter names matter when PostgREST resolves overloads.
- A function can be present in a local direct connection but absent in the API path.
- Bootstrap or dump-based installs can lag behind later migrations even when the repo contains the function.
- Fresh installs and long-lived tenants can diverge; always check the live target, not just repository SQL.
- Supabase JS `head: true` probes can return 204/no error for missing relations in some local drift states; verify with a real REST/GET or RPC call before treating the target as live.
- When `psql` is unavailable but the repo has the Node `pg` package, run direct Postgres diagnostics and one-off SQL application with a small Node script. Record manually applied migrations in `supabase_migrations.schema_migrations` if you bypass the Supabase CLI.

## Useful probes

- List matching functions:
  - `select proname, pg_get_function_identity_arguments(p.oid) from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and proname in ('<rpc_name>');`
- Inspect applied migrations:
  - `select version from supabase_migrations.schema_migrations order by version desc;`
- Reload cache after DDL:
  - `NOTIFY pgrst, 'reload schema';`

## Debugging order

1. Reproduce the RPC error.
2. Confirm the target host/port.
3. Inspect the function signature on the target DB.
4. Check migration application state.
5. Reload the schema cache.
6. Re-run the failing RPC test.
