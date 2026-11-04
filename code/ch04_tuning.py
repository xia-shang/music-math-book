"""
ch04_tuning.py —— 第 4 章配套实验：律制的误差预算

运行：
    python code/ch04_tuning.py

输出：
    表 1  五度链 12 步：累计 cent、折回一个八度后的位置、毕达哥拉斯音差
    表 2  三种律制下 7 个自然音级相对 12-TET 的偏差
    表 3  12 音五度链的闭合五度（狼五度）与相邻音级间距
    表 4  固定目标音程、搜索 n = 5~60 的加权 RMS 误差与前 5 名
    表 5  几个候选 n 的分项误差（五度 / 大三度 / 最大误差 / 加权 RMS）

约定：以 C = 0 ¢ 为起点；纯律与五度相生律的比值来自 common.py。
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    cents_of_ratio,
    just_major_ratios,
    pythagorean_major_ratios,
    ratio_of_cents,
)

FIFTH = cents_of_ratio(3.0 / 2.0)  # 701.955 ¢
MAJOR_THIRD = cents_of_ratio(5.0 / 4.0)  # 386.314 ¢
MINOR_THIRD = cents_of_ratio(6.0 / 5.0)  # 315.642 ¢


def disp_width(text: str) -> int:
    import unicodedata

    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def pad(text: str, width: int, align: str = "left") -> str:
    gap = max(0, width - disp_width(text))
    if align == "right":
        return " " * gap + text
    return text + " " * gap


def row(cells: list[str], widths: list[int], aligns: list[str]) -> str:
    return "  ".join(pad(t, w, a) for t, w, a in zip(cells, widths, aligns))


def table_fifths() -> None:
    print("表 1：五度链 12 步（每步 +701.955 ¢，每步都折回一个八度）\n")
    widths = [6, 12, 12, 14]
    aligns = ["right", "right", "right", "right"]
    print(row(["k", "累计 ¢", "折叠 ¢", "离最近半音"], widths, aligns))
    print("-" * 45)
    for k in range(13):
        total = k * FIFTH
        folded = total % 1200.0
        # 离最近 100 ¢ 整格的距离（12-TET 的半音格）
        nearest = round(folded / 100.0) * 100.0
        diff = folded - nearest
        print(row([str(k), f"{total:.3f}", f"{folded:.3f}", f"{diff:+.3f}"],
                  widths, aligns))
    comma = 12 * FIFTH - 7 * 1200.0
    ratio = (1.5 ** 12) / (2.0 ** 7)
    print(f"\n12 个纯五度 = {12 * FIFTH:.3f} ¢；7 个八度 = 8400.000 ¢。")
    print(f"差 = 毕达哥拉斯音差 = {comma:.3f} ¢；(3/2)^12 / 2^7 = {ratio:.6f}。")
    print("第 k=12 行的折叠位置是 23.460 ¢ —— 五度链无法在第 12 步精确闭合。")


def table_scale_errors() -> None:
    print("\n表 2：三种律制下 7 个自然音级相对 12-TET 的偏差\n")
    just = just_major_ratios()
    pyth = pythagorean_major_ratios()
    names = ["C", "D", "E", "F", "G", "A", "B"]
    widths = [6, 11, 11, 11, 11, 11, 11]
    aligns = ["left", "right", "right", "right", "right", "right", "right"]
    print(row(["音级", "12-TET ¢", "纯律 ¢", "五度 ¢", "纯律偏差", "五度偏差", "纯律比"],
              widths, aligns))
    print("-" * 78)
    for i, name in enumerate(names):
        tet = [0.0, 200.0, 400.0, 500.0, 700.0, 900.0, 1100.0][i]
        j = cents_of_ratio(just[i])
        p = cents_of_ratio(pyth[i])
        print(row([name, f"{tet:.1f}", f"{j:.3f}", f"{p:.3f}",
                   f"{j - tet:+.3f}", f"{p - tet:+.3f}",
                   f"{just[i]:.4f}"], widths, aligns))
    print("\n纯律的 C-E、F-A、G-B 都是 5:4（386.314 ¢），比 12-TET 的大三度低 13.686 ¢；")
    print("五度相生律把大三度抬到 407.820 ¢，比 12-TET 高 7.820 ¢。")
    print("两条曲线在 400 ¢ 附近分道扬镳：这就是 4.2 与 4.3 要解释的取舍。")


def table_wolf() -> None:
    print("\n表 3：12 音五度链的闭合五度与相邻音级间距\n")
    folded = sorted((k * FIFTH) % 1200.0 for k in range(12))
    widths = [12, 12, 12]
    aligns = ["right", "right", "right"]
    print(row(["音级序号", "折叠 ¢", "与前一级差"], widths, aligns))
    print("-" * 40)
    for i, c in enumerate(folded):
        prev = folded[i - 1]
        gap = (c - prev) % 1200.0
        print(row([str(i), f"{c:.3f}", f"{gap:.3f}"], widths, aligns))
    wolf = 1200.0 - (11 * FIFTH) % 1200.0  # 第 11 个五度音级到下一个 C 的"五度"
    print(f"\n链的闭合五度（k=11 的音级 → 下一个 C）= {wolf:.3f} ¢。")
    print(f"它比纯五度 {FIFTH:.3f} ¢ 短 {FIFTH - wolf:.3f} ¢ —— 这就是狼五度。")
    print("12 个音级之间的间距只有两种：90.225 ¢（小二度 limma）与 113.685 ¢（大二度）。")


TARGETS = [
    ("纯五度 3:2", 3.0 / 2.0, 1.0),
    ("大三度 5:4", 5.0 / 4.0, 0.8),
    ("小三度 6:5", 6.0 / 5.0, 0.6),
    ("大六度 5:3", 5.0 / 3.0, 0.6),
    ("大二度 9:8", 9.0 / 8.0, 0.5),
    ("小二度 16:15", 16.0 / 15.0, 0.3),
    ("小七度 7:4", 7.0 / 4.0, 0.2),
]


def tet_error(target_cents: float, n: int) -> float:
    """目标音程在 n-TET 上的最近整数步误差（带符号，落在 ±半步内）。"""
    step = 1200.0 / n
    k = round(target_cents / step)
    return target_cents - k * step


def weighted_rms(n: int) -> float:
    num = 0.0
    den = 0.0
    for _, ratio, weight in TARGETS:
        e = tet_error(cents_of_ratio(ratio), n)
        num += weight * e * e
        den += weight
    return math.sqrt(num / den)


def worst_error(n: int) -> float:
    return max(abs(tet_error(cents_of_ratio(r), n)) for _, r, _ in TARGETS)


def table_search() -> None:
    print("\n表 4：固定 7 个目标音程，搜索 n = 5~60 的加权 RMS 误差（前 5 名）\n")
    scores = [(weighted_rms(n), n) for n in range(5, 61)]
    scores.sort()
    widths = [10, 12, 14, 14]
    aligns = ["right", "right", "right", "right"]
    print(row(["n", "每步 ¢", "加权 RMS ¢", "最大误差 ¢"], widths, aligns))
    print("-" * 44)
    for score, n in scores[:5]:
        print(row([str(n), f"{1200.0 / n:.3f}", f"{score:.3f}", f"{worst_error(n):.3f}"],
                  widths, aligns))
    print("\n12 不在前 5 名：它的加权 RMS 误差明显大于 19、31、53 等候选。")
    print("但 12 有一个别人没有的性质 —— 转调后所有音程都不变，见 4.3。")


def table_candidates() -> None:
    print("\n表 5：几个候选 n 的分项误差\n")
    widths = [6, 11, 13, 13, 12, 12]
    aligns = ["right", "right", "right", "right", "right", "right"]
    print(row(["n", "每步 ¢", "五度误差", "大三度误差", "最大误差", "加权 RMS"], widths, aligns))
    print("-" * 60)
    for n in (12, 19, 24, 31, 41, 53):
        e5 = tet_error(cents_of_ratio(3.0 / 2.0), n)
        e3 = tet_error(cents_of_ratio(5.0 / 4.0), n)
        print(row([str(n), f"{1200.0 / n:.3f}", f"{e5:+.3f}", f"{e3:+.3f}",
                   f"{worst_error(n):.3f}", f"{weighted_rms(n):.3f}"], widths, aligns))
    print("\n53-TET 几乎是「有理比的复印机」：五度误差不到 0.1 ¢，大三度约 1.4 ¢。")
    print("19-TET 把五度与大三度都摊到 +7 ¢ 左右；31-TET 更偏重大三度；53-TET 两头都照顾。")


def main() -> None:
    print("ch04_tuning.py —— 第 4 章配套实验：律制的误差预算\n")
    table_fifths()
    table_scale_errors()
    table_wolf()
    table_search()
    table_candidates()
    print("\n关键数字：")
    print(f"  纯五度          = {FIFTH:.3f} ¢")
    print(f"  纯律大三度      = {MAJOR_THIRD:.3f} ¢（比 12-TET 低 {400.0 - MAJOR_THIRD:.3f} ¢）")
    print(f"  毕达哥拉斯音差  = {12 * FIFTH - 8400.0:.3f} ¢")
    print(f"  三个纯律大三度  = {3 * MAJOR_THIRD:.3f} ¢（离八度还差 {1200.0 - 3 * MAJOR_THIRD:.3f} ¢）")
    print(f"  2^(1/12)        = {ratio_of_cents(100.0):.9f}")


if __name__ == "__main__":
    main()
