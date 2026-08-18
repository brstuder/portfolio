#!/usr/bin/env python3
"""Build architecture diagrams: verify, then emit a self-contained SVG.

    python3 build.py diagrams/src/homelab.svg          # build one
    python3 build.py diagrams/src/*.svg                # build all
    python3 build.py diagrams/src/homelab.svg --check  # verify only, no output

Source SVGs live in diagrams/src/ and reference icons by path. Output SVGs go to
docs/images/diagrams/ with the font and icons embedded as base64, because an SVG
loaded through <img> renders in a restricted mode that blocks every external
resource. Never hand-edit the output.

--check needs only the standard library. Building needs fonttools + brotli
(see requirements-dev.txt).
"""
import argparse
import base64
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

# --------------------------------------------------------------------------
# CONFIG — edit these paths once to match the repository.
# All paths are relative to the repo root (the directory holding mkdocs.yml).
# --------------------------------------------------------------------------
CONFIG = {
    "font_family": "Inter",
    "font_files": {
        "400": "docs/assets/fonts/inter-latin-400-normal.woff2",
        "600": "docs/assets/fonts/inter-latin-600-normal.woff2",
    },
    "output_dir": "docs/images/diagrams",
    "metrics": "font-metrics.json",   # relative to this script
}

NS = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}"

FIT_CEILING = 0.88          # max fraction of available width a label may use
FILL_TARGET = (0.17, 0.25)  # shape area / canvas area (icon variants run denser)
PAD = 14                    # inner padding between a label and the box edge

HERE = os.path.dirname(os.path.abspath(__file__))


def repo_root():
    """Walk up from this script until mkdocs.yml is found."""
    d = HERE
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "mkdocs.yml")):
            return d
        d = os.path.dirname(d)
    sys.exit("could not locate the repo root (no mkdocs.yml found above this script)")


# --------------------------------------------------------------------------
# Text measurement
# --------------------------------------------------------------------------
def load_metrics():
    path = os.path.join(HERE, CONFIG["metrics"])
    if not os.path.exists(path):
        sys.exit(f"missing {path}\nRun: python3 {os.path.join(HERE, 'make_metrics.py')}")
    return json.load(open(path, encoding="utf-8"))


def text_width(s, px, weight, metrics):
    """Advance width of `s` at `px`, from real font metrics.

    Never estimate from character count: the font is proportional and advances
    span roughly 0.28em to 0.99em, so counting characters errs badly.
    """
    m = metrics.get(str(weight)) or metrics["400"]
    return sum(m.get(c, m["__default__"]) for c in s) * px


# --------------------------------------------------------------------------
# Verification
# --------------------------------------------------------------------------
def _boxes(root):
    solid, dashed = [], []
    for e in root.iter(NS + "rect"):
        try:
            box = tuple(float(e.get(k)) for k in ("x", "y", "width", "height"))
        except (TypeError, ValueError):
            continue
        (dashed if e.get("stroke-dasharray") else solid).append(box)
    return solid, dashed


def _overlap(a, b):
    return (min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]) > 0
            and min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]) > 0)


def _in_box(b, x, y):
    return b[0] <= x <= b[0] + b[2] and b[1] <= y <= b[1] + b[3]


def check(path, metrics):
    errs, warns = [], []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return [f"not valid XML: {e}"], [], 0.0

    if not root.tag.startswith(NS):
        errs.append('root element lacks xmlns="http://www.w3.org/2000/svg" '
                    "(a standalone .svg will not render without it)")
    if not root.get("viewBox"):
        return errs + ["root has no viewBox"], warns, 0.0
    if root.get("width") or root.get("height"):
        errs.append("root should carry viewBox only, no width/height, so it scales")
    if root.find(NS + "title") is None:
        errs.append("no <title> element (needed for screen readers)")

    vb = [float(v) for v in root.get("viewBox").split()]
    solid, dashed = _boxes(root)

    icons = []
    for e in root.iter(NS + "image"):
        href = e.get("href") or e.get(XLINK + "href") or ""
        try:
            icons.append((float(e.get("x")), float(e.get("y")),
                          float(e.get("width")), float(e.get("height")), href))
        except (TypeError, ValueError):
            errs.append(f'<image href="{href}"> is missing x/y/width/height')

    for ix, iy, iw, ih, href in icons:
        if href.startswith(("http://", "https://", "//")):
            errs.append(f'icon "{href}" is an external URL; '
                        "<img>-embedded SVG cannot load it. Use a local path.")
        elif not any(_in_box(b, ix, iy) for b in solid):
            warns.append(f'icon "{href}" is not inside any component box')

    def available(box, text_x):
        """Width a label may use, accounting for an icon in the same box."""
        for ix, iy, _, _, _ in icons:
            if _in_box(box, ix, iy):
                return box[0] + box[2] - PAD - text_x
        return box[2]

    lines = {}
    for e in root.iter(NS + "text"):
        if e.get("x") is None or e.get("y") is None:
            continue
        x, y = float(e.get("x")), float(e.get("y"))
        for b in solid:
            if _in_box(b, x, y):
                lines[b] = lines.get(b, 0) + 1
                label = "".join(e.itertext())
                if label.strip():
                    px = float(e.get("font-size", 13))
                    w = text_width(label, px, e.get("font-weight", "400"), metrics)
                    avail = available(b, x)
                    if avail <= 0:
                        errs.append(f'label "{label}" starts outside its box')
                    elif w > avail * FIT_CEILING:
                        errs.append(
                            f'label "{label}" is {w / avail * 100:.0f}% of the '
                            f"{avail:.0f}px available in its box "
                            f"(ceiling {FIT_CEILING * 100:.0f}%) — "
                            "shorten the label or widen the box, never shrink the font")
                break

    for b, n in lines.items():
        if n > 2:
            errs.append(f"box at ({b[0]:.0f},{b[1]:.0f}) has {n} text lines; "
                        "max 2 (title + one sublabel)")

    for i, a in enumerate(solid):
        for b in solid[i + 1:]:
            if _overlap(a, b):
                errs.append(f"components overlap: ({a[0]:.0f},{a[1]:.0f}) "
                            f"and ({b[0]:.0f},{b[1]:.0f})")

    for s in solid + dashed:
        if s[0] < 0 or s[1] < 0 or s[0] + s[2] > vb[2] or s[1] + s[3] > vb[3]:
            errs.append(f"shape at ({s[0]:.0f},{s[1]:.0f}) extends outside the viewBox")

    fill = sum(w * h for _, _, w, h in solid) / (vb[2] * vb[3]) if vb[2] * vb[3] else 0
    if fill < FILL_TARGET[0]:
        warns.append(f"fill {fill * 100:.1f}% is sparse "
                     f"(target {FILL_TARGET[0] * 100:.0f}-{FILL_TARGET[1] * 100:.0f}%); "
                     "enlarge shapes or tighten gaps")
    elif fill > FILL_TARGET[1]:
        warns.append(f"fill {fill * 100:.1f}% is crowded")

    return errs, warns, fill


# --------------------------------------------------------------------------
# Transforms
# --------------------------------------------------------------------------
def namespace_ids(svg, slug):
    """Suffix every id with the diagram slug and rewrite references.

    Not strictly required while diagrams are embedded with <img> (each file is
    an isolated document), but it costs nothing and makes the output safe if
    the diagrams are ever inlined into page HTML, where ids share one DOM.
    """
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    for i in sorted(ids, key=len, reverse=True):
        new = f"{i}-{slug}"
        svg = svg.replace(f'id="{i}"', f'id="{new}"')
        svg = svg.replace(f"url(#{i})", f"url(#{new})")
        svg = svg.replace(f'href="#{i}"', f'href="#{new}"')
    return svg


def embed_icons(svg, base_dir):
    """Inline every local <image href> as a base64 data URI."""
    mimes = {".png": "image/png", ".jpg": "image/jpeg",
             ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}

    def repl(m):
        attr, path = m.group(1), m.group(2)
        if path.startswith(("data:", "#")):
            return m.group(0)
        if path.startswith(("http://", "https://", "//")):
            sys.exit(f"external icon URL not allowed: {path}")
        full = os.path.normpath(os.path.join(base_dir, path))
        if not os.path.exists(full):
            sys.exit(f"icon not found: {full}")
        mime = mimes.get(os.path.splitext(full)[1].lower())
        if not mime:
            sys.exit(f"unsupported icon type: {path}")
        data = base64.b64encode(open(full, "rb").read()).decode()
        return f'{attr}="data:{mime};base64,{data}"'

    return re.sub(r'\b(href|xlink:href)="([^"]+)"', repl, svg)


def used_characters(svg):
    root = ET.fromstring(svg)
    chars = set()
    for e in root.iter(NS + "text"):
        chars.update("".join(e.itertext()))
    return chars


def embed_font(svg, chars, root_dir):
    """Subset the local woff2 to the glyphs this diagram uses, then inline it."""
    try:
        from fontTools import subset  # noqa: F401
        from fontTools.ttLib import TTFont  # noqa: F401
    except ImportError:
        sys.exit("font embedding needs fonttools and brotli:\n"
                 "  pip install -r requirements-dev.txt")

    import io
    from fontTools import subset as fsubset

    text = "".join(sorted(chars))
    rules = []
    for weight, rel in CONFIG["font_files"].items():
        src = os.path.join(root_dir, rel)
        if not os.path.exists(src):
            sys.exit(f"font file not found: {src}\n"
                     "Update CONFIG['font_files'] in build.py to point at the "
                     "woff2 files this site already self-hosts.")
        opts = fsubset.Options()
        opts.flavor = "woff2"
        opts.desubroutinize = True
        opts.layout_features = ["*"]
        font = fsubset.load_font(src, opts)
        subsetter = fsubset.Subsetter(options=opts)
        subsetter.populate(text=text)
        subsetter.subset(font)
        buf = io.BytesIO()
        fsubset.save_font(font, buf, opts)
        font.close()
        b64 = base64.b64encode(buf.getvalue()).decode()
        rules.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%s;"
            "src:url(data:font/woff2;base64,%s) format('woff2');}"
            % (CONFIG["font_family"], weight, b64))

    m = re.search(r"<svg\b[^>]*>", svg)
    if not m:
        sys.exit("could not find the opening <svg> tag")
    return svg[:m.end()] + "\n  <style>" + "".join(rules) + "</style>" + svg[m.end():]


# --------------------------------------------------------------------------
def build_one(src, root_dir, metrics, check_only, out_dir):
    name = os.path.basename(src)
    errs, warns, fill = check(src, metrics)
    print(f"{name}")
    for w in warns:
        print(f"  warning: {w}")
    if errs:
        for e in errs:
            print(f"  ERROR: {e}")
        return False
    print(f"  checks passed (fill {fill * 100:.1f}%)")
    if check_only:
        return True

    slug = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(name)[0].lower()).strip("-")
    svg = open(src, encoding="utf-8").read()
    svg = namespace_ids(svg, slug)
    chars = used_characters(svg)
    svg = embed_icons(svg, os.path.dirname(os.path.abspath(src)))
    svg = embed_font(svg, chars, root_dir)

    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, f"{slug}.svg")
    open(dest, "w", encoding="utf-8").write(svg)
    rel = os.path.relpath(dest, root_dir)
    print(f"  -> {rel}  ({len(svg.encode()) / 1024:.1f} KB, "
          f"{len(chars)} glyphs embedded)")
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("sources", nargs="+", help="source SVG files")
    p.add_argument("--check", action="store_true", help="verify only, write nothing")
    p.add_argument("--out", help="override the output directory")
    a = p.parse_args()

    root_dir = repo_root()
    metrics = load_metrics()
    out_dir = a.out or os.path.join(root_dir, CONFIG["output_dir"])

    files = []
    for s in a.sources:
        files.extend(sorted(glob.glob(s)) or [s])

    ok = True
    for f in files:
        if not os.path.exists(f):
            print(f"{f}\n  ERROR: file not found")
            ok = False
            continue
        ok &= build_one(f, root_dir, metrics, a.check, out_dir)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
