#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Live 主题配色编辑器
-------------------
专门用来编辑 Ableton Live 12 的 .ask 主题文件（纯 XML 颜色表）。

功能：
  * 列出主题目录里的所有 .ask，一键载入
  * 每个色值逐个可改：点色块调系统取色器、或直接输入十六进制
  * 右侧实时预览（仿 Live 界面的 transport / session / arrangement / device）
  * 支持 #RRGGBB 与 #RRGGBBAA（带 alpha 的色值会自动与底色混合显示）
  * 保存 / 另存为 / 直接安装到主题目录
  * 单色还原、全部还原、多步撤销

用法：
    pythonw live_theme_editor.py            正常启动（双击“启动编辑器.cmd”）
    python  live_theme_editor.py --selftest 自检（不开窗口）
"""

import os
import re
import sys
import math
import colorsys
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox

from token_labels import zh_for, bilingual

DEFAULT_THEMES_DIR = r"D:\ablenton\Resources\Themes"


def app_base_dir():
    """打包成 exe 后取 exe 所在目录，源码运行时取脚本目录。"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def _has_ask(path):
    try:
        return any(n.lower().endswith(".ask") for n in os.listdir(path))
    except OSError:
        return False


def _probe_theme_dir(root):
    import glob
    for parts in (("Live*", "Resources", "Themes"), ("Resources", "Themes")):
        for hit in glob.glob(os.path.join(root, *parts)):
            if os.path.isdir(hit) and _has_ask(hit):
                return hit
    return None


def resolve_themes_dir(cli_dir=None):
    """按 命令行 → 环境变量 → 常见安装路径 → exe 同级 Themes 的顺序找主题目录。"""
    if cli_dir and os.path.isdir(cli_dir):
        return cli_dir
    env = os.environ.get("ABLETON_THEMES_DIR", "").strip()
    if env and os.path.isdir(env):
        return env
    if os.path.isdir(DEFAULT_THEMES_DIR) and _has_ask(DEFAULT_THEMES_DIR):
        return DEFAULT_THEMES_DIR
    roots = []
    for drive in "CDEFGHIJKL":
        base = drive + ":\\"
        if not os.path.exists(base):
            continue
        for rel in ("Ableton", "ablenton", "ProgramData\\Ableton",
                    "Program Files\\Ableton", "Program Files (x86)\\Ableton"):
            cand = base + rel
            if os.path.isdir(cand):
                roots.append(cand)
    for r in roots:
        hit = _probe_theme_dir(r)
        if hit:
            return hit
    fallback = os.path.join(app_base_dir(), "Themes")
    try:
        os.makedirs(fallback, exist_ok=True)
    except OSError:
        pass
    return fallback

# ---------- 界面配色（编辑器自身） ----------
UI_BG = "#181818"
UI_PANEL = "#212121"
UI_PANEL2 = "#2a2a2a"
UI_FG = "#d0d0d0"
UI_SUB = "#8b8b8b"
UI_ACCENT = "#ffad56"
UI_INPUT = "#141414"

TOKEN_RE = re.compile(r'<([A-Za-z0-9_]+)\s+Value="([^"]*)"\s*/>')
OPEN_RE = re.compile(r'<([A-Za-z0-9_]+)(?:\s[^>]*)?>')
CLOSE_RE = re.compile(r'</([A-Za-z0-9_]+)>')

# 语义分类：按关键字匹配 token 名称，顺序即显示顺序
CATEGORIES = [
    ("面板与基础", ["Desktop", "SurfaceArea", "SurfaceBackground", "SurfaceHighlight",
                    "SurfaceAreaFocus", "ControlBackground", "ControlForeground",
                    "ControlFillHandle", "ControlContrast", "ControlTextBack",
                    "ControlSelectionFrame", "TextDisabled", "ControlDisabled",
                    "ControlOn", "ControlOff", "ShadowDark", "ShadowLight",
                    "PreferencesTab", "DetailViewBackground", "SelectionFrame",
                    "StandbySelection", "SelectionBackground", "SelectionForeground",
                    "SecondarySelectionForeground", "ViewControl", "ViewCheckControl"]),
    ("Clip 与轨道", ["Clip", "SceneContrast", "BackgroundClip", "MutedAuditionClip",
                     "DeactivatedClip", "LinkedTrackHover", "TakeLane", "ExpressionLane",
                     "FilledDrumRackPad", "DrumRackScroller", "FreezeColor"]),
    ("播放头与状态色", ["Chosen", "LoopColor", "OffGridLoopColor", "ImplicitArm",
                        "Range", "Learn", "BipolReset", "Automation", "Alert",
                        "Progress", "TransportProgress", "SearchIndication"]),
    ("传输与显示", ["Transport", "RetroDisplay", "DisplayBackground", "Scrollbar",
                    "MeterBackground", "Meter", "Maximum", "Minimum", "Decibel",
                    "ThresholdLine", "GainReduction"]),
    ("浏览器与列表", ["Browser", "Tree", "GridLabel"]),
    ("波形与频谱", ["Waveform", "Velocity", "Spectrum", "InputCurve", "OutputCurve",
                    "NoteProbability", "MidiNoteMaxVelocity", "ScaleAwareness",
                    "Warp", "Piano", "KeyZone", "SelectorZone", "MidiEditor", "Grid"]),
    ("旋钮与元件", ["Poti", "Modulation", "Operator", "Gain"]),
    ("其他", []),
]


def categorize(name):
    for title, keys in CATEGORIES:
        for k in keys:
            if name.startswith(k) or k in name:
                return title
    return "其他"


# ---------------- 颜色工具 ----------------
def parse_color(value):
    """把 #RGB / #RRGGBB / #RRGGBBAA 解析成 (r,g,b,a)，失败返回 None。"""
    if not isinstance(value, str):
        return None
    s = value.strip()
    if not s.startswith("#"):
        return None
    h = s[1:]
    try:
        if len(h) == 3:
            r, g, b = (int(c * 2, 16) for c in h)
            return (r, g, b, 255)
        if len(h) == 6:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
        if len(h) == 8:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))
    except ValueError:
        return None
    return None


def to_rgb6(value, fallback="#3a3a3a"):
    c = parse_color(value)
    if not c:
        return fallback
    return "#%02x%02x%02x" % c[:3]


def lum(hex6):
    """粗略感知亮度，用于判断前景/背景是否够对比。"""
    try:
        r, g, b = (int(hex6[i:i + 2], 16) for i in (1, 3, 5))
    except Exception:
        return 128
    return (r * 299 + g * 587 + b * 114) / 1000.0


def blend_over(value, bg_value, fallback="#3a3a3a"):
    """把可能带 alpha 的颜色叠到背景色上，返回 6 位十六进制。"""
    fg = parse_color(value)
    bg = parse_color(bg_value) or (30, 30, 30, 255)
    if not fg:
        return fallback
    a = fg[3] / 255.0
    return "#%02x%02x%02x" % tuple(
        int(round(fg[i] * a + bg[i] * (1 - a))) for i in range(3))


def normalize_hex(text, keep_alpha_from=None):
    """校验并规整用户输入的颜色；返回大写 #RRGGBB(AA) 或 None。"""
    s = (text or "").strip()
    if not s.startswith("#"):
        s = "#" + s
    h = s[1:]
    if re.fullmatch(r"[0-9a-fA-F]{3}", h):
        h = "".join(c * 2 for c in h)
    if re.fullmatch(r"[0-9a-fA-F]{6}", h):
        if keep_alpha_from and len(keep_alpha_from) == 9:
            h = h + keep_alpha_from[7:]
        return "#" + h.upper()
    if re.fullmatch(r"[0-9a-fA-F]{8}", h):
        return "#" + h.upper()
    return None


# ---------------- 主题文档 ----------------
class Token:
    __slots__ = ("name", "value", "line", "section", "original", "zh")

    def __init__(self, name, value, line, section):
        self.name = name
        self.value = value
        self.line = line
        self.section = section
        self.original = value
        self.zh = ""


class ThemeDoc:
    def __init__(self, path):
        self.path = path
        with open(path, "r", encoding="utf-8", newline="") as fh:
            self.raw = fh.read()
        self.lines = self.raw.splitlines(keepends=True)
        self.tokens = []
        self._parse()

    def _parse(self):
        stack = []
        for idx, line in enumerate(self.lines):
            m = TOKEN_RE.search(line)
            if m:
                section = "/".join(stack) if stack else "Theme"
                self.tokens.append(Token(m.group(1), m.group(2), idx, section))
                continue
            om = OPEN_RE.search(line)
            if om:
                tag = om.group(1)
                if tag not in ("Ableton", "Theme", "xml"):
                    stack.append(tag)
                continue
            cm = CLOSE_RE.search(line)
            if cm and stack:
                stack.pop()

    def get(self, name, section=None, default=None):
        for t in self.tokens:
            if t.name == name and (section is None or t.section.endswith(section)):
                return t.value
        return default

    def by_category(self):
        order = [c[0] for c in CATEGORIES]
        buckets = {c[0]: [] for c in CATEGORIES}
        for t in self.tokens:
            buckets[categorize(t.name)].append(t)
        out = []
        for title in order:
            if buckets[title]:
                out.append((title, buckets[title]))
        return out

    def save(self, path):
        lines = list(self.lines)
        for t in self.tokens:
            # 每个 token 独占一行，只替换该行的 Value 属性，其余格式原样保留
            lines[t.line] = re.sub(r'Value="[^"]*"', 'Value="%s"' % t.value, lines[t.line], count=1)
        text = "".join(lines)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        return text

    def reset_all(self):
        for t in self.tokens:
            t.value = t.original


# ---------------- 主界面 ----------------
class App:
    def __init__(self, root, themes_dir=None):
        self.root = root
        self.doc = None
        self._rows = []
        self.undo_stack = []
        self.filter_text = ""
        self.themes_dir = themes_dir or resolve_themes_dir()

        root.title("Live 主题配色编辑器 · Ableton Live 12 (.ask)")
        root.configure(bg=UI_BG)
        root.geometry("1380x880")
        root.minsize(1140, 720)

        self._build_topbar()
        body = tk.Frame(root, bg=UI_BG)
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)
        body.grid_columnconfigure(2, weight=0)
        body.grid_rowconfigure(0, weight=1)

        self._build_theme_list(body)
        self._build_editor(body)
        self._build_preview(body)

        self._bind_keys()
        self._autoload()

    # ---------- 顶部工具栏 ----------
    def _build_topbar(self):
        bar = tk.Frame(self.root, bg=UI_PANEL)
        bar.pack(fill="x", padx=10, pady=10)

        tk.Label(bar, text="主题名称", bg=UI_PANEL, fg=UI_SUB,
                 font=("Microsoft YaHei UI", 9)).pack(side="left", padx=(12, 6))
        self.name_var = tk.StringVar(value="My Theme")
        tk.Entry(bar, textvariable=self.name_var, width=22, bg=UI_INPUT, fg=UI_FG,
                 insertbackground=UI_FG, relief="flat",
                 font=("Consolas", 11)).pack(side="left", ipady=4, padx=(0, 14))

        def btn(text, cmd, accent=False):
            b = tk.Button(bar, text=text, command=cmd,
                          bg=UI_ACCENT if accent else UI_PANEL2,
                          fg="#101010" if accent else UI_FG, relief="flat", bd=0,
                          activebackground="#ffc377" if accent else "#343434",
                          activeforeground="#101010" if accent else UI_FG,
                          font=("Microsoft YaHei UI", 9), padx=12, pady=5, cursor="hand2")
            b.pack(side="left", padx=4)

        btn("安装到主题目录", self.install_theme, accent=True)
        btn("另存为…", self.save_as)
        btn("配色方案…", self.scheme_dialog)
        btn("撤销", self.undo)
        btn("全部还原", self.reset_all)

        self.status = tk.Label(bar, text="", bg=UI_PANEL, fg=UI_SUB,
                               font=("Microsoft YaHei UI", 9))
        self.status.pack(side="right", padx=14)

    # ---------- 左：主题列表 ----------
    def _build_theme_list(self, parent):
        col = tk.Frame(parent, bg=UI_PANEL, width=238)
        col.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        col.grid_propagate(False)

        tk.Label(col, text="主题目录", bg=UI_PANEL, fg=UI_ACCENT,
                 font=("Microsoft YaHei UI", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 2))
        self.dir_label = tk.Label(col, text=self.themes_dir, bg=UI_PANEL, fg=UI_SUB,
                                  wraplength=210, justify="left",
                                  font=("Consolas", 8))
        self.dir_label.pack(fill="x", padx=12)

        holder = tk.Frame(col, bg=UI_PANEL)
        holder.pack(fill="both", expand=True, padx=12, pady=8)
        sb = tk.Scrollbar(holder, bg=UI_PANEL, troughcolor=UI_PANEL2, relief="flat")
        sb.pack(side="right", fill="y")
        self.theme_list = tk.Listbox(holder, bg=UI_INPUT, fg=UI_FG, selectbackground=UI_ACCENT,
                                     selectforeground="#101010", relief="flat", bd=0,
                                     highlightthickness=0, font=("Microsoft YaHei UI", 9),
                                     yscrollcommand=sb.set, activestyle="none")
        self.theme_list.pack(side="left", fill="both", expand=True)
        sb.config(command=self.theme_list.yview)
        self.theme_list.bind("<<ListboxSelect>>", self._on_pick_theme)

        btns = tk.Frame(col, bg=UI_PANEL)
        btns.pack(fill="x", padx=12, pady=(0, 12))
        for text, cmd in (("刷新列表", self.refresh_themes),
                          ("换主题目录…", self.change_themes_dir),
                          ("打开 .ask 文件…", self.open_file)):
            tk.Button(btns, text=text, command=cmd, bg=UI_PANEL2, fg=UI_FG, relief="flat",
                      bd=0, activebackground="#343434", font=("Microsoft YaHei UI", 9),
                      pady=5, cursor="hand2").pack(fill="x", pady=3)

        self.refresh_themes()

    def refresh_themes(self):
        self.theme_list.delete(0, "end")
        self._theme_files = []
        try:
            names = sorted(n for n in os.listdir(self.themes_dir) if n.lower().endswith(".ask"))
        except OSError:
            names = []
        for n in names:
            self._theme_files.append(os.path.join(self.themes_dir, n))
            self.theme_list.insert("end", "  " + n[:-4])

    def _on_pick_theme(self, _evt=None):
        sel = self.theme_list.curselection()
        if sel and sel[0] < len(self._theme_files):
            self.load(self._theme_files[sel[0]])

    def open_file(self):
        p = filedialog.askopenfilename(title="选择 .ask 主题文件", initialdir=self.themes_dir,
                                       filetypes=[("Ableton 主题", "*.ask"), ("所有文件", "*.*")])
        if p:
            self.load(p)

    def change_themes_dir(self):
        p = filedialog.askdirectory(title="选择包含 .ask 文件的主题目录",
                                    initialdir=self.themes_dir)
        if p:
            self.themes_dir = p
            self.dir_label.config(text=p)
            self.refresh_themes()

    def _autoload(self):
        for p in getattr(self, "_theme_files", []):
            if os.path.basename(p).startswith("Default Dark Neutral Medium"):
                self.load(p)
                return
        if getattr(self, "_theme_files", None):
            self.load(self._theme_files[0])

    # ---------- 中：色值列表 ----------
    def _build_editor(self, parent):
        col = tk.Frame(parent, bg=UI_PANEL)
        col.grid(row=0, column=1, sticky="nsew")
        col.grid_rowconfigure(2, weight=1)
        col.grid_columnconfigure(0, weight=1)

        head = tk.Frame(col, bg=UI_PANEL)
        head.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        self.file_label = tk.Label(head, text="未载入主题", bg=UI_PANEL, fg=UI_FG,
                                   font=("Microsoft YaHei UI", 10, "bold"))
        self.file_label.pack(side="left")
        self.count_label = tk.Label(head, text="", bg=UI_PANEL, fg=UI_SUB,
                                    font=("Microsoft YaHei UI", 9))
        self.count_label.pack(side="right")

        search_bar = tk.Frame(col, bg=UI_PANEL)
        search_bar.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        tk.Label(search_bar, text="搜索", bg=UI_PANEL, fg=UI_SUB,
                 font=("Microsoft YaHei UI", 9)).pack(side="left", padx=(0, 6))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._apply_filter())
        tk.Entry(search_bar, textvariable=self.search_var, bg=UI_INPUT, fg=UI_FG,
                 insertbackground=UI_FG, relief="flat", font=("Consolas", 10),
                 width=30).pack(side="left", ipady=4)
        tk.Label(search_bar, text="中英双语 · 可搜中文或英文 · 点色块调取色器",
                 bg=UI_PANEL, fg=UI_SUB, font=("Microsoft YaHei UI", 8)).pack(side="right")

        wrap = tk.Frame(col, bg=UI_PANEL)
        wrap.grid(row=2, column=0, sticky="nsew", padx=(12, 0), pady=(0, 12))
        wrap.grid_rowconfigure(0, weight=1)
        wrap.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(wrap, bg=UI_PANEL, highlightthickness=0, bd=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        vsb = tk.Scrollbar(wrap, orient="vertical", command=self.canvas.yview,
                           bg=UI_PANEL, troughcolor=UI_PANEL2, relief="flat")
        vsb.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=vsb.set)

        self.inner = tk.Frame(self.canvas, bg=UI_PANEL)
        self._inner_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind("<MouseWheel>", self._on_wheel)
        self.inner.bind("<MouseWheel>", self._on_wheel)

    def _on_canvas_resize(self, evt):
        self.canvas.itemconfig(self._inner_id, width=evt.width)

    def _on_wheel(self, evt):
        self.canvas.yview_scroll(int(-1 * (evt.delta / 120)), "units")
        return "break"

    def _apply_filter(self):
        self.filter_text = self.search_var.get().strip().lower()
        visible = 0
        for item in self._rows:
            token, frame, header = item[0], item[1], item[2]
            if header is not None:
                if self.filter_text:
                    header.grid_remove()
                else:
                    header.grid()
                continue
            ok = (not self.filter_text) or (self.filter_text in token.name.lower()
                                            or self.filter_text in token.section.lower()
                                            or self.filter_text in getattr(token, "zh", ""))
            if ok:
                frame.grid()
                visible += 1
            else:
                frame.grid_remove()
        if self.doc:
            self.count_label.config(text="%d / %d 色值" % (visible, len(self.doc.tokens)))

    def load(self, path):
        try:
            doc = ThemeDoc(path)
        except Exception as exc:
            messagebox.showerror("载入失败", "%s\n\n%s" % (path, exc))
            return
        if not doc.tokens:
            messagebox.showerror("载入失败", "这个文件里没有找到色值：\n" + path)
            return
        self.doc = doc
        self.undo_stack.clear()
        self.name_var.set(os.path.basename(path)[:-4] + " 自定义")
        self.file_label.config(text=os.path.basename(path))
        self.status.config(text="已载入 %d 个色值" % len(doc.tokens))
        self._build_rows()
        self._apply_filter()
        self.redraw_preview()

    def _build_rows(self):
        for child in self.inner.winfo_children():
            child.destroy()
        self._rows = []
        self.inner.grid_columnconfigure(0, weight=1)
        r = 0
        for title, tokens in self.doc.by_category():
            header = tk.Frame(self.inner, bg=UI_PANEL2)
            header.grid(row=r, column=0, sticky="ew", pady=(8 if r else 2, 2))
            tk.Label(header, text=title, bg=UI_PANEL2, fg=UI_ACCENT,
                     font=("Microsoft YaHei UI", 9, "bold"), anchor="w").pack(
                         fill="x", padx=8, pady=3)
            self._rows.append((None, header, header, None, None))
            r += 1
            for t in tokens:
                frame = tk.Frame(self.inner, bg=UI_PANEL)
                frame.grid(row=r, column=0, sticky="ew", pady=1)
                frame.grid_columnconfigure(1, weight=1)

                sw = tk.Button(frame, bg=to_rgb6(t.value), relief="flat", bd=0, width=3,
                               activebackground="#ffffff", cursor="hand2",
                               command=lambda tok=t: self.pick_color(tok))
                sw.grid(row=0, column=0, rowspan=2, padx=(8, 8), pady=2, ipady=5)

                zh = zh_for(t.name, t.section)
                t.zh = zh
                tk.Label(frame, text=zh or t.name, bg=UI_PANEL, fg=UI_FG, anchor="w",
                         font=("Microsoft YaHei UI", 10, "bold")).grid(
                             row=0, column=1, sticky="w")
                sub = t.name
                if t.section not in ("Theme", ""):
                    sub += "   ·   " + t.section
                tk.Label(frame, text=sub, bg=UI_PANEL, fg=UI_SUB, anchor="w",
                         font=("Consolas", 8)).grid(row=1, column=1, sticky="w")

                ent = tk.Entry(frame, width=11, bg=UI_INPUT, fg=UI_FG, insertbackground=UI_FG,
                               relief="flat", font=("Consolas", 10), justify="center")
                ent.insert(0, t.value)
                ent.grid(row=0, column=2, rowspan=2, padx=(8, 6), ipady=3)
                ent.bind("<Return>", lambda e, tok=t, en=ent: self.commit_entry(tok, en))
                ent.bind("<FocusOut>",
                         lambda e, tok=t, en=ent: self.commit_entry(tok, en, quiet=True))

                tk.Button(frame, text="↺", bg=UI_PANEL, fg=UI_SUB, relief="flat", bd=0,
                          activebackground=UI_PANEL2, cursor="hand2",
                          command=lambda tok=t, en=ent: self.reset_one(tok, en)
                          ).grid(row=0, column=3, padx=(0, 10))

                self._rows.append((t, frame, None, sw, ent))
                r += 1

    # ---------- 色值修改 ----------
    def pick_color(self, token):
        rgb, hexval = colorchooser.askcolor(color=to_rgb6(token.value),
                                            title="选择颜色 · " + bilingual(token.name, token.section), parent=self.root)
        if hexval:
            self._set(token, normalize_hex(hexval, keep_alpha_from=token.value))

    def commit_entry(self, token, entry, quiet=False):
        new = normalize_hex(entry.get(), keep_alpha_from=token.value)
        if new is None:
            if not quiet:
                messagebox.showwarning("格式不对", "请输入 #RRGGBB 或 #RRGGBBAA，例如 #1E90FF")
            entry.configure(bg="#4a1c1c")
            self.root.after(600, lambda: entry.configure(bg=UI_INPUT))
            return
        if new != token.value:
            self._set(token, new)
        entry.configure(bg=UI_INPUT)
        entry.delete(0, "end")
        entry.insert(0, new)

    def _refresh_row(self, token):
        for item in self._rows:
            if item[0] is token:
                item[3].configure(bg=to_rgb6(token.value))
                item[4].delete(0, "end")
                item[4].insert(0, token.value)
                break

    def _set(self, token, value, record=True):
        if record:
            self.undo_stack.append((token, token.value))
        token.value = value
        self._refresh_row(token)
        self.status.config(text="已修改 %s → %s" % (bilingual(token.name, token.section), value))
        self.redraw_preview()

    def reset_one(self, token, entry):
        self._set(token, token.original)

    def reset_all(self):
        if not self.doc:
            return
        for item in self._rows:
            if item[0] is not None:
                self._set(item[0], item[0].original, record=False)
        self.undo_stack.clear()
        self.status.config(text="已全部还原为原文件数值")

    def undo(self):
        if not self.undo_stack:
            self.status.config(text="没有可撤销的修改")
            return
        last = self.undo_stack.pop()
        if isinstance(last, tuple) and len(last) == 2 and last[0] == "bulk":
            for token, old in last[1]:
                token.value = old
                self._refresh_row(token)
            self.status.config(text="已撤销一次整体调色（%d 个色值）" % len(last[1]))
        else:
            token, old = last
            token.value = old
            self._refresh_row(token)
            self.status.config(text="已撤销 %s → %s" % (bilingual(token.name, token.section), old))
        self.redraw_preview()

    # ---------- 配色方案（整体调色） ----------
    def apply_scheme(self, hue_deg, sat_scale, light_scale):
        """整主题调色：彩色整体转色相/加饱和/调亮暗，灰色保持原样。"""
        if not self.doc:
            return 0
        bulk = []
        for item in self._rows:
            token = item[0]
            if token is None:
                continue
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
                bulk.append((token, token.value))
                token.value = new
                self._refresh_row(token)
        if bulk:
            self.undo_stack.append(("bulk", bulk))
            self.redraw_preview()
            self.status.config(text="已整体调色 %d 个色值（Ctrl+Z 可撤销）" % len(bulk))
        else:
            self.status.config(text="当前主题没有可调的彩色，或参数无变化")
        return len(bulk)

    def scheme_dialog(self):
        if not self.doc:
            messagebox.showinfo("先载入主题", "请先在左侧选一个 .ask 主题。")
            return
        dlg = tk.Toplevel(self.root)
        dlg.title("配色方案 · 整体调色")
        dlg.configure(bg=UI_PANEL)
        dlg.geometry("460x352")
        dlg.transient(self.root)
        dlg.resizable(False, False)

        tk.Label(dlg, text="整体调色只作用于彩色，灰色（背景/文字/面板层次）保持原样",
                 bg=UI_PANEL, fg=UI_SUB, font=("Microsoft YaHei UI", 9),
                 wraplength=420, justify="left").pack(anchor="w", padx=16, pady=(14, 8))

        hue_var = tk.DoubleVar(value=0.0)
        sat_var = tk.DoubleVar(value=1.0)
        lit_var = tk.DoubleVar(value=1.0)

        style = ttk.Style(dlg)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TScale", background=UI_PANEL, troughcolor=UI_INPUT,
                        bordercolor=UI_PANEL, lightcolor=UI_ACCENT, darkcolor=UI_ACCENT)

        def slider(label, var, frm, to, fmt):
            row = tk.Frame(dlg, bg=UI_PANEL)
            row.pack(fill="x", padx=16, pady=5)
            tk.Label(row, text=label, bg=UI_PANEL, fg=UI_FG, width=8, anchor="w",
                     font=("Microsoft YaHei UI", 9)).pack(side="left")
            val = tk.Label(row, text=fmt % var.get(), bg=UI_PANEL, fg=UI_ACCENT, width=7,
                           anchor="e", font=("Consolas", 9))
            val.pack(side="right")
            sc = ttk.Scale(row, from_=frm, to=to, variable=var, orient="horizontal",
                           command=lambda _v, var=var, val=val, fmt=fmt:
                           val.config(text=fmt % var.get()))
            sc.pack(side="left", fill="x", expand=True, padx=8)
            label_refs.append((var, val, fmt))

        label_refs = []
        slider("色相偏移", hue_var, -180, 180, "%+.0f")
        slider("饱和度", sat_var, 0.3, 1.8, "%.2f")
        slider("亮度", lit_var, 0.7, 1.3, "%.2f")

        tk.Label(dlg, text="快捷预设（相对当前主题再偏一次）", bg=UI_PANEL, fg=UI_SUB,
                 font=("Microsoft YaHei UI", 8)).pack(anchor="w", padx=16, pady=(10, 2))
        presets = tk.Frame(dlg, bg=UI_PANEL)
        presets.pack(fill="x", padx=16)
        preset_defs = (("冷蓝", -14, 1.10, 1.0), ("森绿", 95, 1.15, 1.0),
                       ("酒红", -135, 1.20, 0.98), ("紫罗兰", 70, 1.25, 1.02),
                       ("落日橙", -25, 1.30, 1.05), ("灰调", 0, 0.35, 1.0))

        for name, hv, sv, lv in preset_defs:
            def pick(_=None, hv=hv, sv=sv, lv=lv):
                hue_var.set(hv)
                sat_var.set(sv)
                lit_var.set(lv)
                for var, lab, fmt in label_refs:
                    lab.config(text=fmt % var.get())
                for w in presets.winfo_children():
                    w.configure(bg=UI_PANEL2)
            tk.Button(presets, text=name, command=pick, bg=UI_PANEL2, fg=UI_FG,
                      relief="flat", bd=0, activebackground="#343434",
                      font=("Microsoft YaHei UI", 8), padx=8, pady=4,
                      cursor="hand2").pack(side="left", padx=3)

        btns = tk.Frame(dlg, bg=UI_PANEL)
        btns.pack(fill="x", padx=16, pady=16)
        tk.Button(btns, text="应用", bg=UI_ACCENT, fg="#101010", relief="flat", bd=0,
                  font=("Microsoft YaHei UI", 9, "bold"), padx=18, pady=6, cursor="hand2",
                  command=lambda: self.apply_scheme(hue_var.get(), sat_var.get(),
                                                    lit_var.get())).pack(side="left", padx=3)
        tk.Button(btns, text="撤销一次", bg=UI_PANEL2, fg=UI_FG, relief="flat", bd=0,
                  font=("Microsoft YaHei UI", 9), padx=12, pady=6, cursor="hand2",
                  command=self.undo).pack(side="left", padx=3)
        tk.Button(btns, text="关闭", bg=UI_PANEL2, fg=UI_FG, relief="flat", bd=0,
                  font=("Microsoft YaHei UI", 9), padx=12, pady=6, cursor="hand2",
                  command=dlg.destroy).pack(side="right", padx=3)

    # ---------- 保存 ----------
    def _current_name(self):
        n = self.name_var.get().strip() or "My Theme"
        for ch in '\\/:*?"<>|':
            n = n.replace(ch, "_")
        return n + ".ask"

    def save_as(self):
        if not self.doc:
            return
        p = filedialog.asksaveasfilename(title="另存为 .ask", initialdir=self.themes_dir,
                                         initialfile=self._current_name(),
                                         defaultextension=".ask",
                                         filetypes=[("Ableton 主题", "*.ask")])
        if not p:
            return
        try:
            self.doc.save(p)
        except Exception as exc:
            messagebox.showerror("保存失败", str(exc))
            return
        self.status.config(text="已保存到 %s" % p)

    def install_theme(self):
        if not self.doc:
            return
        name = self._current_name()
        target = os.path.join(self.themes_dir, name)
        if not os.path.isdir(self.themes_dir):
            messagebox.showerror("找不到主题目录", self.themes_dir)
            return
        if os.path.exists(target) and not messagebox.askyesno("同名主题已存在", "覆盖 %s ？" % name):
            return
        try:
            self.doc.save(target)
        except Exception as exc:
            messagebox.showerror("写入失败", str(exc))
            return
        self.refresh_themes()
        messagebox.showinfo("已安装",
                            "已写入：\n%s\n\n关掉 Live 再重新打开，在 设置 → Look and Feel → Theme 里就能选到它。"
                            % target)
        self.status.config(text="已安装 %s" % name)

    # ---------- 右：实时预览 ----------
    def _build_preview(self, parent):
        col = tk.Frame(parent, bg=UI_PANEL, width=480)
        col.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        col.grid_propagate(False)
        tk.Label(col, text="实时预览（仿 Live 布局）", bg=UI_PANEL, fg=UI_ACCENT,
                 font=("Microsoft YaHei UI", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 6))
        self.preview = tk.Canvas(col, bg="#101010", width=450, height=720,
                                 highlightthickness=0, bd=0)
        self.preview.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.preview.bind("<Configure>", lambda e: self.redraw_preview())

    def _vu(self, seg_name, default="#5d9e5d"):
        if not self.doc:
            return default
        val = self.doc.get(seg_name, section="StandardVuMeter")
        return to_rgb6(val, default) if val else default

    def redraw_preview(self):
        if not self.doc:
            return
        c = self.preview
        c.delete("all")
        W = int(c.winfo_width()) or 450
        H = int(c.winfo_height()) or 720
        if W < 80:
            W = 450
        d = self.doc

        desktop = to_rgb6(d.get("Desktop", default="#1e1e1e"))
        surface = to_rgb6(d.get("SurfaceArea", default="#242424"))
        fg = to_rgb6(d.get("ControlForeground", default="#b5b5b5"))
        sub = to_rgb6(d.get("TextDisabled", default="#757575"))
        ctrl_bg = to_rgb6(d.get("ControlBackground", default="#1e1e1e"))
        detail_bg = to_rgb6(d.get("DetailViewBackground", default="#3e3e3e"))
        acc = to_rgb6(d.get("ChosenDefault", default="#ffad56"))
        play = to_rgb6(d.get("ChosenPlay", default=acc))
        rec = to_rgb6(d.get("ChosenRecord", default="#ff5559"))
        frame_line = to_rgb6(d.get("ControlContrastFrame", default="#5d5d5d"))

        c.configure(bg=desktop)

        # === 1. 顶栏 transport ===
        top_h = 44
        c.create_rectangle(0, 0, W, top_h, fill=surface, outline="")
        x = 12
        for i in range(5):
            c.create_rectangle(x, 12, x + 20, 32, fill=(play if i == 2 else ctrl_bg),
                               outline=frame_line)
            x += 26
        c.create_oval(W - 100, 13, W - 82, 31, fill=rec, outline="")
        lcd_bg = to_rgb6(d.get("RetroDisplayBackground", default="#141414"))
        lcd_fg = to_rgb6(d.get("RetroDisplayForeground", default="#9adcff"))
        c.create_rectangle(W - 74, 10, W - 14, 34, fill=lcd_bg, outline="")
        c.create_text(W - 44, 22, text="120.0", fill=lcd_fg, font=("Consolas", 9, "bold"))
        c.create_text(160, 22, text="TRANSPORT", fill=sub, font=("Microsoft YaHei UI", 8))

        # === 2. 左侧浏览器 ===
        brow_w = 112
        brow_bg = to_rgb6(d.get("BrowserBar", default=surface))
        c.create_rectangle(0, top_h, brow_w, H, fill=brow_bg, outline="")
        tag_bg = to_rgb6(d.get("BrowserTagBackground", default="#3a3a3a"))
        c.create_text(10, top_h + 12, text="BROWSER", fill=sub, anchor="w",
                      font=("Microsoft YaHei UI", 8, "bold"))
        yy = top_h + 30
        for label in ("Sounds", "Drums", "Audio Effects", "MIDI", "Packs", "User"):
            c.create_rectangle(8, yy, brow_w - 10, yy + 15, fill=tag_bg, outline="")
            c.create_text(13, yy + 8, text=label, fill=fg, anchor="w",
                          font=("Microsoft YaHei UI", 7))
            yy += 19
        yy += 6
        cat_bg = to_rgb6(d.get("TreeRowCategoryBackground", default=brow_bg))
        for i in range(9):
            c.create_rectangle(10, yy, brow_w - 12, yy + 9, fill=cat_bg, outline="")
            c.create_text(14, yy + 5, text="Folder %d" % (i + 1), fill=sub, anchor="w",
                          font=("Microsoft YaHei UI", 7))
            yy += 14

        # === 3. Session 网格 ===
        gx0, gy0 = brow_w + 8, top_h + 8
        gx1 = W - 8
        tracks, scenes = 4, 4
        head_h, cell_h, scene_col = 20, 30, 24
        cw = (gx1 - gx0 - scene_col) // tracks
        c.create_text(gx0, gy0 - 2, text="SESSION", fill=sub, anchor="sw",
                      font=("Microsoft YaHei UI", 8, "bold"))
        for t in range(tracks):
            x0 = gx0 + scene_col + t * cw
            c.create_rectangle(x0, gy0, x0 + cw, gy0 + head_h, fill=surface, outline=frame_line)
            c.create_text(x0 + cw / 2, gy0 + head_h / 2, text="Track %d" % (t + 1),
                          fill=fg, font=("Microsoft YaHei UI", 7))
        sel_bg = to_rgb6(d.get("SelectionBackground", default=acc))
        clip_border = to_rgb6(d.get("ClipBorder", default="#000000"))
        clip_text = to_rgb6(d.get("ClipText", default="#ffffff"))
        scene_fg = to_rgb6(d.get("SceneContrast", default=surface))
        for s in range(scenes):
            y0 = gy0 + head_h + 4 + s * (cell_h + 4)
            c.create_rectangle(gx0, y0, gx0 + scene_col - 4, y0 + cell_h,
                               fill=scene_fg, outline="")
            c.create_text(gx0 + (scene_col - 4) / 2, y0 + cell_h / 2, text=str(s + 1),
                          fill=fg, font=("Consolas", 8))
            for t in range(tracks):
                if s == 2 and t == 1:
                    continue
                cidx = (t * scenes + s) % 16 + 1
                fill = to_rgb6(d.get("Clip%d" % cidx, default="#4a6b8a"))
                x0 = gx0 + scene_col + t * cw
                c.create_rectangle(x0 + 2, y0 + 2, x0 + cw - 2, y0 + cell_h - 2,
                                   fill=fill, outline=clip_border)
                c.create_text(x0 + 7, y0 + 9, text="Clip", fill=clip_text, anchor="w",
                              font=("Microsoft YaHei UI", 7, "bold"))
                c.create_line(x0 + 4, y0 + cell_h - 8, x0 + cw - 4, y0 + cell_h - 8,
                              fill=clip_border)
        sx0 = gx0 + scene_col + cw + 1
        sy0 = gy0 + head_h + 4 + 2 * (cell_h + 4) + 1
        c.create_rectangle(sx0, sy0, sx0 + cw - 3, sy0 + cell_h - 3,
                           outline=sel_bg, width=2)

        # === 4. Arrangement 区 ===
        ay0 = gy0 + head_h + 4 + scenes * (cell_h + 4) + 14
        ay1 = min(ay0 + 176, H - 236)
        arr_bg = to_rgb6(d.get("ArrangerGridTiles", default=surface))
        c.create_rectangle(brow_w + 8, ay0, W - 8, ay1, fill=arr_bg, outline="")
        c.create_text(brow_w + 14, ay0 + 8, text="ARRANGEMENT", fill=sub, anchor="w",
                      font=("Microsoft YaHei UI", 8, "bold"))
        grid = to_rgb6(d.get("GridLineBase", default="#3a3a3a"))
        rule = to_rgb6(d.get("ArrangementRulerMarkings", default=sub))
        for gx in range(int(brow_w + 30), int(W - 10), 26):
            c.create_line(gx, ay0 + 18, gx, ay1 - 8, fill=grid)
        for gx in range(int(brow_w + 30), int(W - 10), 52):
            c.create_line(gx, ay0 + 14, gx, ay0 + 19, fill=rule)
        disp_bg = to_rgb6(d.get("DisplayBackground", default="#141414"))
        wave = to_rgb6(d.get("WaveformColor", default="#6ea8d8"))
        clip_bg = to_rgb6(d.get("BackgroundClip", default="#3b4a58"))
        clip_frame = to_rgb6(d.get("BackgroundClipFrame", default="#7a8a99"))
        track_h = max(18, (ay1 - ay0 - 44) // 3 - 4)
        for i in range(3):
            cy0 = ay0 + 26 + i * (track_h + 4)
            cx0 = brow_w + 34 + i * 28
            cw2 = W - 34 - cx0 - (54 - i * 18)
            if cw2 < 60:
                continue
            c.create_rectangle(cx0, cy0, cx0 + cw2, cy0 + track_h, fill=clip_bg, outline=clip_frame)
            if abs(lum(wave) - lum(clip_bg)) < 55:
                wave = "#f2f2f2" if lum(clip_bg) < 128 else "#171717"
            mid = cy0 + track_h / 2
            pts = []
            for px in range(int(cx0 + 4), int(cx0 + cw2 - 4), 3):
                amp = (track_h / 2 - 3) * math.sin((px - cx0) / 7.0) * \
                      (0.55 + 0.45 * math.sin(px / 23.0))
                pts += [px, mid + amp]
            if len(pts) >= 4:
                c.create_line(*pts, fill=wave)
        loop = to_rgb6(d.get("LoopColor", default=acc))
        ph = brow_w + 178
        c.create_rectangle(ph - 42, ay0 + 12, ph + 42, ay1 - 4, outline=loop, width=1)
        c.create_text(ph - 38, ay0 + 6, text="loop", fill=loop, anchor="w",
                      font=("Microsoft YaHei UI", 7))
        c.create_line(ph, ay0 + 12, ph, ay1, fill=play, width=2)

        # === 5. 底部 device / 详情 ===
        dy0 = ay1 + 10
        if H - 8 - dy0 > 70:
            c.create_rectangle(brow_w + 8, dy0, W - 8, H - 8, fill=detail_bg, outline="")
            c.create_rectangle(brow_w + 16, dy0 + 8, W - 16, dy0 + 28, fill=ctrl_bg, outline="")
            c.create_text(brow_w + 24, dy0 + 18, text="Operator", fill=fg, anchor="w",
                          font=("Microsoft YaHei UI", 8, "bold"))
            poti = to_rgb6(d.get("Poti", default="#6a6a6a"))
            needle = to_rgb6(d.get("PotiNeedle", default="#e0e0e0"))
            kx, ky = brow_w + 42, dy0 + 52
            for i in range(4):
                c.create_oval(kx - 10, ky - 10, kx + 10, ky + 10, fill=poti, outline="")
                ang = math.radians(-150 + i * 36)
                c.create_line(kx, ky, kx + 9 * math.cos(ang), ky + 9 * math.sin(ang),
                              fill=needle, width=2)
                c.create_text(kx, ky + 19, text="A%d" % (i + 1), fill=sub,
                              font=("Microsoft YaHei UI", 7))
                kx += 40

            # 参数条
            bar_top = dy0 + 88
            for i, label in enumerate(("Coarse", "Fine", "Spread")):
                c.create_text(brow_w + 20, bar_top + i * 18, text=label, fill=sub, anchor="w",
                              font=("Microsoft YaHei UI", 7))
                c.create_rectangle(brow_w + 78, bar_top - 5 + i * 18,
                                   brow_w + 168, bar_top + 5 + i * 18, fill=ctrl_bg, outline="")
                c.create_rectangle(brow_w + 80, bar_top - 3 + i * 18,
                                   brow_w + 118 + i * 14, bar_top + 3 + i * 18,
                                   fill=acc, outline="")

            # 右侧 mixer 通道推子
            mx0 = W - 132
            c.create_text(mx0, dy0 + 16, text="MIXER", fill=sub, anchor="w",
                          font=("Microsoft YaHei UI", 7, "bold"))
            fader_bg = to_rgb6(d.get("MeterBackground", default="#181818"))
            handle = to_rgb6(d.get("ControlFillHandle", default="#5d5d5d"))
            step = (W - 48 - mx0) / 5.0
            for i in range(5):
                cx = mx0 + step * i + 2
                c.create_rectangle(cx, dy0 + 26, cx + 7, H - 46, fill=fader_bg, outline="")
                pos = dy0 + 40 + (i % 4) * 14
                c.create_rectangle(cx - 1, pos, cx + 8, pos + 6, fill=handle, outline="")

            # VU 电平表（用 StandardVuMeter 的分段色）
            mx, my0, my1 = W - 38, dy0 + 26, H - 46
            c.create_rectangle(mx, my0, mx + 12, my1,
                               fill=to_rgb6(d.get("MeterBackground", default="#181818")),
                               outline="")
            seg = ["BelowZeroDecibel2", "BelowZeroDecibel1", "ZeroDecibel",
                   "AboveZeroDecibel", "Maximum"]
            hgt = (my1 - my0) / len(seg)
            for i, name in enumerate(seg):
                y0 = my1 - (i + 1) * hgt
                c.create_rectangle(mx + 2, y0 + hgt * 0.35, mx + 6, y0 + hgt - 1,
                                   fill=self._vu(name), outline="")
        c.create_text(W - 12, H - 12, text="仅为配色示意", fill=sub, anchor="se",
                      font=("Microsoft YaHei UI", 7))

    # ---------- 快捷键 ----------
    def _bind_keys(self):
        self.root.bind("<Control-s>", lambda e: self.install_theme())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<F5>", lambda e: self.refresh_themes())


def selftest():
    """无窗口自检：能建界面、能改值、写出的文件只有被改的那一行不同。"""
    import tempfile
    themes = resolve_themes_dir()
    if not _has_ask(themes):
        themes = tempfile.mkdtemp(prefix="ask_selftest_")
        sample = (
            '<?xml version="1.0" encoding="UTF-8" ?>\n'
            '<Ableton MajorVersion="5" MinorVersion="12.0_12120" '
            'SchemaChangeVersion="21.6" Creator="Live" Revision="12120">\n'
            '\t<Theme>\n'
            '\t\t<PanelBackground Value="#1e1e1e" />\n'
            '\t\t<TextPrimary Value="#c8c8c8" />\n'
            '\t\t<Clip1 Value="#4a6b8a" />\n'
            '\t\t<StandardVuMeter>\n'
            '\t\t\t<Minimum Value="#00ff00" />\n'
            '\t\t</StandardVuMeter>\n'
            '\t</Theme>\n'
            '</Ableton>\n'
        )
        with open(os.path.join(themes, "Selftest.ask"), "w", encoding="utf-8",
                  newline="") as fh:
            fh.write(sample)
    root = tk.Tk()
    root.withdraw()
    app = App(root, themes)
    root.update_idletasks()
    root.update()
    if not app.doc:
        print("FAIL: 没有载入主题")
        return 1
    src = app.doc.path
    with open(src, "r", encoding="utf-8", newline="") as fh:
        before = fh.read()
    app._set(app.doc.tokens[0], "#FF00AA")
    tmp = os.path.join(tempfile.gettempdir(), "_selftest_theme.ask")
    app.doc.save(tmp)
    with open(tmp, "r", encoding="utf-8", newline="") as fh:
        after = fh.read()
    bl, al = before.splitlines(), after.splitlines()
    diff = [(i, b, a) for i, (b, a) in enumerate(zip(bl, al)) if b != a]
    print("tokens:", len(app.doc.tokens), "| rows:", len(app._rows))
    print("diff lines:", len(diff))
    for i, b, a in diff[:3]:
        print("  line", i, b.strip(), "->", a.strip())
    ok = len(diff) == 1 and "#FF00AA" in diff[0][2] and len(bl) == len(al)
    print("SELFTEST:", "OK" if ok else "FAIL")
    root.destroy()
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    themes = None
    argv = sys.argv[1:]
    if "--themes-dir" in argv:
        i = argv.index("--themes-dir")
        if i + 1 < len(argv):
            themes = argv[i + 1]
    root = tk.Tk()
    App(root, themes or resolve_themes_dir())
    root.mainloop()


if __name__ == "__main__":
    main()
