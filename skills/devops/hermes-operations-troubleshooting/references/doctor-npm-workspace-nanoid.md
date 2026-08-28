# hermes doctor: web / ui-tui npm workspace advisories

## Symptoms

```
⚠ web workspace deps (... high ... — build-tool advisory; clears via lockfile bump)
⚠ ui-tui workspace deps (... high ... — build-tool advisory; clears via lockfile bump)

Found N issue(s) to address:
  2. web workspace has N npm vulnerabilities
  3. ui-tui workspace has N npm vulnerabilities
```

Doctor tip `hermes doctor --fix` does **not** clear these.

## Risk

Usually build-time tooling under `vite` / `postcss` / `sanitize-html`, not Hermes agent runtime. Safe to treat as hygiene unless shipping/building web or ui-tui from the checkout.

## Where to work

On bluehost Docker deploy:

| Shell | Path |
|-------|------|
| Host root SSH | NO `/root/.hermes/hermes-agent` |
| Container `hermes` | `/home/hermes/.hermes/hermes-agent` |

```bash
docker exec -it hermes bash
cd /home/hermes/.hermes/hermes-agent
```

## Diagnose

```bash
npm audit --workspace web
npm audit --workspace ui-tui
npm ls nanoid --workspace web
npm ls nanoid --workspace ui-tui
grep -n nanoid package.json
```

Known advisory shape (2026-08):

- `nanoid < 3.3.18` — GHSA-2v37-7h3g-55p8
- Chains: `vite → postcss → nanoid`, `sanitize-html → postcss → nanoid`
- Root override may pin the bad version:
  `"nanoid@^3": "3.3.17"`

## Do not lead with

```bash
npm audit fix --workspace web
npm audit fix --workspace ui-tui
npm audit fix
```

Doctor omits these on purpose: npm arborist can crash on this monorepo (`edgesOut` / `isDescendantOf`).

## Fix recipe (override + nested refresh)

```bash
cd /home/hermes/.hermes/hermes-agent
cp package.json package.json.bak
cp package-lock.json package-lock.json.bak

# In package.json overrides:
#   "nanoid@^3": "3.3.18"   # was 3.3.17
# leave "nanoid@^6" alone

# one-liner if the old pin is exact:
sed -i 's/"nanoid@\^3": "3\.3\.17"/"nanoid@^3": "3.3.18"/' package.json
grep -n 'nanoid' package.json

# override edit alone often leaves nested 3.3.17 as "invalid"
rm -rf node_modules/vite/node_modules/nanoid \
       node_modules/sanitize-html/node_modules/nanoid

npm install --no-fund --no-audit

npm ls nanoid --workspace web
npm ls nanoid --workspace ui-tui
npm audit --workspace web
npm audit --workspace ui-tui
hermes doctor
```

## Pitfall: EOVERRIDE from a root direct dep

Do **not** run something that adds root `"dependencies": { "nanoid": "^3.3.18" }` while `"overrides": { "nanoid@^3": "3.3.18" }` exists.

Symptom:
```
npm error code EOVERRIDE
npm error Override for nanoid@^3.3.18 conflicts with direct dependency
```

Recovery:
```bash
# remove root dependencies.nanoid from package.json (keep the override)
npm install --no-fund --no-audit
```

## Success criteria

- `npm ls` shows `nanoid@3.3.18` (or newer patched 3.x) under web/ui-tui postcss chains
- `npm audit --workspace web|ui-tui` → found 0 vulnerabilities (for this advisory)
- `hermes doctor` → web/ui-tui lines green; npm issues gone from the summary list

## Longer-term

If the checkout is meant to track upstream, prefer a lockfile bump from `hermes update` / upstream commit so local override edits are not wiped on the next sync. Local `package.json` / lock changes are durable only until the next overwrite of those files.
