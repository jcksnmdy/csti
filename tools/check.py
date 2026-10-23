#!/usr/bin/env python3
"""Check the generated site before committing.

Usage:
    python3 tools/check.py [SITE_DIR] [--mobile]

SITE_DIR defaults to docs/ at the repo root. Checks:
  - every relative href (and #anchor) resolves to a file / id
  - HTML tags nest properly
  - no duplicate ids on a page
  - prints a word count (text outside SVG diagrams)
  --mobile  also loads each page at 390 px wide with Playwright (if installed)
            and reports pages that scroll sideways.
Exits non-zero if anything fails.
"""
import html
import glob
import os
import re
import sys
from collections import Counter
from html.parser import HTMLParser

VOID = {"meta", "link", "br", "hr", "img", "input", "path", "circle", "rect", "source", "wbr"}


class Nesting(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            open_tag = self.stack[-1] if self.stack else None
            self.errors.append(f"line {self.getpos()[0]}: </{tag}> but open tag is {open_tag}")


ID_RE = re.compile(r"\b(?:FR|NFR|SR|CON|PV|D|C|I|E|U)-\d{2}\b|\bN[1-5]\b")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mobile = "--mobile" in sys.argv
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    site = os.path.abspath(args[0]) if args else os.path.join(repo_root, "docs")
    if not os.path.isdir(site):
        print(f"No site directory at {site}")
        return 2

    files = sorted(glob.glob(os.path.join(site, "**", "*.html"), recursive=True))
    if not files:
        print(f"No HTML files under {site}")
        return 2

    ids, problems, words = {}, [], 0
    for f in files:
        ids[f] = re.findall(r'\bid="([^"]+)"', open(f, encoding="utf-8").read())

    for f in files:
        rel = os.path.relpath(f, site)
        s = open(f, encoding="utf-8").read()

        dups = [i for i, n in Counter(ids[f]).items() if n > 1]
        if dups:
            problems.append(f"{rel}: duplicate ids {dups}")

        p = Nesting()
        p.feed(s)
        for e in p.errors[:5]:
            problems.append(f"{rel}: {e}")
        if p.stack:
            problems.append(f"{rel}: unclosed tags {[t for t, _ in p.stack[-3:]]}")

        for h in re.findall(r'href="([^"]+)"', s):
            if re.match(r"^(https?:|mailto:|tel:)", h):
                continue
            path, _, frag = h.partition("#")
            target = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f
            if not os.path.exists(target):
                problems.append(f"{rel}: broken link {h}")
            elif frag and target.endswith(".html") and frag not in set(ids.get(target, [])):
                problems.append(f"{rel}: missing anchor {h}")

        body = re.sub(r"<svg.*?</svg>", " ", s, flags=re.S)
        body = re.sub(r"<(script|style).*?</\1>", " ", body, flags=re.S)
        words += len(re.sub(r"<[^>]+>", " ", body).split())
        visible = re.sub(r"<(code|pre|title)\b.*?</\1>", " ", body, flags=re.S)
        visible = html.unescape(re.sub(r"<[^>]+>", " ", visible))
        for m in ID_RE.finditer(visible):
            ctx = visible[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")
            problems.append(f"{rel}: visible ID '{m.group(0)}' in: ...{ctx}...")

    if mobile:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("--mobile skipped: Playwright is not installed (pip install playwright).")
        else:
            with sync_playwright() as pw:
                b = pw.chromium.launch()
                pg = b.new_page(viewport={"width": 390, "height": 800})
                for f in files:
                    pg.goto("file://" + f)
                    w = pg.evaluate("document.documentElement.scrollWidth")
                    if w > 390:
                        problems.append(f"{os.path.relpath(f, site)}: {w}px wide at 390px (scrolls sideways)")
                b.close()

    print(f"Checked {len(files)} pages in {site}")
    print(f"Words (outside diagrams): {words:,} (~{words // 500} report pages at 500 words/page)")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for x in problems:
            print("  - " + x)
        return 1
    print("OK: links, anchors, nesting and ids all pass" + (" (mobile width too)" if mobile else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
