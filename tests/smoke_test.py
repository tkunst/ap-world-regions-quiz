#!/usr/bin/env python3
"""Browser smoke test for the regions quiz (Playwright, headless Chromium).

Plays both parts the way a student would, on a laptop-sized and a phone-sized
screen, and fails on any JavaScript error.

    pip install playwright && python -m playwright install chromium
    python3 tests/smoke_test.py
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

PAGE = pathlib.Path(__file__).resolve().parent.parent / "index.html"
N = 16

VIEWPORTS = {"laptop": {"width": 1366, "height": 768}, "phone": {"width": 390, "height": 844}}


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def run(browser, label, viewport):
    page = browser.new_page(viewport=viewport, has_touch=label == "phone")
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.goto(PAGE.as_uri())

    check(page.locator("#jswarn").is_hidden(), "JS did not start (preview warning still showing)")
    check(page.locator('a[href="/"]').count() >= 1, "missing link back to the hub")
    check(page.locator("#map .zone").count() == N, f"expected {N} drop zones")
    check(page.locator("#bank .chip").count() == N, f"expected {N} labels in the bank")

    positioned = page.evaluate("() => [...document.querySelectorAll('#map .zone')].every(z => z.style.left && z.style.top)")
    check(positioned, "drop zones not positioned on the map")

    # Part 1 via tap-to-place (the path that works on iPads/Chromebooks without dragging):
    # tap a label, tap a zone. Placing every label anywhere then checking must report a score.
    for i in range(N):
        page.locator("#bank .chip").first.click()
        page.locator("#map .zone").nth(i).click()
    check(page.locator("#bank .chip").count() == 0, "bank not empty after placing all labels")
    page.click("#dragCheck")
    score = page.locator("#dragScore").inner_text()
    check(f"/ {N} correct" in score, f"drag score text unexpected: {score!r}")

    # Part 2: get the answer key from "Show correct answers" (no page internals needed).
    page.click("#tabType")
    check(page.locator("#map .marker:visible").count() == N, f"expected {N} numbered markers in Part 2")
    page.click("#typeCheck")  # blank check unlocks "Show correct answers"
    page.click("#typeReveal")
    reveals = page.locator("#answers .fb").all_inner_texts()
    key = [t.replace("Answer: ", "").strip() for t in reveals]
    check(len(key) == N and all(key), "reveal did not show every answer")

    # Part 2: type every answer correctly (lower-case, extra spaces) -> full marks.
    page.click("#typeReset")
    inputs = page.locator("#answers input")
    for i, name in enumerate(key):
        inputs.nth(i).fill("  " + name.lower() + " ")
    page.click("#typeCheck")
    score = page.locator("#typeScore").inner_text()
    check(score.startswith(f"{N} / {N}"), f"typing every answer should score {N}/{N}, got {score!r}")

    # A near-miss spelling is "close", not right.
    page.click("#typeReset")
    inputs.nth(0).fill(key[0][:-1] + "x")
    page.click("#typeCheck")
    check("close" in (page.locator("#answers .fb").first.get_attribute("class") or ""), "misspelling not marked close")

    check(not errors, f"JavaScript errors: {errors}")
    page.close()
    print(f"ok  {label}: {N} zones, tap-to-place, {N}/{N} typed, close-spelling")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for label, vp in VIEWPORTS.items():
                run(browser, label, vp)
        finally:
            browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
