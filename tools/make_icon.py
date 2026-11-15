# -*- coding: utf-8 -*-
"""生成应用图标（色环 + 深色圆角底），输出 assets/icon.ico 与 assets/icon.png。

用法：python tools/make_icon.py
依赖 Pillow（打包时才需要，运行主程序不需要）。
"""

import colorsys
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(HERE), "assets")
SIZE = 512
SCALE = 4  # 先画大图再缩小，边缘更干净


def hsv(h, s, v):
    return tuple(int(round(c * 255)) for c in colorsys.hsv_to_rgb(h, s, v))


def build():
    n = SIZE * SCALE
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # 深色圆角底
    pad = int(n * 0.06)
    radius = int(n * 0.19)
    d.rounded_rectangle([pad, pad, n - pad - 1, n - pad - 1], radius=radius,
                        fill=(26, 26, 26, 255), outline=(66, 66, 66, 255), width=int(n * 0.008))

    # 色环：8 段
    cx = cy = n / 2
    r_out = n * 0.355
    r_in = n * 0.175
    seg = 8
    for i in range(seg):
        start = -90 + i * (360 / seg)
        end = start + (360 / seg) + 0.6
        color = hsv(i / seg, 0.72, 0.95)
        d.pieslice([cx - r_out, cy - r_out, cx + r_out, cy + r_out], start, end,
                   fill=color + (255,))

    # 挖空中心
    d.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], fill=(26, 26, 26, 255))

    # 中心亮点（当前强调色）
    r_dot = n * 0.062
    d.ellipse([cx - r_dot, cy - r_dot, cx + r_dot, cy + r_dot], fill=(255, 171, 74, 255))

    img = img.resize((SIZE, SIZE), Image.LANCZOS)
    os.makedirs(OUT_DIR, exist_ok=True)
    png = os.path.join(OUT_DIR, "icon.png")
    img.save(png)
    ico = os.path.join(OUT_DIR, "icon.ico")
    img.save(ico, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
                         (128, 128), (256, 256)])
    print("saved:", png)
    print("saved:", ico)


if __name__ == "__main__":
    build()
