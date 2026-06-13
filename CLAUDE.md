# CLAUDE.md — engineering notes

> Notes for anyone (human or AI assistant) touching this code. It's the first thing to read
> and the first thing to update when something surprising happens.

## What this is
<!-- One paragraph: what it does, who it's for, the live URL. -->

## Stack
<!-- e.g. TypeScript · React · Vite · Vitest · <backend> · <cloud> -->

## File layout
```
src/            — app code
  lib/          — pure logic + co-located *.test.ts
  components/   — UI
docs/           — testing strategy, build journal, case study
scripts/        — idempotent setup / deploy / ops scripts
.githooks/      — the pre-commit Inspector (git config core.hooksPath .githooks)
```

## Dev commands
```bash
npm install
npm run dev            # local dev
npm test               # unit tests (must be non-interactive, e.g. "vitest run")
npm run lint           # eslint
npx tsc --noEmit       # type-check (the Inspector runs this as a hard gate)
```

## Conventions
- **Conventional Commits**: `feat(scope):`, `fix:`, `docs:`, `chore:`, `test:` — with the *why* in the body.
- **New user-facing features default OFF** — opt in, don't force.
- **Config via env**, never literals. `.env.example` lists every key.
- **Tests co-located** as `*.test.ts`; test the risky surfaces (see [docs/testing.md](docs/testing.md)).

## Cloud resource IDs
<!-- The single source of truth for "what's deployed where". Fill in once provisioned. -->
| Resource | Name / ID | Region |
|---|---|---|
| _e.g. bucket_ | _name_ | _region_ |

## Gotchas
<!-- Append every surprising bug here the moment you understand it. -->
- …

## Rollback playbook
> The first time you need this is the worst time to write it. Fill it in BEFORE launch.

| Symptom | First check | Likely fix |
|---|---|---|
| Site broken after deploy | which revision/version is serving? | `git revert <sha>` + redeploy |
| API 5xx spike | logs for the failing route | roll back the function version |
| _…_ | _…_ | _…_ |

**Cannot be rolled back** (handle with care): schema migrations, key rotations, anything
that deletes data. List yours here.
