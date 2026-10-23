# CSTI: Cross-Stage Test Infrastructure

Course Project 1 (Software Design and Quality, Fall 2026), team of five. CSTI is a high-level design for test infrastructure that runs one automated-driving scenario, unchanged, in desktop simulation (MiL), on the target computer (PiL/HIL) and on a real vehicle on a closed course, where simulated traffic is injected around the vehicle's real position (ViL). The site covers the requirements summary, the high-level design, the traceability matrix, the design rationale and an evolution analysis.

**Live site:** https://YOUR-USERNAME.github.io/REPO-NAME/

## How to edit

The site in `docs/` is **generated**. Never edit files in `docs/` by hand: the next build overwrites them.

1. Edit the source in `src/`. Most changes go in `src/data.py`; diagrams are in `src/diagrams.py`.
2. Build: `python3 src/build.py docs`
3. Check: `python3 tools/check.py docs` (add `--mobile` if you have Playwright installed)
4. Commit **both** `src/` and `docs/`, then push. GitHub Pages republishes within a minute or two.

IDs are permanent. Never renumber or reuse one (FR-xx, C-xx, D-xx and so on); retire it instead. Any ID written in body text, such as `FR-03` or `C-12`, becomes a link automatically.

| To change… | Edit |
|---|---|
| Requirement wording, acceptance criterion, proposed values | `src/data.py`, requirements data |
| Short requirement label used in the matrix | `src/data.py`, `REQ` |
| Which components satisfy a requirement | `src/data.py`, `TRACE` (first entry = primary) |
| A component's description, owner, interfaces | `src/data.py`, `C["C-xx"]` |
| A design decision | `src/data.py`, `DEC` |
| Interfaces or the stack contract | `src/data.py`, `I`, `CONTRACT`, `MSG_SKETCH` |
| Evolution scenarios | `src/data.py`, `EVO` |
| Team member names or areas | `src/data.py`, `MEMBERS` and each component's `owner` |
| Glossary | `src/data.py`, `GLOSSARY` |
| A diagram | `src/diagrams.py` (one function per figure) |
| Page layout or section text | `src/build.py` |
| Colors and styling | `src/static/css/site.css` |

## Layout

```
src/         generator scripts and stylesheet
docs/        generated site (served by GitHub Pages)
tools/       check.py
```
