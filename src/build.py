"""Builds the whole CSTI site. Usage: python3 build.py [OUTDIR]  (default /home/claude/site)."""
import os, re, sys, shutil
from data import *
from requirements_data import *
import diagrams

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else "/home/claude/site"
for sub in ("", "components", "img", "css"):
    os.makedirs(os.path.join(SITE, sub), exist_ok=True)
shutil.copytree(os.path.join(HERE, "static"), SITE, dirs_exist_ok=True)

NAV = [("index.html", "Overview"), ("requirements.html", "Requirements"), ("design.html", "Design"), ("integration.html", "Fusion"),
       ("traceability.html", "Traceability"), ("rationale.html", "Rationale"), ("evolution.html", "Evolution"),
       ("glossary.html", "Glossary")]
COMP_IDS = sorted(C)


def page(fname, title, lede, body, current, pre="", toc=None, doc_title=None, link=True):
    nav = "".join(f'<li><a href="{pre}{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a></li>' for h, t in NAV)
    tochtml = ""
    if toc:
        tochtml = ('<nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>' +
                   "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in toc) + "</ol></nav>")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{doc_title or title} — Cross-Stage Test Infrastructure</title>
<link rel="stylesheet" href="{pre}css/site.css">
</head>
<body>
<header class="site-header">
  <div class="inner">
    <p class="site-title"><a href="{pre}index.html">Cross-Stage Test Infrastructure (CSTI)</a></p>
    <p class="site-subtitle">One scenario, every stage: MiL &rarr; PiL &rarr; HIL &rarr; Vehicle-in-the-Loop</p>
    <nav class="site-nav" aria-label="Site"><ul>{nav}</ul></nav>
  </div>
</header>
<main>
<div class="page-head"><h1>{title}</h1>{f'<p class="lede">{lede}</p>' if lede else ''}</div>
{tochtml}
{autolink(body, pre)}
</main>
<footer class="site-footer"><div class="inner">Project 1 · Software Design and Quality · Fall 2026 · Team of five (Members 1–5). Hardware and vehicle details are generic by design.</div></footer>
</body>
</html>
"""
    with open(os.path.join(SITE, fname), "w") as f:
        f.write(html)


TOKEN = re.compile(r"\b(FR|NFR|SR|CON|PV|D|C|I|E|U)-(\d{2})(?:\.(\d))?\b")
NODE = re.compile(r"\bN([1-5])\b")
NODE_NAMES = {"1": "desktop workstation", "2": "target computer", "3": "in-vehicle test computer",
              "4": "GPU sensor-simulation host", "5": "real-time plant simulator"}
CON_NAMES = {"CON-01": "ROS 2 stack in one container", "CON-02": "Stack not modified", "CON-03": "Generic hardware, public site",
             "CON-04": "Closed course with safety driver", "CON-05": "Vehicle localization on ROS 2", "CON-06": "No single vendor format"}
DEC_NAMES = {"D-01": "Simulator-agnostic scenario format", "D-02": "Adapter pattern", "D-03": "CSTI owns actor behavior",
             "D-04": "Object-level injection in ViL", "D-05": "One clock master per stage", "D-06": "Frozen stack contract",
             "D-07": "Injection on fusion's existing topics", "D-08": "CSTI has no safety authority",
             "D-10": "Stop injecting on a stack fault", "D-11": "Record everything", "D-12": "Run-lifecycle state machine",
             "D-13": "Validate before the run", "D-14": "Pose extrapolation", "D-15": "ROS 2 stack with C++ fusion core"}
PV_SHORT = {"PV-01": "50 ms", "PV-02": "1 ms", "PV-03": "0.20 m", "PV-04": "0.5°", "PV-05": "1.0 m", "PV-06": "20 actors",
            "PV-07": "60 minutes", "PV-08": "15 m/s", "PV-09": "2 s", "PV-10": "100 ms", "PV-13": "0.10 m"}


def display(kind, num, sub):
    tid = f"{kind}-{num}"
    if kind in ("FR", "NFR", "SR"):
        return REQ.get(tid)
    if kind == "CON":
        return CON_NAMES.get(tid)
    if kind == "PV":
        return PV_SHORT[tid] + " (proposed)" if tid in PV_SHORT else None
    if kind == "D":
        return DEC_NAMES.get(tid)
    if kind == "E":
        return next((e["title"] for e in EVO if e["id"] == tid), None)
    if kind == "U":
        return next((u[1] for u in REQPAGE_STAKEHOLDERS if u[0] == tid), None)
    if kind == "I":
        return next((i[1] for i in I if i[0] == tid), None)
    if kind == "C":
        if tid not in C:
            return None
        if sub:
            return next((x[1] for x in C[tid].get("subs", []) if x[0] == f"{tid}.{sub}"), None)
        return C[tid]["name"]
    return None


def target(kind, num, sub, pre):
    tid = f"{kind}-{num}"
    if kind in ("FR", "NFR", "SR", "CON", "PV"):
        return f"{pre}requirements.html#{tid}"
    if kind == "U":
        return f"{pre}requirements.html#stakeholders"
    if kind == "D":
        return f"{pre}rationale.html#{tid}"
    if kind == "E":
        return f"{pre}evolution.html#{tid}"
    if kind == "I":
        return f"{pre}design.html#{tid}"
    if kind == "C":
        if tid not in C or (sub and f"{tid}.{sub}" not in [x[0] for x in C[tid].get("subs", [])]):
            return None
        return f"{pre}components/{tid}.html" + (f"#{tid}-{sub}" if sub else "")
    return None


def name_of(tid):
    m = TOKEN.fullmatch(tid)
    return display(m.group(1), m.group(2), m.group(3)) if m else tid


def autolink(html, pre):
    """Render every ID as its name: linked outside links, plain inside links; leave svg/code/pre untouched."""
    out, skip, in_a = [], 0, 0
    for part in re.split(r"(<[^>]+>)", html):
        if part.startswith("<"):
            t = part.lower()
            if re.match(r"<(svg|code|pre|title|style|script)\b", t):
                skip += 1
            elif re.match(r"</(svg|code|pre|title|style|script)>", t):
                skip -= 1
            elif re.match(r"<a\b", t):
                in_a += 1
            elif t.startswith("</a"):
                in_a -= 1
            out.append(part)
            continue
        if skip > 0:
            out.append(part)
            continue
        def rep(m):
            name = display(m.group(1), m.group(2), m.group(3))
            if not name:
                return m.group(0)
            if in_a:
                return name
            href = target(m.group(1), m.group(2), m.group(3), pre)
            cls = "ref" if m.group(1) in ("FR", "NFR", "SR", "CON", "D", "E") else ("pv" if m.group(1) == "PV" else "cref")
            return f'<a class="{cls}" href="{href}">{name}</a>' if href else name
        part = TOKEN.sub(rep, part)
        def node_rep(m):
            n = NODE_NAMES[m.group(1)]
            before = part[:m.start()].rstrip()
            return n[0].upper() + n[1:] if (not before or before[-1] in ".;:(") else n
        part = NODE.sub(node_rep, part)
        out.append(part)
    return "".join(out)


def table(headers, rows, cls=""):
    h = "".join(f"<th>{x}</th>" for x in headers)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'


def fig(key, caption, pre=""):
    svg = diagrams.ALL[key]().svg()
    with open(f"{SITE}/img/{key}.svg", "w") as f:
        f.write(diagrams.ALL[key]().svg(standalone=True))
    return f'<figure class="diagram">{svg}<figcaption>{caption} <a href="{pre}img/{key}.svg">Open as image</a>.</figcaption></figure>'


def comps_for(req):
    return TRACE.get(req, [])


def reqs_for(c):
    return [(r, "P" if TRACE[r][0] == c else "S") for r in REQ if c in TRACE[r]]


def decs_for_req(r):
    return [d["id"] for d in DEC if r in d["reqs"]]


# ===================================================================== design
def build_design():
    b = []
    b.append('<h2 id="glance">1. Architecture at a glance</h2>')
    b.append("<p>The stack and the scenario never change between stages; only what sits between them does. A scenario is written once (C-01), the runtime turns it into actors, vehicle motion and sensor data, and one gateway delivers that data to the stack (C-11). CSTI has no safety role: the stack's own fault detection, state machines and safety interlock keep the vehicle safe, and CSTI stops injecting when the stack reports a fault. Everything is recorded (C-13).</p>")
    b.append(table(["Principle", "What it means here", "Decisions"], [
        ["One source of truth per concern", "One scenario, one owner of actor motion, one vehicle state, one clock.", "D-01, D-03, D-05"],
        ["Simulator code only at the edge", "Only the adapters touch simulator-specific code.", "D-02"],
        ["One frozen contract to the stack", "Every stage reaches the stack the same way.", "D-06, D-07"],
        ["Safety stays in the stack", "CSTI only listens to the stack's status and stops injecting.", "D-08, D-10"],
        ["Everything is evidence", "Every input, output and decision is recorded.", "D-11"],
    ]))

    b.append('<h2 id="context">2. Context view</h2>')
    b.append(fig("context", "Figure 1. CSTI, its users, the stack under test, the simulators and the vehicle. Real sensor data goes straight to the stack (SR-01)."))

    b.append('<h2 id="components">3. Component view</h2>')
    b.append(fig("component", "Figure 2. How test data flows from scenario to stack. The operator view is not drawn; see its page below."))
    rows = []
    for cid in COMP_IDS:
        c = C[cid]
        rows.append([f'<a href="components/{cid}.html">{c["name"]}</a>', c["resp"], c["tool"]])
    b.append('<h3 id="component-pages">Component pages</h3>')
    b.append("<p>Each page covers one component: what it is for, what it connects to, how it differs by stage, what happens when it fails, and the requirements and decisions behind it.</p>")
    b.append(table(["Page", "Purpose", "Tool"], rows))

    b.append('<h2 id="interfaces">4. Interfaces</h2>')
    b.append("<p><strong>Frozen</strong> interfaces never change incompatibly, <strong>versioned</strong> ones change only with a version both sides check, and <strong>internal</strong> ones may change within the team.</p>")
    b.append(table(["Interface", "From", "To", "Purpose", "Stability"],
                   [[f'<span id="{i[0]}"></span>{i[1]}', i[2], i[3], i[4], i[6]] for i in I]))
    b.append('<h3 id="contract">What crosses the stack boundary</h3>')
    b.append(table(["Direction", "Data", "Stages"], [list(r) for r in BOUNDARY]))

    b.append('<h2 id="deployment">5. Deployment view</h2>')
    b.append("<p>Controls and perception each run MiL and PiL separately, then come together in HIL on the sensor cart and in ViL on the car.</p>")
    b.append(fig("stages", "Figure 3. Stages by track. The tracks join in HIL."))
    b.append("<h3>Controls MiL</h3>")
    b.append(fig("mil-controls", "Figure 3a. Controls MiL: Simulink controllers against RoadRunner Scenario on one desktop. No fusion and no interlock."))
    b.append("<h3>Perception MiL</h3>")
    b.append(fig("mil-perception", "Figure 3b. Perception MiL: sensor placement and specs checked in RoadRunner; AURELION adds realistic sensor data and sensor faults on the desktop."))
    b.append("<h3>Controls PiL</h3>")
    b.append(fig("pil-controls", "Figure 3c. Controls PiL: code-generated C++ controller nodes on the AUTERA, fed ground truth over ROS 2."))
    b.append("<h3>Perception PiL</h3>")
    b.append(fig("pil-perception", "Figure 3d. Perception PiL: AURELION on the desktop feeds RTMaps and the C++ object fusion on the AUTERA."))
    b.append("<h3>HIL: the sensor cart</h3>")
    b.append(fig("hil", "Figure 3e. HIL: the sensor cart's real sensors feed RTMaps and the full stack on the AUTERA; the stack commands the Simulink vehicle model on the bench over Ethernet."))
    b.append("<h3>ViL: controls and perception</h3>")
    b.append(fig("vil", "Figure 3f. ViL: real sensors plus CSTI's virtual object lists on the car; the Intrepid logger records and uploads to the cloud."))
    b.append(table(["Part", "MiL", "PiL", "HIL", "ViL"], [
        ["Scenario, validation, orchestration", "Desktop", "Desktop", "Desktop", "In-vehicle test computer"],
        ["Controls and vehicle model", "Simulink controllers and vehicle model on the desktop", "C++ controller nodes on the AUTERA; Simulink vehicle model", "Simulink vehicle model on the HIL bench", "The real vehicle"],
        ["Sensors", "RoadRunner objects (controls); RoadRunner placement plus AURELION data and faults (perception)", "RoadRunner ground truth (controls); AURELION into RTMaps on the AUTERA (perception)", "Sensor cart: real sensors into RTMaps", "Real sensors plus headless player"],
        ["Gateway and stack", "Desktop", "Target computer", "Target computer", "Target computer"],
        ["Stack safety interlock", "Not used", "Not used", "Active", "Active"],
        ["Recording", "Desktop", "Desktop", "Intrepid data logger, uploaded to the cloud", "Intrepid data logger, uploaded to the cloud"],
    ]))
    b.append("<p>The in-vehicle test computer and the target computer share a dedicated test network; no cellular link is in the actuation path.</p>")

    b.append('<h2 id="lifecycle">6. Run lifecycle</h2>')
    b.append(fig("lifecycle", "Figure 4. Every run follows this state machine. On the desktop, injection starts automatically; on HIL and the vehicle it needs the stack ready and the operator's confirmation."))

    b.append('<h2 id="testing">7. Test tracking</h2>')
    b.append("<p>Simulink Test Manager runs each RoadRunner scenario and its variants against the models in MiL and PiL, and its test cases are linked to the requirements in Requirements Toolbox, so every run updates each requirement's pass or fail status. HIL and vehicle results join the same view as result files, and scenes rebuilt from real map data rerun the same tests. The requirements page explains how the team's Excel sheet stays in sync.</p>")

    page("design.html", "High-Level Design",
         "How CSTI is built: its context, components, interfaces, deployment and run lifecycle.",
         "\n".join(b), "design.html",
         toc=[("glance", "Architecture at a glance"), ("context", "Context view"), ("components", "Component view"),
              ("component-pages", "Component pages"), ("interfaces", "Interfaces"), ("deployment", "Deployment view"),
              ("lifecycle", "Run lifecycle"), ("testing", "Test tracking")])


# ===================================================================== components
def build_components():
    for n, cid in enumerate(COMP_IDS):
        c = C[cid]
        pre = "../"
        b = [f'<p class="crumb"><a href="../design.html#components">Design</a> › {c["name"]}</p>']
        kv = [["Responsibility", c["resp"]], ["Tool category", "«tool» " + c["tool"]], ["Owner", c["owner"]], ["Group", c["group"]], ["Deployment", c["node"]],
              ["Provides", ", ".join(c["provides"]) or "—"], ["Requires", ", ".join(c["requires"]) or "—"]]
        b.append('<div class="table-wrap"><table class="kv"><tbody>' + "".join(
            f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in kv) + "</tbody></table></div>")
        b.append("<h2>Description</h2>" + "".join(f"<p>{p}</p>" for p in c["body"]))
        if c.get("subs"):
            b.append("<h2>Sub-components</h2>")
            b.append(table(["Name", "Role"], [[f'<span id="{s[0].replace(".", "-")}"></span>{s[1]}', s[2]] for s in c["subs"]]))
        b.append("<h2>Key behaviors</h2><ul>" + "".join(f"<li>{x}</li>" for x in c["behaviors"]) + "</ul>")
        b.append(f"<h2>Stage variation</h2><p>{c['stages']}</p>")
        b.append(f"<h2>Failure behavior</h2><p>{c['failure']}</p>")
        rs = reqs_for(cid)
        b.append(f"<h2>Requirements satisfied ({len(rs)})</h2>")
        b.append('<ul class="reqlist">' + "".join(
            f'<li>{r} <span class="{"mk-p" if k == "P" else "mk-s"}">({"primary" if k == "P" else "supporting"})</span></li>' for r, k in rs) + "</ul>")
        b.append("<h2>Related decisions</h2><ul>" + "".join(
            f'<li>{d}</li>' for d in c["decisions"]) + "</ul>")
        prev_c = COMP_IDS[n - 1] if n else None
        next_c = COMP_IDS[n + 1] if n + 1 < len(COMP_IDS) else None
        navp = []
        if prev_c:
            navp.append(f'← <a href="{prev_c}.html">{C[prev_c]["name"]}</a>')
        if next_c:
            navp.append(f'<a href="{next_c}.html">{C[next_c]["name"]}</a> →')
        b.append('<p class="crumb">' + " · ".join(navp) + "</p>")
        page(f"components/{cid}.html", c['name'], None, "\n".join(b), "design.html", pre=pre)


# ===================================================================== traceability
def build_trace():
    b = []
    b.append('<h2 id="matrix">1. Requirements to components</h2>')
    b.append('<p><span class="mk-p">●</span> primary responsibility · <span class="mk-s">○</span> supporting. Decisions are listed per row.</p>')
    head = "<th>Requirement</th>" + "".join(f'<th class="c vert"><a href="components/{c}.html"><span>{C[c].get("short", C[c]["name"])}</span></a></th>' for c in COMP_IDS) + "<th>Decisions</th>"
    rows = []
    for grp, pfx in (("Functional", "FR-"), ("Non-functional", "NFR-"), ("Safety", "SR-")):
        rows.append(f'<tr class="grp"><td colspan="{len(COMP_IDS) + 2}">{grp}</td></tr>')
        for r in [x for x in REQ if x.startswith(pfx)]:
            cells = ""
            for c in COMP_IDS:
                cs = TRACE[r]
                mk = '<span class="mk-p">●</span>' if cs[0] == c else ('<span class="mk-s">○</span>' if c in cs else "")
                cells += f'<td class="m">{mk}</td>'
            rows.append(f'<tr><td class="lab">{r}</td>{cells}<td>{", ".join(decs_for_req(r)) or "—"}</td></tr>')
    b.append(f'<div class="table-wrap"><table class="matrix"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')

    b.append('<h2 id="reverse">2. Components to requirements</h2>')
    rows = []
    for c in COMP_IDS:
        rs = reqs_for(c)
        p = [r for r, k in rs if k == "P"]
        s = [r for r, k in rs if k == "S"]
        rows.append([c, C[c]["owner"], ", ".join(p) or "—", ", ".join(s) or "—", str(len(rs))])
    b.append(table(["Component", "Owner", "Primary for", "Supports", "Total"], rows))

    b.append('<h2 id="constraints">3. Constraints to design</h2>')
    b.append(table(["Constraint", "Where the design honors it"], [
        ["CON-01", "Gateway on fusion's ROS 2 inputs (D-15)."],
        ["CON-02", "Frozen contract (D-06) on fusion's existing topics (D-07)."],
        ["CON-03", "Vehicle-specific values live in a vehicle profile, not on this site."],
        ["CON-04", "CSTI has no safety role; the stack's own safety chain and the driver keep the vehicle safe (D-08, E-04)."],
        ["CON-05", "Read by the ego-state bridge."],
        ["CON-06", "Open scenario format (D-01) and adapters (D-02)."],
    ]))

    # checks
    untraced = [r for r in REQ if not TRACE.get(r)]
    orphan = [c for c in COMP_IDS if not reqs_for(c)]
    b.append('<h2 id="checks">4. Completeness checks</h2>')
    b.append(f"<ul><li><strong>Forward:</strong> {len(REQ) - len(untraced)} of {len(REQ)} requirements trace to at least one component. Untraced: {', '.join(untraced) or 'none'}.</li>"
             f"<li><strong>Backward:</strong> {len(COMP_IDS) - len(orphan)} of {len(COMP_IDS)} components trace to at least one requirement. Components with no requirement: {', '.join(orphan) or 'none'}.</li>"
             f"<li><strong>Decisions:</strong> all {len(DEC)} decisions on the rationale page cite at least one requirement.</li></ul>")
    b.append('<h2 id="gaps">5. Gaps and weak spots</h2>')
    b.append(table(["Requirement(s)", "Issue"], [[g[0], g[1]] for g in GAPS]))

    page("traceability.html", "Traceability Matrix",
         "How every requirement maps to the components that satisfy it, in both directions, with the gaps called out.",
         "\n".join(b), "traceability.html",
         toc=[("matrix", "Requirements to components"), ("reverse", "Components to requirements"),
              ("constraints", "Constraints to design"), ("checks", "Completeness checks"), ("gaps", "Gaps and weak spots")])


# ===================================================================== rationale
def build_rationale():
    b = ["<p>Each decision lists the requirements that drove it, the options, the choice, why, and what it costs.</p>"]
    b.append('<h2 id="summary">Summary</h2>')
    b.append(table(["Decision", "Driven by"], [[f'<a href="#{d["id"]}">{d["title"]}</a>', ", ".join(d["reqs"])] for d in DEC]))
    b.append('<h2 id="decisions">Decisions</h2>')
    for d in DEC:
        opts = "".join(f"<li><strong>{o[0]}.</strong> {o[1]}</li>" for o in d["options"])
        choice = re.sub(r"^Option (\d)", lambda m: "Chosen: <em>" + d["options"][int(m.group(1)) - 1][0] + "</em>", d["choice"])
        b.append(f'<div class="decision" id="{d["id"]}"><h3>{d["title"]}</h3>'
                 f'<p class="meta">Requirements: {", ".join(d["reqs"])} · Components: {", ".join(d["comps"])}</p>'
                 f'<dl><dt>Issue</dt><dd>{d["issue"]}</dd><dt>Options considered</dt><dd><ul>{opts}</ul></dd>'
                 f'<dt>Decision</dt><dd>{choice}</dd><dt>Justification</dt><dd>{d["why"]}</dd>'
                 f'<dt>Trade-offs accepted</dt><dd>{d["cons"]}</dd></dl></div>')
    b.append('<h2 id="evolved">How the design evolved</h2>')
    b.append(table(["Topic", "What changed and why"], [[h[0], h[1]] for h in HISTORY]))
    page("rationale.html", "Design Rationale",
         "The key design decisions and the requirements behind them.",
         "\n".join(b), "rationale.html",
         toc=[("summary", "Summary"), ("decisions", "Decisions"), ("evolved", "How the design evolved")])


# ===================================================================== evolution
def build_evolution():
    b = []
    b.append('<h2 id="tiers">1. Stability tiers</h2>')
    b.append(table(["Tier", "Interfaces", "Rule"], [
        ["Frozen", "I-11, I-18, I-19", "Never changed incompatibly; the stack contract only grows."],
        ["Versioned", "I-01, I-03, I-04, I-08, I-12, I-14, I-20", "Changes need a new version."],
        ["Internal", "All others", "May change if both owners agree."],
    ]))
    b.append('<h2 id="scenarios">2. Change scenarios</h2>')
    for e in EVO:
        rows = []
        for c in COMP_IDS:
            if c in e["impact"]:
                k, t = e["impact"][c]
                lab = {"chg": "Changes", "cfg": "Configuration only", "add": "Additions only", "ref": "Refuses"}[k]
                rows.append([c, f'<span class="{"chg" if k in ("chg", "ref") else "cfg"}">{lab}</span>', t])
        unchanged = [c for c in COMP_IDS if c not in e["impact"]]
        b.append(f'<h3 id="{e["id"]}">{e["title"]}</h3>')
        b.append(f'<p><em>{e["story"]}</em></p>')
        b.append(table(["Component", "Impact", "What"], rows))
        if e["id"] != "E-04":
            b.append(f"<p><strong>Unchanged:</strong> {len(unchanged)} of {len(COMP_IDS)} components, the stack and every scenario.</p>")
        b.append(f'<p>{e["text"]}</p>')
        b.append(f'<p class="crumb">Requirements: {", ".join(e["reqs"])} · Decisions: {", ".join(e["decs"])}</p>')
    b.append('<h2 id="summary">3. Impact summary</h2>')
    head = ["Scenario"] + [f'<span>{C[c].get("short", C[c]["name"])}</span>' for c in COMP_IDS] + ["<span>Stack</span>", "<span>Scenarios</span>"]
    sym = {"chg": "●", "cfg": "◐", "add": "+", "ref": "✕"}
    rows = []
    for e in EVO:
        rows.append([e['title']] + [f'<span class="{"mk-p" if e["impact"].get(c, ("",))[0] in ("chg", "ref") else "mk-s"}">{sym.get(e["impact"].get(c, ("",))[0], "")}</span>' for c in COMP_IDS] + ["—", "—"])
    b.append(table(head, rows, "matrix vhead"))
    b.append("<p>● changes · ◐ configuration only · + additions only · ✕ refuses · blank: unchanged.</p>")
    page("evolution.html", "Evolution",
         "Which parts change, and which do not, for four likely changes.",
         "\n".join(b), "evolution.html",
         toc=[("tiers", "Stability tiers"), ("scenarios", "Change scenarios"), ("summary", "Impact summary")])


# ===================================================================== glossary, index
def build_integration():
    import integration
    page("integration.html", "Sensor Fusion and Integration",
         "What sensor fusion means on this vehicle, where it runs, and where CSTI connects to it.",
         integration.body(fig, table), "integration.html",
         toc=[("definition", "What sensor fusion means here"), ("sensors", "Sensors and what fusion receives"), ("datapath", "Where CSTI connects"), ("simchain", "Simulation chain"), ("sources", "Sources")])


def build_glossary():
    b = '<dl class="defs">' + "".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in sorted(GLOSSARY, key=lambda g: g[0].lower())) + "</dl>"
    page("glossary.html", "Glossary", "Terms and abbreviations used on this site.", b, "glossary.html")


def build_index():
    b = []
    b.append('<h2 id="problem">The problem</h2>')
    b.append("<p>Automated-driving software is tested on a desktop (MiL), on its target computer (PiL), on a hardware bench (HIL) and on the real vehicle (ViL). Each stage usually has its own copy of every test, so the copies drift and results don't compare. The vehicle is the most expensive place to find that out.</p>")
    b.append('<h2 id="solution">Our design</h2>')
    b.append("<p>The <strong>Cross-Stage Test Infrastructure (CSTI)</strong> runs one scenario unchanged in every stage. On the vehicle, virtual traffic is injected into the stack around the car's real position, and the stack cannot tell it from real sensors. CSTI has no safety role: when the stack's own safety chain reports a fault, CSTI stops injecting.</p>")
    b.append(table(["Stage", "Where the stack runs", "Vehicle", "Sensors"], [
        ["MiL", "Desktop", "Simulink controllers and vehicle model; no safety interlock", "RoadRunner objects (controls); AURELION sensor data and faults (perception)"],
        ["PiL", "AUTERA AutoBox: C++ controller nodes (controls); RTMaps and object fusion (perception)", "Simulink vehicle model", "RoadRunner ground truth (controls); AURELION data (perception)"],
        ["HIL", "AUTERA, real time, safety interlock active", "Simulink vehicle model on the HIL bench", "Sensor cart: real sensors through RTMaps"],
        ["ViL", "Target computer, in the vehicle, full safety chain", "The real vehicle with a safety driver", "Real sensors plus virtual object lists"],
    ]))
    b.append('<p>The customer is the Virginia Tech HEVT EcoCAR CAV sub-team; users are listed on the <a href="requirements.html#stakeholders">requirements page</a>.</p>')
    b.append('<h2 id="read">How to read this site</h2>')
    b.append(table(["Page", "What it contains", "Course section"], [
        ['<a href="requirements.html">Requirements</a>', "Users, constraints and every requirement with how it is verified.", "Requirements summary"],
        ['<a href="design.html">Design</a>', "Diagrams, component pages and interfaces.", "High-level design"],
        ['<a href="integration.html">Fusion</a>', "How sensor fusion works on this vehicle and where CSTI connects.", "High-level design"],
        ['<a href="traceability.html">Traceability</a>', "Requirements mapped to components, both ways.", "High-level design"],
        ['<a href="rationale.html">Rationale</a>', "The key design decisions and why.", "Design rationale"],
        ['<a href="evolution.html">Evolution</a>', "How the design absorbs likely changes.", "Design rationale"],
        ['<a href="glossary.html">Glossary</a>', "Terms used on this site.", "—"],
    ]))
    b.append('<h2 id="diverge">Where we diverge from existing approaches</h2>')
    b.append("<p>Single-vendor toolchains, co-simulation frameworks and per-stage test scripts each fall short of carrying one test onto a real vehicle. CSTI differs in four ways: the scenario belongs to no tool (D-01), CSTI owns actor motion (D-03), the stack sees one frozen contract (D-06), and vehicle injection never touches real data and leaves safety to the stack (D-07, D-08).</p>")
    b.append('<h2 id="team">Team</h2>')
    b.append(table(["Member", "Area", "Components"],
                   [[m, a, ", ".join(C[cid]["name"] for cid in COMP_IDS if C[cid]["owner"] == m)] for m, a in MEMBERS.items()]))
    page("index.html", "One Scenario, Every Stage",
         "A design for running the same automated-driving test in simulation, on the bench and on a real vehicle with virtual traffic.",
         "\n".join(b), "index.html")


# ===================================================================== consistency
TRACK_REQ = '<p>Each requirement is tracked through the stages with MathWorks tools. Test cases in Simulink Test Manager run RoadRunner scenarios against the Simulink models, one test case or iteration per scenario and variant (<a href="https://www.mathworks.com/help/sltest/ug/create-and-run-a-roadrunner-test-case.html">RoadRunner test cases</a>). Requirements live in Requirements Toolbox, imported from the team\'s Excel sheet (<a href="https://www.mathworks.com/help/slrequirements/ug/import-requirements-from-microsoft-excel.html">Excel import</a>), and each one is linked to the test cases that verify it, so its pass or fail status updates after every run (<a href="https://www.mathworks.com/help/slrequirements/ug/link-requirement-test-items.html">linking tests</a>). Results from HIL and the vehicle, which run outside Simulink, can feed the same status as JUnit or Excel result files (<a href="https://www.mathworks.com/help/slrequirements/ug/include-results-from-external-sources-in-verification-status.html">external results</a>). As scenes are rebuilt from real map data collected on the car, the same test cases rerun on them, so every failure stays tied to a requirement, a scenario and a software version.</p>'


def check_consistency():
    rows = {r["id"]: r for _, groups in (REQPAGE_FUNCTIONAL, REQPAGE_NONFUNCTIONAL, REQPAGE_SAFETY)
            for _, rs in groups for r in rs}
    errs = []
    for k in ("text", "accept", "ver", "prio", "src"):
        errs += [f"{i}: empty {k}" for i, r in rows.items() if not r.get(k)]
    errs += [f"{i}: in REQ but no requirement row" for i in REQ if i not in rows]
    errs += [f"{i}: requirement row but not in REQ" for i in rows if i not in REQ]
    errs += [f"{i}: in TRACE but not in REQ" for i in TRACE if i not in REQ]
    errs += [f"{i}: in REQ but not in TRACE" for i in REQ if not TRACE.get(i)]
    errs += [f"{i}: TRACE names unknown component {c}" for i, cs in TRACE.items() for c in cs if c not in C]
    errs += [f"{d['id']}: cites unknown requirement {r}" for d in DEC for r in d["reqs"] if r not in REQ and not r.startswith("CON-")]
    pv_ids = {p[0] for p in REQPAGE_PV}
    used = set(re.findall(r'href="#(PV-\d+)"', str(rows)))
    errs += [f"{p}: referenced but not defined in PV table" for p in used - pv_ids]
    if errs:
        sys.exit("BUILD FAILED, inconsistent data:\n  " + "\n  ".join(errs))


# ===================================================================== requirements
def build_requirements():
    I2 = "  "
    def wrap(inner):
        return f'{I2}<div class="table-wrap">\n{I2}<table{inner}'

    def simple(headers, rows, row_id=False):
        h = "".join(f"<th>{x}</th>" for x in headers)
        body = []
        for r in rows:
            rid = f' id="{r[0]}"' if row_id else ""
            first = f'<td class="nm">{name_of(r[0]) if row_id else r[1]}</td>' if not row_id or r[0].startswith("CON") else ""
            rest = "".join(f"<td>{c}</td>" for c in (r[1:] if row_id else r[2:]))
            body.append(f"      <tr{rid}>{first}{rest}</tr>")
        return (f'{I2}<div class="table-wrap">\n{I2}<table>\n    <thead><tr>{h}</tr></thead>\n    <tbody>\n'
                + "\n".join(body) + f"\n    </tbody>\n{I2}</table>\n{I2}</div>")

    def reqtable(rows):
        h = "<th>Name</th><th>Requirement</th><th>Acceptance criterion</th><th>Ver.</th><th>Priority</th><th>Source</th>"
        body = []
        for r in rows:
            tag = f'<span class="tag {r["prio"]}">{r["prio"].capitalize()}</span>'
            body.append(f'      <tr id="{r["id"]}"><td class="nm">{REQ[r["id"]]}</td><td>{r["text"]}</td><td>{r["accept"]}</td>'
                        f'<td class="v">{r["ver"]}</td><td class="p">{tag}</td><td>{r["src"]}</td></tr>')
        return (f'{I2}<div class="table-wrap">\n{I2}<table class="req">\n    <thead><tr>{h}</tr></thead>\n    <tbody>\n'
                + "\n".join(body) + f"\n    </tbody>\n{I2}</table>\n{I2}</div>")

    def reqsection(anchor, title, data):
        intro, groups = data
        out = [f'{I2}<h2 id="{anchor}">{title}</h2>']
        if intro:
            out.append(intro)
        for sub, rows in groups:
            if sub:
                out.append(f"\n{I2}<h3>{sub}</h3>")
            out.append(reqtable(rows))
        return "\n".join(out)

    b = []
    b.append(f'{I2}<h2 id="purpose">1. Purpose and scope</h2>\n{REQPAGE_PURPOSE}')
    b.append(f'{I2}<h2 id="stakeholders">2. Customer, users and stakeholders</h2>\n{REQPAGE_CUSTOMER}')
    b.append(simple(["User", "What they need from CSTI"], REQPAGE_STAKEHOLDERS))
    b.append(f'{I2}<h2 id="conventions">3. Conventions</h2>\n{REQPAGE_CONVENTIONS}')
    b.append(f'{I2}<h2 id="constraints">4. Constraints and assumptions</h2>')
    b.append(simple(["Name", "Constraint or assumption"], REQPAGE_CONSTRAINTS, row_id=True))
    b.append(reqsection("functional", "5. Functional requirements", REQPAGE_FUNCTIONAL))
    b.append(reqsection("nonfunctional", "6. Non-functional requirements", REQPAGE_NONFUNCTIONAL))
    b.append(reqsection("safety", "7. Safety requirements", REQPAGE_SAFETY))
    b.append(f'{I2}<h2 id="proposed">8. Proposed values</h2>\n{REQPAGE_PV_INTRO}')
    b.append(simple(["Quantity", "Value", "Basis", "Confirm by"], REQPAGE_PV, row_id=True))
    b.append(REQPAGE_PV_NOTE)
    b.append(f'{I2}<h2 id="coverage">9. Coverage check</h2>\n{REQPAGE_COVERAGE_INTRO}')
    cov = [(f"{t}", r) for t, r in REQPAGE_COVERAGE]
    h = "<th>Topic</th><th>Requirements</th>"
    b.append(f'{I2}<div class="table-wrap">\n{I2}<table>\n    <thead><tr>{h}</tr></thead>\n    <tbody>\n'
             + "\n".join(f"      <tr><td>{t}</td><td>{r}</td></tr>" for t, r in cov) + f"\n    </tbody>\n{I2}</table>\n{I2}</div>")
    b.append(f'{I2}<h2 id="tracking">10. How requirements are tracked</h2>\n{I2}' + TRACK_REQ)
    b.append(f'{I2}<h2 id="open">11. Open issues</h2>\n{I2}<ol>\n' + "\n".join(f"    <li>{x}</li>" for x in REQPAGE_OPEN_ISSUES) + f"\n{I2}</ol>")
    page("requirements.html", "Requirements Summary", REQPAGE_LEDE, "\n\n".join(b), "requirements.html",
         toc=[("purpose", "Purpose and scope"), ("stakeholders", "Customer, users and stakeholders"),
              ("conventions", "Conventions"), ("constraints", "Constraints and assumptions"),
              ("functional", "Functional requirements"), ("nonfunctional", "Non-functional requirements"),
              ("safety", "Safety requirements"), ("proposed", "Proposed values"), ("coverage", "Coverage check"),
              ("tracking", "How requirements are tracked"), ("open", "Open issues")],
         doc_title="Requirements", link=False)


check_consistency()
build_requirements()
build_design()
build_components()
build_trace()
build_rationale()
build_evolution()
build_integration()
build_glossary()
build_index()
print("built ->", SITE)
