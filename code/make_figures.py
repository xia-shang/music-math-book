"""
make_figures.py —— 用纯标准库生成书中插图（SVG）

运行：
    python code/make_figures.py

输出目录：
    docs/public/figures/

为什么不用 matplotlib：插图是矢量、体积小、可版本化，且不引入依赖。
每个 SVG 都带浅色卡片底，浅色/深色主题下都能读。
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import dissonance, ratio_of_cents  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "docs" / "public" / "figures"

TEAL = "#0f766e"
TEAL_SOFT = "#5eead4"
AMBER = "#b45309"
AMBER_SOFT = "#fbbf24"
SLATE = "#475569"
MUTED = "#94a3b8"
INK = "#0f172a"
GRID = "#e2e8f0"
BLUE = "#2563eb"

STYLE = """
text{font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;fill:#334155}
.title{font-size:13px;font-weight:700;fill:#0f172a}
.lbl{font-size:11px}
.tick{font-size:10px;fill:#64748b}
.mono{font-family:Consolas,'Cascadia Code',monospace}
"""


def svg(width: int, height: int, body: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="{title}">'
        f"<style>{STYLE}</style>"
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" '
        f'fill="#fbfcfe" stroke="{GRID}"/>'
        f"{body}</svg>"
    )


def path(points: list[tuple[float, float]]) -> str:
    if not points:
        return ""
    head = f"M{points[0][0]:.2f},{points[0][1]:.2f}"
    rest = " ".join(f"L{x:.2f},{y:.2f}" for x, y in points[1:])
    return f"{head} {rest}"


# ---------------------------------------------------------------- 图 1：方波合成


def fig_harmonics() -> str:
    w, h = 740, 300
    parts = ['<text x="28" y="30" class="title">方波的傅里叶合成：项数越多，越接近理想方波</text>']

    x0, x1 = 34, 356
    y0, y1 = 52, 248
    cy = (y0 + y1) / 2
    n = 260
    t_max = 2.0

    def raw(coeffs: list[float]) -> list[float]:
        return [
            sum(c * math.sin(2 * math.pi * (j + 1) * t_max * i / n) for j, c in enumerate(coeffs))
            for i in range(n + 1)
        ]

    odd9 = [1.0, 0, 1 / 3, 0, 1 / 5, 0, 1 / 7, 0, 1 / 9]
    curves = {
        "fund": raw([1.0] + [0.0] * 8),
        "odd3": raw([1.0, 0, 1 / 3] + [0.0] * 6),
        "odd9": raw(odd9),
    }
    maxabs = max(max(abs(v) for v in c) for c in curves.values()) or 1.0
    # 自动缩放，保证所有曲线都落在面板内
    scale = 0.9 * (y1 - y0) / 2 / maxabs

    def to_pts(vals: list[float]) -> list[tuple[float, float]]:
        return [(x0 + (x1 - x0) * i / n, cy - v * scale) for i, v in enumerate(vals)]

    parts.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#ffffff" stroke="{GRID}"/>')
    parts.append(f'<line x1="{x0}" y1="{cy}" x2="{x1}" y2="{cy}" stroke="{GRID}" stroke-dasharray="4 4"/>')

    ideal = [
        (x0 + (x1 - x0) * i / n, cy - (1 if math.sin(2 * math.pi * t_max * i / n) >= 0 else -1) * 0.9 * (y1 - y0) / 2)
        for i in range(n + 1)
    ]
    parts.append(f'<path d="{path(ideal)}" fill="none" stroke="{AMBER_SOFT}" stroke-width="1.6" stroke-dasharray="5 4"/>')

    parts.append(f'<path d="{path(to_pts(curves["fund"]))}" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')
    parts.append(f'<path d="{path(to_pts(curves["odd3"]))}" fill="none" stroke="{TEAL}" stroke-width="1.5"/>')
    parts.append(f'<path d="{path(to_pts(curves["odd9"]))}" fill="none" stroke="{INK}" stroke-width="1.8"/>')

    parts.append(f'<text x="{x0}" y="{y0 + 14}" class="tick">时域：2 个周期</text>')
    parts.append(f'<text x="{x0}" y="{y1 + 16}" class="tick">虚线 = 理想方波　粗线 = 前 5 个奇次谐波</text>')

    # 右侧频谱
    sx0, sy = 404, 232
    max_bar = 150
    bar_w = 30
    for idx, k in enumerate([1, 3, 5, 7, 9]):
        x = sx0 + idx * 46
        hh = max_bar * (1 / k) / 1.0
        parts.append(
            f'<rect x="{x}" y="{sy - hh}" width="{bar_w}" height="{hh}" rx="3" fill="{TEAL}" opacity="0.85"/>'
        )
        parts.append(f'<text x="{x + bar_w / 2}" y="{sy + 14}" text-anchor="middle" class="tick">{k}</text>')
        parts.append(f'<text x="{x + bar_w / 2}" y="{sy - hh - 5}" text-anchor="middle" class="tick mono">1/{k}</text>')
    parts.append(f'<line x1="{sx0 - 8}" y1="{sy}" x2="{sx0 + 232}" y2="{sy}" stroke="{SLATE}" stroke-width="1"/>')
    parts.append(f'<text x="{sx0 + 240}" y="{sy - 150}" class="tick" text-anchor="end">振幅</text>')
    parts.append(f'<text x="{sx0}" y="30" class="title">频域：只有奇次谐波</text>')
    parts.append(f'<text x="{sx0}" y="{sy + 32}" class="tick">谐波次数 k（振幅 ∝ 1/k）</text>')
    return svg(w, h, "".join(parts), "方波的傅里叶合成")


# ---------------------------------------------------------------- 图 2：音色


def fig_timbre() -> str:
    w, h = 740, 300
    parts = ['<text x="28" y="30" class="title">同一音符的两种音色：差别在谐波的衰减速度</text>']
    x0, y0, pw, ph = 56, 56, 620, 186
    parts.append(f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="#ffffff" stroke="{GRID}"/>')
    for g in range(0, 6):
        y = y0 + ph - ph * g / 5
        parts.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0 + pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        parts.append(f'<text x="{x0 - 8}" y="{y + 3:.1f}" text-anchor="end" class="tick">{g / 5:.1f}</text>')

    piano = [(1 / k) ** 1.4 for k in range(1, 11)]
    violin = [(1 / k) ** 0.75 for k in range(1, 11)]
    pmax = max(piano[0], violin[0])
    bw = 15
    for i in range(10):
        cx = x0 + 34 + i * 60
        hp = ph * piano[i] / pmax
        hv = ph * violin[i] / pmax
        parts.append(f'<rect x="{cx - bw - 2}" y="{y0 + ph - hp:.1f}" width="{bw}" height="{hp:.1f}" rx="2" fill="{BLUE}" opacity="0.85"/>')
        parts.append(f'<rect x="{cx + 2}" y="{y0 + ph - hv:.1f}" width="{bw}" height="{hv:.1f}" rx="2" fill="{AMBER}" opacity="0.85"/>')
        parts.append(f'<text x="{cx}" y="{y0 + ph + 14}" text-anchor="middle" class="tick">{i + 1}</text>')
    parts.append(f'<text x="{x0 + pw / 2}" y="{y0 + ph + 32}" text-anchor="middle" class="tick">谐波次数 k</text>')

    # 图例
    parts.append(f'<rect x="{x0}" y="30" width="10" height="10" fill="{BLUE}"/>')
    parts.append(f'<text x="{x0 + 16}" y="39" class="tick">钢琴：a_k ∝ 1/k^1.4（暗）</text>')
    parts.append(f'<rect x="{x0 + 180}" y="30" width="10" height="10" fill="{AMBER}"/>')
    parts.append(f'<text x="{x0 + 196}" y="39" class="tick">小提琴：a_k ∝ 1/k^0.75（亮）</text>')
    parts.append(f'<text x="{x0}" y="{y0 + ph + 52}" class="tick">同一个 440 Hz 的音，谐波配比不同，听感就是「钢琴」与「小提琴」。</text>')
    return svg(w, h, "".join(parts), "音色由谐波衰减速度决定")


# ---------------------------------------------------------------- 图 3：螺旋


def fig_spiral() -> str:
    w, h = 460, 470
    cx, base_y = 230, 352
    R, H = 118, 54
    parts = ['<text x="24" y="30" class="title">音高螺旋：八度等价把直线卷成圈</text>']
    pts: list[tuple[float, float]] = []
    for n in range(0, 37):
        octv = n // 12
        pc = n % 12
        theta = 2 * math.pi * pc / 12 - math.pi / 2
        x = cx + R * math.cos(theta)
        y = base_y - octv * H - 0.46 * R * math.sin(theta)
        pts.append((x, y))
    parts.append(f'<path d="{path(pts)}" fill="none" stroke="{TEAL}" stroke-width="2"/>')
    for i, (x, y) in enumerate(pts):
        fill = AMBER if i % 12 == 0 else TEAL
        r = 4.2 if i % 12 == 0 else 2.4
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"/>')
    for n, name in [(0, "C4"), (12, "C5"), (24, "C6"), (36, "C7")]:
        x, y = pts[n]
        parts.append(f'<text x="{x + 10:.1f}" y="{y + 4:.1f}" class="lbl mono">{name}</text>')
    for n, name in [(3, "E♭"), (6, "F♯"), (9, "A")]:
        x, y = pts[n]
        parts.append(f'<text x="{x:.1f}" y="{y - 8:.1f}" text-anchor="middle" class="tick">{name}</text>')
    parts.append(f'<text x="24" y="{h - 18}" class="tick">每绕一圈升高一个八度：螺旋是「频率轴」与「音级圆」的共同母体。</text>')
    return svg(w, h, "".join(parts), "音高螺旋")


# ---------------------------------------------------------------- 图 4：n-TET 误差


def fig_tuning_n() -> str:
    w, h = 740, 320
    # 与 code/ch04_tuning.py 完全一致的目标与权重（含 7:4 小七度）
    targets = [
        (1200 * math.log2(3 / 2), 1.0),
        (1200 * math.log2(5 / 4), 0.8),
        (1200 * math.log2(6 / 5), 0.6),
        (1200 * math.log2(5 / 3), 0.6),
        (1200 * math.log2(9 / 8), 0.5),
        (1200 * math.log2(16 / 15), 0.3),
        (1200 * math.log2(7 / 4), 0.2),
    ]
    xs, rms = [], []
    for n in range(5, 61):
        num = den = 0.0
        for t, wt in targets:
            e = t - round(t * n / 1200) * 1200 / n
            num += wt * e * e
            den += wt
        xs.append(n)
        rms.append(math.sqrt(num / den))

    x0, y0, pw, ph = 60, 56, 640, 200
    parts = ['<text x="28" y="30" class="title">把八度分成 n 份：n 越大越准，但代价是键位暴增</text>']
    parts.append(f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="#ffffff" stroke="{GRID}"/>')
    vmax = 60.0

    def px(n: float) -> float:
        return x0 + pw * (n - 5) / (60 - 5)

    def py(v: float) -> float:
        return y0 + ph - ph * min(v, vmax) / vmax

    for g in range(0, 6):
        v = vmax * g / 5
        y = py(v)
        parts.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0 + pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        parts.append(f'<text x="{x0 - 8}" y="{y + 3:.1f}" text-anchor="end" class="tick">{v:.0f}¢</text>')
    for n in (5, 12, 19, 31, 43, 53):
        x = px(n)
        parts.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0 + ph}" stroke="{GRID}" stroke-dasharray="3 3"/>')
        parts.append(f'<text x="{x:.1f}" y="{y0 + ph + 15}" text-anchor="middle" class="tick">{n}</text>')

    parts.append(f'<path d="{path([(px(n), py(v)) for n, v in zip(xs, rms)])}" fill="none" stroke="{TEAL}" stroke-width="2"/>')

    for n, label in ((12, "12-TET"), (19, "19"), (31, "31"), (41, "41"), (53, "53")):
        v = rms[xs.index(n)]
        x = px(n)
        parts.append(f'<circle cx="{x:.1f}" cy="{py(v):.1f}" r="3.4" fill="{AMBER}"/>')
        parts.append(f'<text x="{x:.1f}" y="{py(v) - 8:.1f}" text-anchor="middle" class="tick mono">{label}</text>')

    parts.append(f'<text x="{x0 + pw - 4}" y="{y0 + 16}" text-anchor="end" class="tick">曲线：7 个目标音程的加权 RMS 误差</text>')
    parts.append(f'<text x="{x0}" y="{y0 + ph + 34}" class="tick">12-TET = {rms[xs.index(12)]:.1f}¢，19-TET = {rms[xs.index(19)]:.1f}¢，31-TET = {rms[xs.index(31)]:.1f}¢，53-TET = {rms[xs.index(53)]:.1f}¢。</text>')
    parts.append(f'<text x="{x0}" y="{y0 + ph + 52}" class="tick">53 在数学上完胜，但 53 个键没人愿意学 —— 12 是工程折中，不是数学最优。</text>')
    return svg(w, h, "".join(parts), "n-TET 加权误差随 n 的变化")


# ---------------------------------------------------------------- 图 5：欧几里得节奏


def euclid(k: int, n: int) -> set[int]:
    """与正文定义 7.1 一致的欧几里得节奏：p_j = floor((j·n + k − 1)/k)。"""
    return {int(math.floor((j * n + k - 1) / k)) for j in range(k)}


def fig_euclidean() -> str:
    w, h = 760, 240
    parts = ['<text x="28" y="28" class="title">欧几里得节奏：把 k 个重音尽量均匀地撒进 n 个格子</text>']
    cases = [(3, 8), (5, 8), (5, 13)]
    for idx, (k, n) in enumerate(cases):
        cx = 130 + idx * 250
        cy = 118
        r = 76
        hits = euclid(k, n)
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GRID}" stroke-width="1.4"/>')
        for i in range(n):
            a = 2 * math.pi * i / n - math.pi / 2
            x = cx + r * math.cos(a)
            y = cy + r * math.sin(a)
            if i in hits:
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{TEAL}"/>')
            else:
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#ffffff" stroke="{MUTED}" stroke-width="1.2"/>')
        text = "".join("x" if i in hits else "." for i in range(n))
        parts.append(f'<text x="{cx}" y="{cy + r + 26}" text-anchor="middle" class="lbl mono">E({k},{n}) = {text}</text>')
    parts.append(f'<text x="28" y="{h - 16}" class="tick">实心 = 重音。互质的 (k,n) 会让重音在循环里错位，产生「滚动感」。</text>')
    return svg(w, h, "".join(parts), "欧几里得节奏")


# ---------------------------------------------------------------- 图 6：五度圈


def fig_circle_of_fifths() -> str:
    w, h = 460, 460
    cx, cy, r = 230, 224, 148
    parts = ['<text x="24" y="28" class="title">五度圈：每次 +7 个半音，12 步回到原点</text>']
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GRID}" stroke-width="1.6"/>')
    names = ["C", "G", "D", "A", "E", "B", "F♯", "D♭", "A♭", "E♭", "B♭", "F"]
    for i, name in enumerate(names):
        a = 2 * math.pi * i / 12 - math.pi / 2
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        tx = cx + (r + 26) * math.cos(a)
        ty = cy + (r + 26) * math.sin(a)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{TEAL if i == 0 else "#ffffff"}" stroke="{TEAL}" stroke-width="1.4"/>')
        color = "#ffffff" if i == 0 else TEAL
        parts.append(f'<text x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle" class="lbl mono" fill="{color}">{i}</text>')
        parts.append(f'<text x="{tx:.1f}" y="{ty + 4:.1f}" text-anchor="middle" class="lbl" fill="{INK}">{name}</text>')
    parts.append(f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" class="lbl" fill="{INK}">五度圈</text>')
    parts.append(f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" class="tick mono">S¹</text>')
    parts.append(f'<text x="24" y="{h - 18}" class="tick">内圈是音级编号（C=0）。7 与 12 互质，所以这个旋转能遍历全部 12 个点。</text>')
    return svg(w, h, "".join(parts), "五度圈")


# ---------------------------------------------------------------- 图 7：大调音阶

NOTE_NAMES = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]
MAJOR = [0, 2, 4, 5, 7, 9, 11]


def fig_major_scale() -> str:
    w, h = 520, 500
    cx, cy, r = 250, 246, 150
    parts = ['<text x="24" y="28" class="title">大调音阶：12 个格子里挑 7 个，且间距为 2-2-1-2-2-2-1</text>']
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GRID}" stroke-width="1.4"/>')
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        on = i in MAJOR
        if on:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{TEAL}"/>')
        else:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#ffffff" stroke="{MUTED}" stroke-width="1.2"/>')
        tx = cx + (r + 28) * math.cos(a)
        ty = cy + (r + 28) * math.sin(a)
        color = INK if on else MUTED
        parts.append(f'<text x="{tx:.1f}" y="{ty + 4:.1f}" text-anchor="middle" class="lbl mono" fill="{color}">{NOTE_NAMES[i]}</text>')
    # 相邻音程标注
    for a_idx, b_idx in zip(MAJOR, MAJOR[1:] + [12]):
        step = (b_idx - a_idx)
        mid = (a_idx + b_idx) / 2 if b_idx != 12 else 11.5
        a = 2 * math.pi * mid / 12 - math.pi / 2
        x = cx + (r - 30) * math.cos(a)
        y = cy + (r - 30) * math.sin(a)
        parts.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" class="tick" fill="{AMBER}">{step}</text>')
    parts.append(f'<text x="{cx}" y="{cy - 4}" text-anchor="middle" class="lbl" fill="{INK}">2-2-1-2-2-2-1</text>')
    parts.append(f'<text x="{cx}" y="{cy + 16}" text-anchor="middle" class="tick">单位：半音</text>')
    parts.append(f'<text x="24" y="{h - 18}" class="tick">实心 = 自然大调音级。两个「1」就是 E–F 与 B–C 的小二度。</text>')
    return svg(w, h, "".join(parts), "大调音阶的间距结构")


def fig_roughness_curve() -> str:
    """第 3 章：粗糙度随音程变化的静态曲线（交互组件的降级版）。"""
    w, h = 740, 340
    base = 330.0
    samples = [(c, dissonance(base, base * ratio_of_cents(c))) for c in range(0, 1201, 2)]
    vmax = max(d for _, d in samples) or 1.0
    x0, y0, pw, ph = 64, 58, 610, 210

    def px(c: float) -> float:
        return x0 + pw * c / 1200.0

    def py(d: float) -> float:
        return y0 + ph - ph * d / vmax

    parts = ['<text x="24" y="28" class="title">粗糙度曲线：谷底 = 协和音程（基频 330 Hz）</text>']
    parts.append(f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="#ffffff" stroke="{GRID}"/>')
    for g in range(0, 5):
        v = vmax * g / 4
        y = py(v)
        parts.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0 + pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        parts.append(f'<text x="{x0 - 8}" y="{y + 3:.1f}" text-anchor="end" class="tick">D={v:.2f}</text>')
    for c in range(0, 1201, 200):
        x = px(c)
        parts.append(f'<line x1="{x:.1f}" y1="{y0 + ph}" x2="{x:.1f}" y2="{y0 + ph + 6}" stroke="{MUTED}"/>')
        parts.append(f'<text x="{x:.1f}" y="{y0 + ph + 18}" text-anchor="middle" class="tick">{c}</text>')
    parts.append(f'<text x="{x0 + pw}" y="{y0 + ph + 36}" text-anchor="end" class="tick">音程（cent）</text>')

    parts.append(
        f'<path d="{path([(px(c), py(d)) for c, d in samples])}" '
        f'fill="none" stroke="{TEAL}" stroke-width="2"/>'
    )

    labels = [(5 / 4, "5:4"), (4 / 3, "4:3"), (3 / 2, "3:2"), (5 / 3, "5:3"), (7 / 4, "7:4")]
    for idx, (ratio, name) in enumerate(labels):
        c = 1200 * math.log2(ratio)
        d = dissonance(base, base * ratio)
        x, y = px(c), py(d)
        parts.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0 + ph}" stroke="{AMBER_SOFT}" stroke-dasharray="3 3"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{AMBER}"/>')
        dy = -12 if idx % 2 == 0 else 14
        parts.append(f'<text x="{x:.1f}" y="{y + dy:.1f}" text-anchor="middle" class="tick mono">{name}</text>')

    peak = max(samples, key=lambda p: p[1])
    parts.append(f'<text x="{px(peak[0]):.1f}" y="{py(peak[1]) - 8:.1f}" text-anchor="middle" class="tick">最粗糙 ≈ {peak[0]:.0f} ¢</text>')
    parts.append(f'<text x="24" y="{h - 16}" class="tick">曲线由 code/common.py 的同一个模型算出：谷底越深，谐波重合越多。</text>')
    return svg(w, h, "".join(parts), "粗糙度随音程变化的曲线")


def fig_harmonic_comb() -> str:
    """第 3 章：两组谐波在频率轴上的重合情况。"""
    w, h = 740, 300
    cases = [(3 / 2, "3:2 纯五度"), (5 / 4, "5:4 大三度")]
    f1 = 220.0
    maxf = 2200.0
    parts = ['<text x="24" y="28" class="title">谐波梳：重合的谱线越多，拍频越少</text>']
    for idx, (ratio, name) in enumerate(cases):
        x0, pw = 48 + idx * 360, 300
        y1, y2 = 120, 176
        parts.append(f'<text x="{x0}" y="58" class="title">{name}</text>')
        parts.append(f'<line x1="{x0}" y1="{y2 + 24}" x2="{x0 + pw}" y2="{y2 + 24}" stroke="{SLATE}"/>')
        for tone, yy, color, label in ((1, y1, TEAL, "f₁ 谐波"), (2, y2, AMBER, "f₂ 谐波")):
            parts.append(f'<text x="{x0 - 4}" y="{yy + 4}" text-anchor="end" class="tick">{label}</text>')
            for k in range(1, 7):
                f = tone * f1 * (ratio if tone == 2 else 1) * k
                if f > maxf:
                    break
                x = x0 + pw * f / maxf
                parts.append(f'<line x1="{x:.1f}" y1="{yy}" x2="{x:.1f}" y2="{yy + 20}" stroke="{color}"/>')
                parts.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="4" fill="{color}"/>')
        # 找出前 8 次谐波内的重合
        for i in range(1, 9):
            for j in range(1, 9):
                if abs(i * f1 - j * f1 * ratio) < 1e-6:
                    f = i * f1
                    if f <= maxf:
                        x = x0 + pw * f / maxf
                        parts.append(f'<line x1="{x:.1f}" y1="{y1}" x2="{x:.1f}" y2="{y2 + 20}" stroke="{TEAL_SOFT}" stroke-width="5" opacity="0.45"/>')
        for f in (500, 1000, 1500, 2000):
            x = x0 + pw * f / maxf
            parts.append(f'<text x="{x:.1f}" y="{y2 + 42}" text-anchor="middle" class="tick">{f}</text>')
        parts.append(f'<text x="{x0 + pw}" y="{y2 + 58}" text-anchor="end" class="tick">频率 (Hz)</text>')
    parts.append(f'<text x="24" y="{h - 16}" class="tick">青色竖带 = 两列谐波精确重合的位置；重合处拍频为 0，但其余谱线仍可能贡献粗糙度。</text>')
    return svg(w, h, "".join(parts), "谐波梳与重合位置")


def fig_euclidean_timeline() -> str:
    """第 7 章：欧几里得节奏与 3:4 叠加的时间线。"""
    w, h = 760, 330
    parts = ['<text x="24" y="28" class="title">时间线：重音如何被均匀地放进 n 个格子</text>']
    rows = [(3, 8), (5, 8), (5, 13)]
    left, top, cell, gap = 118, 62, 38, 54
    for r, (k, n) in enumerate(rows):
        y = top + r * gap
        hits = {int(math.floor((j * n + k - 1) / k)) for j in range(k)}
        parts.append(f'<text x="{left - 12}" y="{y + 23}" text-anchor="end" class="lbl mono">E({k},{n})</text>')
        for i in range(n):
            x = left + i * cell
            fill = TEAL if i in hits else "#ffffff"
            parts.append(f'<rect x="{x}" y="{y}" width="{cell - 3}" height="{cell - 6}" rx="4" fill="{fill}" stroke="{GRID}"/>')
        pattern = "".join("x" if i in hits else "." for i in range(n))
        parts.append(f'<text x="{left + n * cell + 9}" y="{y + 23}" class="tick mono">{pattern}</text>')

    # 3:4 叠加
    y = top + 3 * gap + 14
    parts.append(f'<text x="{left - 12}" y="{y + 23}" text-anchor="end" class="lbl">3:4 叠加</text>')
    for i in range(12):
        x = left + i * cell
        parts.append(f'<rect x="{x}" y="{y}" width="{cell - 3}" height="{cell - 6}" rx="4" fill="#ffffff" stroke="{GRID}"/>')
    for i in range(0, 12, 4):
        x = left + i * cell + (cell - 3) / 2
        parts.append(f'<circle cx="{x:.1f}" cy="{y + 9}" r="6" fill="{TEAL}"/>')
    for i in range(0, 12, 3):
        x = left + i * cell + (cell - 3) / 2
        parts.append(f'<circle cx="{x:.1f}" cy="{y + 26}" r="5" fill="{AMBER}"/>')
    parts.append(f'<text x="24" y="{h - 16}" class="tick">实心 = 起音。3:4 两条周期在 12 步后再次对齐；重合点给出「循环感」的锚点。</text>')
    return svg(w, h, "".join(parts), "欧几里得节奏时间线")


def fig_transition_heatmap() -> str:
    """第 8 章：一阶转移概率矩阵热图。"""
    import ch08_melody as m8

    counts = m8.count_matrix(m8.SEQ)
    probs = m8.row_probs(counts)
    names = m8.NOTE
    w, h = 620, 500
    left, top, cw, chh = 92, 66, 60, 46
    vmax = max(max(row) for row in probs) or 1.0

    def mix(v: float) -> str:
        t = v / vmax
        # 白 -> 青 -> 深青
        r = int(247 - 230 * t)
        g = int(250 - 130 * t)
        b = int(252 - 170 * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    parts = ['<text x="24" y="28" class="title">一阶转移概率 P(xₜ → xₜ₊₁)：空格子就是「语料里没出现」</text>']
    for j, name in enumerate(names):
        x = left + j * cw + cw / 2
        parts.append(f'<text x="{x:.1f}" y="{top - 10}" text-anchor="middle" class="lbl mono">{name}</text>')
    for i, name in enumerate(names):
        y = top + i * chh
        parts.append(f'<text x="{left - 10}" y="{y + 28}" text-anchor="end" class="lbl mono">{name}</text>')
        for j in range(7):
            p = probs[i][j]
            x = left + j * cw
            parts.append(f'<rect x="{x}" y="{y}" width="{cw - 3}" height="{chh - 3}" fill="{mix(p)}" stroke="#ffffff"/>')
            color = "#ffffff" if p / vmax > 0.55 else SLATE
            if p > 0:
                parts.append(f'<text x="{x + cw / 2 - 1:.1f}" y="{y + 28}" text-anchor="middle" class="tick mono" fill="{color}">{p:.2f}</text>')
    parts.append(f'<text x="{left}" y="{top + 7 * chh + 24}" class="tick">行 = 当前音级，列 = 下一音级；每行概率和为 1。</text>')
    parts.append(f'<text x="24" y="{h - 16}" class="tick">颜色越深概率越大。训练语料只有 48 个音，因此很多格子为空 —— 这正是第 8 章讨论的稀疏性。</text>')
    return svg(w, h, "".join(parts), "马尔可夫转移概率热图")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    figs = {
        "harmonics.svg": fig_harmonics,
        "timbre.svg": fig_timbre,
        "spiral.svg": fig_spiral,
        "tuning-n.svg": fig_tuning_n,
        "euclidean.svg": fig_euclidean,
        "circle-of-fifths.svg": fig_circle_of_fifths,
        "major-scale.svg": fig_major_scale,
        "roughness-curve.svg": fig_roughness_curve,
        "harmonic-comb.svg": fig_harmonic_comb,
        "euclidean-timeline.svg": fig_euclidean_timeline,
        "transition-heatmap.svg": fig_transition_heatmap,
    }
    print(f"输出目录：{OUT}")
    for name, fn in figs.items():
        content = fn()
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"  {name:<24}{(OUT / name).stat().st_size / 1024:6.1f} KB")
    total = sum((OUT / n).stat().st_size for n in figs) / 1024
    print(f"合计 {total:.1f} KB")


if __name__ == "__main__":
    main()
