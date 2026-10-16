# AP World Regions Map Quiz

Self-contained practice quiz for the 16 AP World History regions: drag-and-drop labels, then type the names with no word bank.

Live: https://tkunst.github.io/ap-world-regions-quiz/

Part of the study-resources hub: https://tkunst.github.io/

The base map image is from a classroom handout and is not covered by the hub's CC BY-NC license.

## Privacy pre-push hook

Run `scripts/install-hooks.sh` once per clone. It blocks pushes containing locally configured private terms (`~/.config/privacy-gate/terms.txt`, kept outside the repo; fail-closed if missing).

## CI

- `ci` (every push/PR): `scripts/site_guard.py` (shared with the hub repo; keep identical) and `tests/smoke_test.py`, a headless-Chromium run of both parts on laptop and phone sizes. Run locally: `pip install -r tests/requirements.txt && python -m playwright install chromium && python3 tests/smoke_test.py`.
- `secrets`: gitleaks over the full history.
- Dependabot: workflow actions + Playwright, monthly.
