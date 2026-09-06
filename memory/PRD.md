# Tanix Repo Import (Copy-Only)

Date: 2026-06

## Task
Import `github.com/alifnewone7-create/tanix` @ `main` (`8df35ca`) byte-for-byte. No execution, no edits.

## Done
- Shallow clone to temp, `.git` deleted, temp removed. Repo history NOT merged.
- 19 root Python files + `pyquotex/` (34 files) + `data/` (4 files) -> `backend/`
- `README.md`, `.gitignore`, `pyproject.toml`, `tanix-bot.service`, `.github/workflows/` -> project root
- Collisions preserved: `backend/requirements.emergent.txt`, `README.emergent.md`, `.gitignore.emergent`
- `backend/server.py` and `backend/.env` untouched
- Verified via `diff -r --brief` and `cmp`: all 62 files byte-identical. Nothing installed, nothing started.

## Known deferred issues (accepted)
- Root-level Python files now in `backend/` -> relative imports (`from config import ...`) and `tanix-bot.service` paths broken.
- Repo `requirements.txt` is now the active backend manifest; FastAPI deps only declared in `requirements.emergent.txt`.
- Plaintext Telegram API ID/hash/token in `backend/config.py` and `backend/data/` — rotate before deploy.
- `.github/workflows/notify-telegram.yml` may auto-trigger if pushed to a GitHub remote.

## Backlog
- P0: decide integration direction (fix bot imports vs. wire bot to FastAPI vs. leave dormant)
- P1: dependency reconciliation between the two requirements files
- P1: secret rotation / move to `.env`
