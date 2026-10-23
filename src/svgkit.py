"""Tiny SVG helper for UML-style diagrams. Styling comes from .dg classes in site.css
(inline) or from an embedded style block (standalone img/*.svg)."""
from html import escape as esc

STANDALONE_STYLE = """
svg{--text:#1d2125;--muted:#5b636b;--line:#d9dcdf;--surface:#fff;--bg:#fbfbf9;--code-bg:#f1f2f3;
--accent:#8a1c2b;--accent-soft:#f6e9eb;--accent2:#c25e00;--proposed-bg:#fdeedc;--safety:#8a1c2b;--safety-bg:#fbe9ec;color:#1d2125;background:#fff}
@media (prefers-color-scheme: dark){svg{--text:#e6e8ea;--muted:#a3abb3;--line:#353a40;--surface:#1d2024;--bg:#15171a;
--code-bg:#262a2f;--accent:#e0848f;--accent-soft:#2d1f22;--accent2:#f0a35c;--proposed-bg:#33261a;--safety:#f09aa4;--safety-bg:#33201f;color:#e6e8ea;background:#1d2024}}
.dg text{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;font-size:12px;fill:var(--text)}
.dg .box{fill:var(--surface);stroke:var(--text);stroke-width:1.2}
.dg .sub{fill:var(--bg);stroke:var(--muted);stroke-width:1}
.dg .ext{fill:var(--code-bg);stroke:var(--muted);stroke-width:1.2;stroke-dasharray:5 3}
.dg .sys{fill:var(--accent-soft);stroke:var(--accent);stroke-width:2}
.dg .safe{fill:var(--safety-bg);stroke:var(--safety);stroke-width:1.6}
.dg .frozen{fill:var(--proposed-bg);stroke:var(--accent2);stroke-width:2.4}
.dg .lane{fill:none;stroke:var(--line);stroke-width:1;stroke-dasharray:2 3}
.dg .lanet{font-size:11px;fill:var(--muted);font-weight:600;letter-spacing:.04em;text-transform:uppercase}
.dg .ln{stroke:var(--text);fill:none;stroke-width:1.2}
.dg .ln.dash{stroke-dasharray:5 4}.dg .ln.red{stroke:var(--safety)}.dg .ln.thin{stroke:var(--muted)}
.dg .lbl{font-size:11px;fill:var(--muted)}.dg .lbl-bg{fill:var(--surface)}
.dg .st{font-size:10.5px;fill:var(--muted);font-style:italic}.dg .id{font-weight:700}
.dg .act{fill:var(--accent-soft);stroke:var(--accent);stroke-width:1}
.dg .frag{fill:none;stroke:var(--muted);stroke-width:1}.dg .fragt{fill:var(--code-bg);stroke:var(--muted);stroke-width:1}
.dg .state{fill:var(--surface);stroke:var(--text);stroke-width:1.3}.dg .dot{fill:var(--text)}
"""


class D:
    def __init__(self, key, w, h, title, desc):
        self.key, self.w, self.h, self.title, self.desc = key, w, h, title, desc
        self.p = []

    # primitives -------------------------------------------------------
    def rect(self, x, y, w, h, cls="box", rx=4):
        self.p.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>')

    def text(self, x, y, s, cls=None, anchor="middle"):
        c = f' class="{cls}"' if cls else ""
        self.p.append(f'<text{c} x="{x}" y="{y}" text-anchor="{anchor}">{esc(s)}</text>')

    def lines(self, x, y, lines, cls=None, anchor="middle", lh=14):
        for i, s in enumerate(lines):
            self.text(x, y + i * lh, s, cls, anchor)

    def label(self, x, y, s, anchor="middle", cls="lbl"):
        for i, line in enumerate(s.split("\n")):
            w = len(line) * 5.5 + 8
            bx = x - w / 2 if anchor == "middle" else (x - 4 if anchor == "start" else x - w + 4)
            yy = y + i * 13
            self.p.append(f'<rect class="lbl-bg" x="{bx:.1f}" y="{yy - 10}" width="{w:.1f}" height="13"/>')
            self.text(x, yy, line, cls, anchor)

    def node(self, x, y, w, h, ident=None, name="", stereo="component", cls="box", extra=None):
        self.rect(x, y, w, h, cls)
        rows = []
        if stereo:
            rows.append(("«" + stereo + "»", "st", 12))
        if ident:
            rows.append((ident, "id", 15))
        for n in name.split("\n"):
            if n:
                rows.append((n, None, 15))
        if extra:
            for e in extra.split("\n"):
                rows.append((e, "st", 13))
        total = sum(r[2] for r in rows)
        cy = y + (h - total) / 2 + 11
        for s, c, lh in rows:
            self.text(x + w / 2, cy, s, c)
            cy += lh

    def path(self, pts, cls="ln", arrow="end", label=None, at=None, anchor="middle", head="arr"):
        d = "M" + " L".join(f"{a},{b}" for a, b in pts)
        m = ""
        if arrow in ("end", "both"):
            m += f' marker-end="url(#{self.key}-{head})"'
        if arrow in ("start", "both"):
            m += f' marker-start="url(#{self.key}-{head}s)"'
        self.p.append(f'<path class="{cls}" d="{d}"{m}/>')
        if label:
            if at is None:
                (x1, y1), (x2, y2) = pts[len(pts) // 2 - 1], pts[len(pts) // 2]
                at = ((x1 + x2) / 2, (y1 + y2) / 2 + 4)
            self.label(at[0], at[1], label, anchor)

    def actor(self, x, y, label_lines):
        self.p.append(f'<circle class="box" cx="{x}" cy="{y}" r="9"/>')
        self.p.append(f'<path class="ln" d="M{x},{y+9} L{x},{y+32} M{x-14},{y+17} L{x+14},{y+17} M{x},{y+32} L{x-11},{y+50} M{x},{y+32} L{x+11},{y+50}"/>')
        self.lines(x, y + 66, label_lines)

    def node3d(self, x, y, w, h, title, stereo="device", cls="box"):
        d = 12
        self.p.append(f'<path class="{cls}" d="M{x},{y} L{x+d},{y-d} L{x+w+d},{y-d} L{x+w},{y} Z"/>')
        self.p.append(f'<path class="{cls}" d="M{x+w},{y} L{x+w+d},{y-d} L{x+w+d},{y+h-d} L{x+w},{y+h} Z"/>')
        self.rect(x, y, w, h, cls, rx=0)
        self.text(x + w / 2, y + 18, "«" + stereo + "»", "st")
        self.text(x + w / 2, y + 34, title, "id")

    # output -----------------------------------------------------------
    def defs(self):
        k = self.key
        return (f'<defs>'
                f'<marker id="{k}-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker>'
                f'<marker id="{k}-arrs" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M10,0 L0,5 L10,10 z" fill="currentColor"/></marker>'
                f'<marker id="{k}-open" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10" fill="none" stroke="currentColor" stroke-width="1.4"/></marker>'
                f'<marker id="{k}-opens" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M10,0 L0,5 L10,10" fill="none" stroke="currentColor" stroke-width="1.4"/></marker>'
                f'</defs>')

    def svg(self, standalone=False):
        head = (f'<svg class="dg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'role="img" aria-labelledby="{self.key}-t {self.key}-d">'
                f'<title id="{self.key}-t">{esc(self.title)}</title><desc id="{self.key}-d">{esc(self.desc)}</desc>')
        style = f"<style>{STANDALONE_STYLE}</style>" if standalone else ""
        return head + style + self.defs() + "\n".join(self.p) + "</svg>"


class Seq:
    """UML sequence diagram builder."""

    def __init__(self, key, title, desc, parts, spacing=95, left=70):
        self.parts = parts
        self.x = {p[0]: left + i * spacing for i, p in enumerate(parts)}
        self.w = left * 2 + spacing * (len(parts) - 1)
        self.d = D(key, self.w, 100, title, desc)
        self.y = 104
        self.frags = []

    def m(self, a, b, label, style="sync"):
        xa, xb = self.x[a], self.x[b]
        cls = "ln" + (" dash" if style in ("ret", "async") else "") + (" red" if style == "red" else "")
        head = "open" if style in ("ret", "async") else "arr"
        self.d.path([(xa, self.y), (xb, self.y)], cls, head=head)
        self.d.label((xa + xb) / 2, self.y - 5, label)
        self.y += 32

    def self_(self, a, label, style="sync", left=False):
        x = self.x[a]
        cls = "ln" + (" red" if style == "red" else "")
        k = -1 if left else 1
        self.d.path([(x, self.y - 6), (x + 26 * k, self.y - 6), (x + 26 * k, self.y + 10), (x + 2 * k, self.y + 10)], cls)
        self.d.label(x + 32 * k, self.y + 6, label, anchor="end" if left else "start")
        self.y += 36

    def frag(self, kind, guard, a, b):
        depth = len(self.frags)
        x1, x2 = self.x[a] - 52 + depth * 7, self.x[b] + 52 - depth * 7
        self.frags.append([kind, x1, x2, self.y - 18, []])
        self.d.p.append(f'<path class="fragt" d="M{x1},{self.y-18} L{x1+42},{self.y-18} L{x1+42},{self.y-6} L{x1+36},{self.y} L{x1},{self.y} Z"/>')
        self.d.text(x1 + 20, self.y - 5, kind, "id")
        self.d.label(x1 + 48, self.y - 5, guard, anchor="start")
        self.y += 28

    def else_(self, guard):
        kind, x1, x2, y0, els = self.frags[-1]
        yy = self.y - 14
        self.d.p.append(f'<path class="ln thin dash" d="M{x1},{yy} L{x2},{yy}"/>')
        self.d.label(x1 + 8, yy + 13, guard, anchor="start")
        self.y += 20

    def end(self):
        kind, x1, x2, y0, _ = self.frags.pop()
        self.d.p.insert(0, f'<rect class="frag" x="{x1}" y="{y0}" width="{x2-x1}" height="{self.y - y0 - 10}"/>')
        self.y += 8

    def note(self, a, text):
        self.d.label(self.x[a], self.y, text, anchor="middle")
        self.y += 18 * (text.count("\n") + 1)

    def finish(self):
        h = self.y + 10
        top = []
        for p in self.parts:
            k, lab = p[0], p[1]
            cls = p[2] if len(p) > 2 else "box"
            x = self.x[k]
            top.append(f'<path class="ln thin dash" d="M{x},{70} L{x},{h-8}"/>')
        hdr = D(self.d.key, 0, 0, "", "")
        for p in self.parts:
            k, lab = p[0], p[1]
            cls = p[2] if len(p) > 2 else "box"
            x = self.x[k]
            hdr.rect(x - 44, 20, 88, 48, cls)
            ls = lab.split("\n")
            hdr.lines(x, 40 if len(ls) > 1 else 48, ls, None)
        self.d.p = top + hdr.p + self.d.p
        self.d.h = h
        return self.d
