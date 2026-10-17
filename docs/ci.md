# CI for the AP World Regions Map Quiz

This repo is one resource on the tklearn study hub (https://tkunst.github.io/). It shares the hub's CI setup, set up on 2026-10-16; the full description, including what was deliberately left out and how to add a new resource repo, is in the hub repo's [`docs/ci.md`](https://github.com/tkunst/tkunst.github.io/blob/main/docs/ci.md).

## What runs here

| Check | When | What it does |
|---|---|---|
| **ci: site-guard** | every push / PR | `scripts/site_guard.py` (shared with the hub; keep the copies identical) fails on: an em-dash; anything loaded from another site; any email except the published contact; an AP mention without the College Board trademark notice; missing `lang`, `<title>`, viewport meta, or image alt text; no link back to the hub. |
| **ci: smoke** | every push / PR | `tests/smoke_test.py` runs the quiz in headless Chromium at laptop (1366x768) and phone (390x844, touch) sizes. It checks that the script started, that there are 16 drop zones and 16 labels, places every label by tap-to-place (the iPad/Chromebook path), checks Part 1 scoring, reads the answer key from "Show correct answers", types all 16 answers in lower case with extra spaces and expects 16/16, confirms a misspelling is marked "close", and fails on any JavaScript error. |
| **secrets** | every push / PR | gitleaks over the full git history. |
| **Dependabot** | monthly | Bumps the workflow actions and Playwright (`tests/requirements.txt`). |

The hub's weekly `live` check also opens this quiz's published page and confirms it returns 200, has a title, and links back to the hub.

## Verified when set up

The smoke test failed, as it should, when answer grading was deliberately broken (0/16 instead of 16/16) and when the page's JavaScript was broken (no drop zones). The first Dependabot update (Playwright 1.60 to 1.63) passed CI and was merged.

## Running locally

```sh
python3 scripts/site_guard.py
pip install -r tests/requirements.txt
python -m playwright install chromium
python3 tests/smoke_test.py
```

## If you change the quiz

The smoke test depends on these element IDs and classes: `#jswarn`, `#map .zone`, `#bank .chip`, `#dragCheck`, `#dragScore`, `#tabType`, `#map .marker`, `#typeCheck`, `#typeReveal`, `#typeReset`, `#typeScore`, `#answers input`, `#answers .fb`. Renaming one means updating `tests/smoke_test.py` in the same commit.
