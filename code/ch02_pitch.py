"""
ch02_pitch.py —— 第 2 章配套实验：音高坐标、八度商空间与音程群

运行：
    python code/ch02_pitch.py

输出：
    表 1  A3–A5 的音名 → 频率 → cent → 螺旋坐标（θ / 圈数）
    表 2  音程加法的两种算法：cent 相加 vs 频率比相乘
    表 3  一个八度内 p:q 音程的复杂度排序（p+q / Stern-Brocot 深度）
    表 4  12-TET 的 12 个音级在螺旋上的坐标

约定：参考音 A4 = 440 Hz，p = 0 ¢；音名按 12-TET 的半音距离排布。
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import cents_of_ratio, freq_of_pitch, pitch_of_freq, ratio_of_cents  # noqa: E402

def disp_width(text: str) -> int:
    import unicodedata

    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def pad(text: str, width: int, align: str = "left") -> str:
    gap = max(0, width - disp_width(text))
    if align == "right":
        return " " * gap + text
    return text + " " * gap


def row(cells: list[str], widths: list[int], aligns: list[str]) -> str:
    """把若干单元格按显示宽度对齐后拼成一行。"""
    return "  ".join(pad(t, w, a) for t, w, a in zip(cells, widths, aligns))


# ---------------------------------------------------------------- 音名表
# (音名, 相对 A4 的半音数)；A3 = -12，A5 = +12。
NOTE_TABLE = [
    ("A3", -12), ("B3", -10), ("C4", -9), ("D4", -7), ("E4", -5),
    ("F4", -4), ("G4", -2), ("A4", 0), ("B4", 2), ("C5", 3),
    ("D5", 5), ("E5", 7), ("F5", 8), ("G5", 10), ("A5", 12),
]


def table_notes() -> None:
    print("表 1：A3–A5 的音名、频率与螺旋坐标\n")
    widths = [8, 6, 12, 11, 9, 6]
    aligns = ["left", "right", "right", "right", "right", "right"]
    print(row(["音名", "半音", "频率 (Hz)", "cent", "θ", "圈数"], widths, aligns))
    print("-" * 62)
    for name, semis in NOTE_TABLE:
        cents = 100.0 * semis
        f = freq_of_pitch(cents)
        theta = (cents / 1200.0) % 1.0
        turn = math.floor(cents / 1200.0)
        # 取模后 1.0 与 0.0 是同一个点，统一写成 0.0000
        if abs(theta - 1.0) < 1e-12:
            theta = 0.0
        print(row([name, f"{semis:+d}", f"{f:.3f}", f"{cents:+.1f}",
                   f"{theta:.4f}", f"{turn:+d}"], widths, aligns))
    print("\nθ 是「音级」坐标（0~1 表示一个八度内的位置），圈数是八度的编号；")
    print("两者合起来就是螺旋坐标：r = log₂ f 给出高度，θ 给出角度。")


# ---------------------------------------------------------------- 音程加法
def table_interval_addition() -> None:
    pairs = [
        ("纯五度 × 纯四度", 3, 2, 4, 3),
        ("大三度 × 纯四度", 5, 4, 4, 3),
        ("大三度 × 小三度", 5, 4, 6, 5),
        ("小三度 × 大六度", 6, 5, 5, 3),
        ("纯五度 × 纯五度", 3, 2, 3, 2),
        ("纯八度 × 纯五度", 2, 1, 3, 2),
    ]
    print("\n表 2：音程加法的两种算法（cent 相加 vs 频率比相乘）\n")
    widths = [16, 8, 8, 9, 9, 8, 8]
    aligns = ["left", "right", "right", "right", "right", "right", "right"]
    print(row(["运算", "左 ¢", "右 ¢", "和 ¢", "积 ¢", "模 1200", "误差"], widths, aligns))
    print("-" * 78)
    for label, p1, q1, p2, q2 in pairs:
        r1 = Fraction(p1, q1)
        r2 = Fraction(p2, q2)
        prod = r1 * r2
        c1 = cents_of_ratio(float(r1))
        c2 = cents_of_ratio(float(r2))
        cp = cents_of_ratio(float(prod))
        total = c1 + c2
        err = abs(total - cp)
        print(row([label, f"{c1:.3f}", f"{c2:.3f}", f"{total:.3f}", f"{cp:.3f}",
                   f"{total % 1200.0:.3f}", f"{err:.2e}"], widths, aligns))
    print("\n每一行的「和 ¢」与「积 ¢」在浮点精度内相等：")
    print("φ(r₁r₂) = φ(r₁) + φ(r₂)，这就是定理 2.1 的数值版本。")
    print("最后一列把音程折回一个八度：5:4 与 6:5 相加得到 3:2，折回仍是 702 ¢；")
    print("3:2 自乘得到 9:4，折回后是 204 ¢ —— 音级空间里只剩「方向」，不再有圈数。")


# ---------------------------------------------------------------- 复杂度排序
def stern_brocot_depth(p: int, q: int) -> int:
    """既约分数 p/q 在 Stern-Brocot 树中的深度 = 连分数部分和 − 1。"""
    a = []
    while q:
        a.append(p // q)
        p, q = q, p % q
    return sum(a) - 1


INTERVAL_NAMES = {
    (1, 1): "纯一度", (2, 1): "纯八度", (3, 2): "纯五度", (4, 3): "纯四度",
    (5, 3): "大六度", (5, 4): "大三度", (6, 5): "小三度", (8, 5): "小六度",
    (7, 4): "和声小七度", (9, 8): "大二度",
}


def table_complexity() -> None:
    print("\n表 3：一个八度内 p:q 音程的复杂度排序（p+q 升序，并列按音高升序）\n")
    items = []
    for p in range(1, 10):
        for q in range(1, 10):
            if p < q or p > 2 * q:
                continue
            f = Fraction(p, q)
            if f.denominator == q:
                items.append((f, p, q))
    items.sort(key=lambda t: (t[0].numerator + t[0].denominator, float(t[0])))
    widths = [8, 10, 6, 8, 12]
    aligns = ["left", "right", "right", "right", "left"]
    print(row(["比值", "cent", "p+q", "SB 深度", "名称"], widths, aligns))
    print("-" * 52)
    for f, p, q in items:
        cents = cents_of_ratio(float(f))
        name = INTERVAL_NAMES.get((p, q), "—")
        print(row([f"{p}:{q}", f"{cents:.2f}", str(p + q),
                   str(stern_brocot_depth(p, q)), name], widths, aligns))
    print("\np+q 越小，频率比越「简单」；SB 深度是同一个直觉的树版本：")
    print("1:1 在树根（深度 0），3:2 是「右-左」两步（深度 2）。")
    print("两种排序大体一致，但在 7:4 这类「分子大而分母适中」的比上会出现分歧。")


# ---------------------------------------------------------------- 12-TET 坐标
TET_NAMES = ["纯一度", "小二度", "大二度", "小三度", "大三度", "纯四度",
             "三全音", "纯五度", "小六度", "大六度", "小七度", "大七度"]


def table_tet() -> None:
    print("\n表 4：12-TET 的 12 个音级在螺旋上的坐标\n")
    widths = [4, 8, 8, 8, 12]
    aligns = ["right", "right", "right", "left", "right"]
    print(row(["k", "cent", "θ", "名称", "频率 (Hz)"], widths, aligns))
    print("-" * 48)
    for k in range(12):
        cents = 100.0 * k
        theta = k / 12.0
        print(row([str(k), f"{cents:.1f}", f"{theta:.4f}", TET_NAMES[k],
                   f"{freq_of_pitch(cents):.3f}"], widths, aligns))
    print("\nθ = k/12 严格等距：平均律把单位圆切成 12 等份，")
    print("每一步的比值都是 2^(1/12) ≈ 1.059463，即每半音 +100 ¢。")


def main() -> None:
    print("ch02_pitch.py —— 第 2 章配套实验（参考音 A4 = 440 Hz，p = 0 ¢）\n")
    table_notes()
    table_interval_addition()
    table_complexity()
    table_tet()
    print("\n一致性检查：")
    print(f"  cents(2:1)      = {cents_of_ratio(2.0):.3f} ¢（应等于 1200）")
    print(f"  2^(1200/1200)   = {ratio_of_cents(1200.0):.6f}（应等于 2）")
    print(f"  pitch(440 Hz)   = {pitch_of_freq(440.0):.3f} ¢（应等于 0）")
    print(f"  freq(0 ¢)       = {freq_of_pitch(0.0):.3f} Hz（应等于 440）")


if __name__ == "__main__":
    main()
