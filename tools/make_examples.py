# -*- coding: utf-8 -*-
"""从 Live 自带主题批量生成示例配色。

用法：
    python tools/make_examples.py <Themes 目录> <输出目录>

只动彩色（饱和度 < 0.06 的灰色跳过），和在界面里点「配色方案…」的预设完全同一套算法。
"""
import colorsys
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from live_theme_editor import ThemeDoc, parse_color  # noqa: E402

# (输出文件名, 基础主题, (色相偏移, 饱和度倍数, 亮度倍数))
EXAMPLES = (
    ("Wine Dark.ask", "Default Dark Neutral Medium.ask", (-135, 1.20, 0.98)),
    ("Forest Light.ask", "Default Light Neutral Medium.ask", (95, 1.15, 1.0)),
    ("Mono Grey.ask", "Default Dark Neutral Medium.ask", (0, 0.35, 1.0)),
)


def apply_scheme(doc, hue_deg, sat_scale, light_scale):
    changed = 0
    for token in doc.tokens:
        col = parse_color(token.value)
        if not col:
            continue
        r, g, b, a = col
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        if s < 0.06:
            continue
        h2 = (h + hue_deg / 360.0) % 1.0
        s2 = max(0.0, min(1.0, s * sat_scale))
        v2 = max(0.0, min(1.0, v * light_scale))
        rr, gg, bb = colorsys.hsv_to_rgb(h2, s2, v2)
        new = "#%02x%02x%02x" % (int(round(rr * 255)), int(round(gg * 255)),
                                 int(round(bb * 255)))
        if a < 255:
            new += "%02x" % a
        if new != token.value:
            token.value = new
            changed += 1
    return changed


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    themes_dir, out_dir = argv[1], argv[2]
    os.makedirs(out_dir, exist_ok=True)
    for name, base, (hv, sv, lv) in EXAMPLES:
        src = os.path.join(themes_dir, base)
        if not os.path.exists(src):
            print("SKIP %s（找不到 %s）" % (name, base))
            continue
        doc = ThemeDoc(src)
        n = apply_scheme(doc, hv, sv, lv)
        doc.save(os.path.join(out_dir, name))
        print("%-18s <- %-32s hue%+5.0f sat %.2f light %.2f : %d/%d 色值"
              % (name, base, hv, sv, lv, n, len(doc.tokens)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
