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

## Feature: Per-channel branding + 10-channel cap (June 2026)
Channel-scoped overrides stored inside each entry of `backend/data/channels.json`
(`image_name`, `text_name`, `owner_tag`); unset keys fall back to global defaults.

- `storage.py`: `MAX_CHANNELS = 10`, `BRAND_KEYS`, `DEFAULT_BRAND`, `get_channel`,
  `get_channel_brand`, `set_channel_brand`, `reset_channel_brand`.
  `add_channel` now returns `added` / `updated` / `limit`.
- `bot.py`: My Channels -> tap a channel -> Channel Settings with
  Change Image Name / Change Text Name / Change Owner Tag / Reset to Default.
  Free-text reply captured via `UI["await_brand"]`, 40-char cap.
  Add Channel blocked at 10 with a "remove one first" message.
- `charting.py`: `render_chart(..., brand=)` + `_draw_brand()` two-tone header
  wordmark (first word white, rest cyan) with renderer-measured spacing.
- `messages.py`: `signal_caption(..., brand=)` — same stylised mono font.
- `sessions.py`: `_broadcast_branded()` renders + captions per channel, caching
  the PNG per unique image name so identical branding renders once.

Verified with a throwaway script (since removed): brand set/get isolation between
channels, caption output, 10-channel limit, reset, and PNG render for 3 brand names.
Bot itself not started (no `.env` / BOT_TOKEN in this environment).

## Known deferred issues (accepted)
- Root-level Python files now in `backend/` -> relative imports (`from config import ...`) and `tanix-bot.service` paths broken.
- Repo `requirements.txt` is now the active backend manifest; FastAPI deps only declared in `requirements.emergent.txt`.
- Plaintext Telegram API ID/hash/token in `backend/config.py` and `backend/data/` — rotate before deploy.
- `.github/workflows/notify-telegram.yml` may auto-trigger if pushed to a GitHub remote.

## Backlog
- P0: decide integration direction (fix bot imports vs. wire bot to FastAPI vs. leave dormant)
- P1: dependency reconciliation between the two requirements files
- P1: secret rotation / move to `.env`
