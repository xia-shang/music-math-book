"""
ch07_rhythm.py —— 第 7 章配套实验：欧几里得节奏、切分与复合节拍

运行：
    python code/ch07_rhythm.py

输出：
    表 1  若干 E(k,n) 的二进制模式、间隔与间隔取值
    表 2  带余除法分解：n = q·k + r，长间隔 / 短间隔的个数
    表 3  穷举验证：1 ≤ k ≤ n ≤ 32 的闭式解、Bresenham 判据与最大均匀性
    表 4  n = 8 各 E(k,8) 的切分度量（期望、方差、平均节拍权重、圆重心）
    表 5  互质复合节奏的叠加：LCM、密度、重合点与时间线
    表 6  克拉普环矩阵：3:4 在 Z_3 × Z_4 环面上的表示

约定：E(k,n) 表示在 n 个等分格子里放 k 个起音；位置编号 0..n-1；
       n = 8 与 n = 16 的节拍权重按二进制细分（2 的幂）定义。
"""

import math
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


# ---------------------------------------------------------------- 表格工具


def disp_width(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def pad(text: str, width: int, align: str = "left") -> str:
    gap = max(0, width - disp_width(text))
    if align == "right":
        return " " * gap + text
    return text + " " * gap


def row(cells, widths, aligns) -> str:
    return "  ".join(pad(str(t), w, a) for t, w, a in zip(cells, widths, aligns))


# ---------------------------------------------------------------- 欧几里得节奏


def euclid_positions(k: int, n: int) -> list[int]:
    """E(k,n) 的闭式位置集：p_j = floor((j·n + k − 1)/k)，j = 0..k−1。"""
    if k <= 0:
        return []
    return [(j * n + k - 1) // k for j in range(k)]


def euclid_bits(k: int, n: int) -> list[int]:
    bits = [0] * n
    for p in euclid_positions(k, n):
        if 0 <= p < n:
            bits[p] = 1
    return bits


def bresenham_bits(k: int, n: int) -> list[int]:
    """一行判据：b_i = 1 当且仅当 (i·k mod n) < k。"""
    return [1 if (i * k) % n < k else 0 for i in range(n)]


def gaps_of(k: int, n: int) -> list[int]:
    """循环间隔：相邻起音之间隔了几个格子。"""
    pos = euclid_positions(k, n)
    if k <= 1:
        return [n]
    return [pos[j + 1] - pos[j] for j in range(k - 1)] + [n - pos[-1]]


def render(bits) -> str:
    return "".join("x" if b else "." for b in bits)


def table_patterns() -> None:
    print("表 1：若干欧几里得节奏 E(k,n) 的模式与循环间隔\n")
    cases = [(2, 5), (3, 7), (3, 8), (4, 9), (5, 8), (5, 12), (7, 12), (7, 16)]
    widths = [10, 4, 4, 22, 20, 11]
    aligns = ["left", "right", "right", "left", "left", "left"]
    print(row(["节奏", "k", "n", "模式（x = 起音）", "循环间隔", "间隔取值"], widths, aligns))
    print("-" * 78)
    for k, n in cases:
        bits = euclid_bits(k, n)
        g = gaps_of(k, n)
        lo, hi = min(g), max(g)
        val = f"{lo}" if lo == hi else f"{lo} / {hi}"
        print(row([f"E({k},{n})", k, n, render(bits), " ".join(map(str, g)), val],
                  widths, aligns))
    print("\nE(3,8) 的间隔 3-3-2 就是古巴 tresillo（三击型）的骨架；")
    print("E(5,8) 的间隔 2-2-1-2-1 是五击型节奏（cinquillo 一类）。")
    print("所有间隔只相差不超过 1：这就是「最大均匀」的含义。")


def table_division() -> None:
    print("\n表 2：带余除法 n = q·k + r 与长短间隔的个数\n")
    cases = [(3, 8), (5, 8), (4, 9), (7, 16)]
    widths = [10, 4, 4, 4, 4, 16, 16]
    aligns = ["left", "right", "right", "right", "right", "right", "right"]
    print(row(["节奏", "q", "r", "k", "n", "长间隔(q+1) 个数", "短间隔(q) 个数"], widths, aligns))
    print("-" * 66)
    for k, n in cases:
        q, r = divmod(n, k)
        g = gaps_of(k, n)
        n_long = sum(1 for x in g if x == q + 1)
        n_short = sum(1 for x in g if x == q)
        print(row([f"E({k},{n})", q, r, k, n, n_long, n_short], widths, aligns))
    print("\n由 r = n − q·k 可直接推出：长间隔恰好 r 个、短间隔恰好 k − r 个。")
    print("当 r = 0（k 整除 n）时所有间隔都等于 q，节奏退化为均匀网格。")
    print("下一步的「多出来的 r 个格子」该放在哪，正是欧几里得算法递归下去的理由。")


def table_verify() -> None:
    print("\n表 3：穷举验证 1 ≤ k ≤ n ≤ 32\n")
    total = 0
    same = 0
    even = 0
    max_gap_levels = 0
    for n in range(1, 33):
        for k in range(1, n + 1):
            total += 1
            if euclid_bits(k, n) == bresenham_bits(k, n):
                same += 1
            g = gaps_of(k, n)
            q = n // k
            if all(x in (q, q + 1) for x in g):
                even += 1
            max_gap_levels = max(max_gap_levels, len(set(g)))
    print(f"  测试组合数                    = {total}")
    print(f"  闭式位置集与 Bresenham 判据一致 = {same} / {total}")
    print(f"  所有间隔 ∈ {{⌊n/k⌋, ⌈n/k⌉}}      = {even} / {total}")
    print(f"  间隔取值的最大种类数          = {max_gap_levels}（≤ 2 即最大均匀）")
    print("\n也就是说，一行判据就能生成 E(k,n)，不必模拟递归分组。")
    print("闭式解 p_j = ⌊(j·n + k − 1)/k⌋ 与判据给出同一集合，误差为 0。")


# ---------------------------------------------------------------- 切分度量


def metrical_weights(n: int) -> list[float]:
    """二进制细分下的节拍权重：h(0)=1，h(i)=2^{v2(i)}/n（n 为 2 的幂）。"""
    level = n.bit_length() - 1
    weights = [0.0] * n
    weights[0] = 1.0
    for i in range(1, n):
        v2 = (i & -i).bit_length() - 1
        weights[i] = 2.0 ** (v2 - level)
    return weights


def circular_centroid(positions, n: int):
    """圆重心：返回 (合成长度 R, 方位（步，范围 −n/2..n/2)）。"""
    z = sum(complex(math.cos(2 * math.pi * p / n), math.sin(2 * math.pi * p / n))
            for p in positions) / len(positions)
    r = abs(z)
    if r < 1e-9:
        return r, None
    angle = math.atan2(z.imag, z.real) / (2 * math.pi) * n
    angle = ((angle + n / 2) % n) - n / 2
    return r, angle


def stats(k: int, n: int):
    pos = euclid_positions(k, n)
    mu = sum(pos) / k
    var = sum((p - mu) ** 2 for p in pos) / k
    w = metrical_weights(n)
    mean_h = sum(w[p] for p in pos) / k
    r, angle = circular_centroid(pos, n)
    return pos, mu, var, mean_h, r, angle


def table_syncopation() -> None:
    print("\n表 4：n = 8 的切分度量（期望 μ、方差 σ²、平均节拍权重 h、切分度 1 − h）\n")
    widths = [9, 10, 7, 7, 7, 7, 6, 10]
    aligns = ["left", "left", "right", "right", "right", "right", "right", "right"]
    print(row(["节奏", "模式", "μ（步）", "σ²（步²）", "平均 h", "切分度", "R", "方位（步）"],
              widths, aligns))
    print("-" * 80)
    for k in range(1, 9):
        pos, mu, var, mean_h, r, angle = stats(k, 8)
        sync = 1.0 - mean_h
        where = "—" if angle is None else f"{angle:+.1f}"
        print(row([f"E({k},8)", render(euclid_bits(k, 8)), f"{mu:.3f}", f"{var:.3f}",
                   f"{mean_h:.4f}", f"{sync:.4f}", f"{r:.3f}", where],
                  widths, aligns))

    pos, mu, var, mean_h, r, angle16 = stats(7, 16)
    print("\n  E(7,16)  x..x.x.x..x.x.x.")
    print(f"    μ = {mu:.3f} 步，σ² = {var:.3f} 步²，平均 h = {mean_h:.4f}，"
          f"切分度 = {1.0 - mean_h:.4f}，R = {r:.3f}，方位 = {angle16:+.1f} 步")
    print("\nE(1,8) 只有一个强拍，切分度 0；E(4,8) 把重音均匀铺在 0、2、4、6，")
    print("平均节拍权重 0.5，切分度 0.5，圆重心 R = 0（旋转对称，无偏向）。")
    print("E(3,8) 的切分度 0.5417 略高于 E(4,8)；E(5,8) 的 0.6000 更高。")
    print("E(3,8) 的圆重心合成向量 R = 0.138，方位 −1 步：重音整体略偏晚。")
    print("注意：切分度随 n 变化（n = 16 的弱位更「弱」），只在同一 n 下比较才有意义。")
    print(f"E(7,16) 的圆重心方位 {angle16:+.1f} 步：向小节末尾方向偏移，但合成向量很短。")


# ---------------------------------------------------------------- 复合节奏


def polyrhythm_table() -> None:
    print("\n表 5：互质复合节奏的叠加（t 时刻：x = 快周期，y = 慢周期，O = 重合）\n")
    cases = [(3, 4), (4, 5), (3, 5), (5, 8), (4, 7)]
    widths = [8, 5, 5, 5, 5, 7, 7]
    aligns = ["left", "right", "right", "right", "right", "right", "right"]
    print(row(["叠加", "LCM", "起音数", "去重后", "密度", "重合点", "周期（拍）"], widths, aligns))
    print("-" * 54)
    for m, n in cases:
        lcm = math.lcm(m, n)
        onsets = {t % lcm for t in range(0, lcm, m)} | {t % lcm for t in range(0, lcm, n)}
        coincide = sum(1 for t in range(lcm) if t % m == 0 and t % n == 0)
        density = len(onsets) / lcm
        print(row([f"{m}:{n}", lcm, m + n, len(onsets), f"{density:.3f}",
                   coincide, lcm], widths, aligns))
    print("\n时间线（每格一拍，共 LCM 拍）：")
    for m, n in cases:
        lcm = math.lcm(m, n)
        chars = []
        for t in range(lcm):
            a = t % m == 0
            b = t % n == 0
            chars.append("O" if a and b else ("x" if a else ("y" if b else ".")))
        print(f"  {m}:{n}  " + "".join(chars))
    print("\n两个互质周期只在 t = 0（以及 t = LCM）处重合，恰好 1 个重合点。")
    print("去重后的起音数 = m + n − 1：这就是「叠加不是简单相加」的定量版本。")


def table_matrix() -> None:
    print("\n表 6：克拉普环矩阵（3:4）—— Z_3 × Z_4 环面上的 12 个格子\n")
    m, n = 3, 4
    lcm = m * n
    grid = [["." for _ in range(n)] for _ in range(m)]
    for t in range(lcm):
        i, j = t % m, t % n
        a = t % m == 0
        b = t % n == 0
        grid[i][j] = "O" if a and b else ("x" if a else ("y" if b else "."))
    print("        j=0  j=1  j=2  j=3")
    for i in range(m):
        print(f"  i={i}   " + "    ".join(grid[i]))
    print("\n行 i = t mod 3 对应快周期（每 3 拍一击），列 j = t mod 4 对应慢周期。")
    print("3:4 的 12 个时刻被中国剩余定理一一映射到 3×4 = 12 个格子。")
    print("快节奏占满一整行（4 格），慢节奏占满一整列（3 格），")
    print("并在 (0,0) 重合，所以并集只有 4 + 3 − 1 = 6 个格子被点亮。")


# ---------------------------------------------------------------- 主程序


def main() -> None:
    print("ch07_rhythm.py —— 第 7 章配套实验：节奏的数学\n")
    table_patterns()
    table_division()
    table_verify()
    table_syncopation()
    polyrhythm_table()
    table_matrix()
    print("\n关键数字：")
    print(f"  E(3,8) 的间隔            = {gaps_of(3, 8)}")
    print(f"  E(5,8) 的间隔            = {gaps_of(5, 8)}")
    print(f"  E(7,16) 的间隔           = {gaps_of(7, 16)}")
    print(f"  3:4 的周期               = lcm(3,4) = {math.lcm(3, 4)}")
    print(f"  5:8 的周期               = lcm(5,8) = {math.lcm(5, 8)}")
    print(f"  3:4 去重后的起音数       = 3 + 4 − 1 = {3 + 4 - 1}")
    print(f"  5:8 去重后的起音数       = 5 + 8 − 1 = {5 + 8 - 1}")


if __name__ == "__main__":
    main()
