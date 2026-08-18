#!/usr/bin/env python3
"""Generate font-metrics.json from the woff2 files this site self-hosts.

    python3 make_metrics.py

Run once during setup, and again whenever the font files change. Reads the
paths from CONFIG in build.py, so there is one place to configure them.

The output maps each character to its horizontal advance width as a fraction
of an em, per weight. build.py uses it to measure label widths without needing
fonttools at check time.

Needs fonttools + brotli (see requirements-dev.txt).
"""
import json
import os
import string
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from build import CONFIG, repo_root  # noqa: E402

CHARS = sorted(set(
    string.ascii_letters + string.digits +
    " !\"#$%&'()*+,-./:;<=>?@[]^_{|}~" +
    "\u00b7\u2013\u2014\u2192\u00d7"   # middot, en/em dash, right arrow, times
))


def main():
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        sys.exit("needs fonttools and brotli:\n  pip install -r requirements-dev.txt")

    root = repo_root()
    metrics, missing_report = {}, {}

    for weight, rel in CONFIG["font_files"].items():
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            sys.exit(f"font file not found: {path}\n"
                     "Update CONFIG['font_files'] in build.py first.")
        font = TTFont(path)
        upm = font["head"].unitsPerEm
        hmtx = font["hmtx"]
        cmap = font.getBestCmap()

        table, missing = {}, []
        for c in CHARS:
            g = cmap.get(ord(c))
            if g is None:
                missing.append(c)
                continue
            table[c] = round(hmtx[g][0] / upm, 5)

        if not table:
            sys.exit(f"{rel} contains none of the expected glyphs")
        table["__default__"] = round(sum(table.values()) / len(table), 5)
        metrics[weight] = table
        missing_report[weight] = missing
        font.close()
        print(f"  weight {weight}: {len(table) - 1} glyphs from {rel}")

    out = os.path.join(HERE, CONFIG["metrics"])
    json.dump(metrics, open(out, "w", encoding="utf-8"), separators=(",", ":"))
    print(f"wrote {out}")

    for weight, missing in missing_report.items():
        if missing:
            print(f"\nWARNING: weight {weight} is missing {len(missing)} glyphs: "
                  f"{''.join(missing)}")
            print("  The site's woff2 may already be subset. Labels using these "
                  "characters will fall back to an average width when measured, "
                  "and may not render. Consider a fuller font file for diagrams.")


if __name__ == "__main__":
    main()
