"""Export CSTI requirements to a tracking CSV.

Usage: python3 tools/export_requirements.py [out.csv]   (run from the repo root)
"""
import csv, html, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import requirements_data as R
import data as D

# Names used on the site, without building the pages.
src_text = open(os.path.join(os.path.dirname(__file__), "..", "src", "build.py")).read()
ns = {}
for var in ("PV_SHORT", "CON_NAMES"):
    m = re.search(var + r" = (\{.*?\})\n", src_text, re.S)
    ns[var] = eval(m.group(1)) if m else {}
PV, CON = ns["PV_SHORT"], ns["CON_NAMES"]
USERS = {u[0]: u[1] for u in R.REQPAGE_STAKEHOLDERS}


def plain(s):
    s = re.sub(r'<a[^>]*href="#(PV-\d+)"[^>]*>.*?</a>', lambda m: PV.get(m.group(1), m.group(1)) + " (proposed)", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\b(PV-\d{2})\b", lambda m: PV.get(m.group(1), m.group(1)) + " (proposed)", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def source(codes):
    users, cons = [], []
    for c in [c.strip() for c in codes.split(",") if c.strip()]:
        (users if c in USERS else cons).append(USERS.get(c) or CON.get(c) or c)
    parts = (["stakeholder need: " + "; ".join(users)] if users else []) + (["constraint: " + "; ".join(cons)] if cons else [])
    return "CSTI Requirements Summary (Project 1); " + "; ".join(parts)


def rows():
    for group, block in (("Functional", R.REQPAGE_FUNCTIONAL), ("Non-functional", R.REQPAGE_NONFUNCTIONAL), ("Safety", R.REQPAGE_SAFETY)):
        for _section, reqs in block[1]:
            for r in reqs:
                comps = D.TRACE.get(r["id"], [])
                primary = D.C[comps[0]] if comps else None
                team = f'{primary["owner"]} ({D.MEMBERS[primary["owner"]]})' if primary else ""
                feature = ", ".join(D.C[c]["name"] for c in comps)
                yield [D.REQ[r["id"]], plain(r["text"]), source(r["src"]),
                       "Acceptance criterion: " + plain(r["accept"]) + f' Verification: {r["ver"]}. Priority: {r["prio"].capitalize()}. Type: {group}.',
                       team, feature, "", "", "", "", "", "", ""]


out = sys.argv[1] if len(sys.argv) > 1 else "requirements.csv"
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Name", "Requirement", "Source/Document of Origin", "Quote", "Responsible Team", "Sub-System/Feature",
                "MIL Test Case ID", "HIL Test Case ID", "VIL Test Case ID", "MIL Test Result", "HIL Test Result",
                "VIL Test Result", "SW Version"])
    n = 0
    for row in rows():
        w.writerow(row); n += 1
print(f"wrote {n} requirements to {out}")
