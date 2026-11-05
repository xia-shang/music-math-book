"""
ch06_harmony.py —— 第 6 章配套实验：和弦的线性代数

运行：
    python code/ch06_harmony.py

输出：
    表 1  12 音级协和度矩阵 M（M_ij = S(i,j)，基准 C4）
    表 2  四类和弦的内部协和度（均值 / 最小 / 三和弦示例）
    表 3  220 个三音集合里协和度最高的 5 个与最低的 3 个
    表 4  移位 T_n / 倒置 I 作用在 C 大三和弦上的结果
    表 5  T、S、D 三个功能向量之间的声部进行距离与转移矩阵 P
    表 6  从 T 出发的 24 步功能序列、经验频率与平稳分布
    表 7  终止式 D→T 的声部移动与势能差

约定：音级编号 C=0, …, B=11；只使用 12-TET；协和度复用 common.py 的模型。
"""

import itertools
import math
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import A4, consonance  # noqa: E402

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
C4 = A4 * 2.0 ** (-9.0 / 12.0)
QUALITY = {"major": "大三", "minor": "小三", "aug": "增三", "dim": "减三"}


# ---------------------------------------------------------------- 表格工具


def disp_width(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def pad(text: str, width: int, align: str = "left") -> str:
    gap = max(0, width - disp_width(text))
    if align == "right":
        return " " * gap + text
    return text + " " * gap


def row(cells, widths, aligns) -> str:
    return "  ".join(pad(t, w, a) for t, w, a in zip(cells, widths, aligns))


def freq(p: int) -> float:
    return C4 * 2.0 ** (p / 12.0)


# ---------------------------------------------------------------- 基本对象


def build_matrix() -> list[list[float]]:
    """M_ij = S(f(i), f(j))，12×12。"""
    return [[consonance(freq(i), freq(j)) for j in range(12)] for i in range(12)]


def chord_vec(notes) -> tuple[int, ...]:
    """12 维指示向量。"""
    v = [0] * 12
    for n in notes:
        v[n % 12] = 1
    return tuple(v)


def chord_score(M, notes) -> float:
    """和弦内部两两协和度的均值。"""
    pairs = list(itertools.combinations(notes, 2))
    return sum(M[i][j] for i, j in pairs) / len(pairs)


def min_pair(M, notes) -> float:
    return min(M[i][j] for i, j in itertools.combinations(notes, 2))


def classify(notes):
    """识别三和弦：返回 (根音, 性质) 或 None。"""
    s = set(notes)
    for root in notes:
        d = sorted((n - root) % 12 for n in notes)
        if d == [0, 4, 7]:
            return root, "major"
        if d == [0, 3, 7]:
            return root, "minor"
        if d == [0, 4, 8]:
            return root, "aug"
        if d == [0, 3, 6]:
            return root, "dim"
    return None


def chord_name(notes) -> str:
    c = classify(notes)
    if c is None:
        return "（非三和弦）"
    root, q = c
    return f"{NAMES[root]} {QUALITY[q]}"


# ---------------------------------------------------------------- 表 1：M


def table_matrix(M) -> None:
    print("表 1：12 音级协和度矩阵 M（行 = 第一个音，列 = 第二个音）\n")
    head = "     " + " ".join(f"{NAMES[j]:>4}" for j in range(12))
    print(head)
    print("-" * len(head))
    for i in range(12):
        cells = " ".join(f"{M[i][j]:.2f}" for j in range(12))
        print(f"{NAMES[i]:>3}  {cells}")
    off = [M[i][j] for i in range(12) for j in range(12) if i != j]
    hi, lo = max(off), min(off)
    print(f"\n对角线在两位小数下全为 1.00，但并非严格等于 1：跨阶谐波对仍有微小正贡献。")
    print(f"非对角元范围 {lo:.2f} ~ {hi:.2f}；纯五度也四舍五入为 1.00。")
    print("最小值出现在 A–A♯、A♯–B 这两个相邻音对，不应笼统归给三全音。M 对称：S(i,j) = S(j,i)。")


# ---------------------------------------------------------------- 表 2：和弦类型


def table_types(M) -> None:
    print("\n表 2：四类三和弦的内部协和度\n")
    examples = {
        "major": (0, 4, 7),
        "minor": (0, 3, 7),
        "aug": (0, 4, 8),
        "dim": (0, 3, 6),
    }
    widths = [8, 14, 12, 12, 12, 24]
    aligns = ["left", "left", "right", "right", "right", "left"]
    print(row(["性质", "C 为根", "均值 S", "最小 S", "全类平均", "三个音程"],
              widths, aligns))
    print("-" * 88)
    for q in ("major", "minor", "aug", "dim"):
        notes = examples[q]
        gaps = sorted((b - a) % 12 for a, b in itertools.combinations(notes, 2))
        scores = [chord_score(M, tuple((n + t) % 12 for n in notes)) for t in range(12)]
        avg = sum(scores) / len(scores)
        print(row([QUALITY[q], chord_name(notes),
                   f"{chord_score(M, notes):.4f}", f"{min_pair(M, notes):.4f}",
                   f"{avg:.4f}", " / ".join(f"{100 * g} ¢" for g in gaps)],
                  widths, aligns))
    print("\n以 C 为根时：大三 0.8868 > 增三 0.8757 > 小三 0.8562 > 减三 0.7437。")
    print("把 12 个根音平均后，大三与小三都约为 0.9099（相差不到 0.0001）：")
    print("它们的音程多重集相同（3、4、7 个半音），只是排列顺序不同。")
    print("增三 0.8959，减三 0.8440。")

    print("\nC 大三和弦的 3×3 协和子矩阵 K：\n")
    notes = (0, 4, 7)
    print("      " + " ".join(f"{NAMES[n]:>6}" for n in notes))
    for a in notes:
        cells = " ".join(f"{M[a][b]:6.3f}" for b in notes)
        print(f"  {NAMES[a]:>3}  {cells}")
    print("\n在三位小数下，对角元为行内最大；这不是线性代数中「严格对角占优」的标准结论（命题 6.2）。")


# ---------------------------------------------------------------- 表 3：220 个三音集合


def table_all_triads(M) -> None:
    print("\n表 3：C(12,3)=220 个三音集合的协和度排序\n")
    scored = []
    for combo in itertools.combinations(range(12), 3):
        scored.append((chord_score(M, combo), combo))
    scored.sort(reverse=True)
    widths = [5, 26, 10, 14]
    aligns = ["right", "left", "right", "left"]
    print(row(["名次", "音级", "均值 S", "识别"], widths, aligns))
    print("-" * 60)
    for i, (s, notes) in enumerate(scored[:5], 1):
        print(row([str(i), " ".join(NAMES[n] for n in notes), f"{s:.4f}",
                   chord_name(notes)], widths, aligns))
    print("  ...")
    for i, (s, notes) in enumerate(scored[-3:], len(scored) - 2):
        print(row([str(i), " ".join(NAMES[n] for n in notes), f"{s:.4f}",
                   chord_name(notes)], widths, aligns))
    by_type = {}
    for s, notes in scored:
        c = classify(notes)
        if c is not None:
            by_type.setdefault(c[1], []).append(s)
    print("\n按类型平均（12 个根音的集合都算）：")
    for q in ("major", "minor", "aug", "dim"):
        vals = by_type[q]
        print(f"  {QUALITY[q]}：{len(vals)} 个集合，平均 {sum(vals) / len(vals):.4f}，"
              f"最高 {max(vals):.4f}")
    print("排在最前的是大三和弦与小三和弦（G、F#、F、Bm、E 等）：")
    print("一个纯五度加一个三度，正好落在 3.3 节粗糙度曲线的谷底上。")

    def canon_t(s):
        return min(tuple(sorted((x + t) % 12 for x in s)) for t in range(12))

    def canon_ti(s):
        return min(canon_t(s), canon_t(tuple((-x) % 12 for x in s)))

    t_classes = {canon_t(c) for c in itertools.combinations(range(12), 3)}
    ti_classes = {canon_ti(c) for c in itertools.combinations(range(12), 3)}
    print(f"\n220 个三音集合按平移去重剩 {len(t_classes)} 类，再按平移+倒置去重剩 "
          f"{len(ti_classes)} 类。")


# ---------------------------------------------------------------- 表 4：变换


def perm_matrix_T(n: int) -> list[list[int]]:
    """T_n 的置换矩阵：w[i] = v[(i - n) mod 12]。"""
    return [[1 if (i - n) % 12 == j else 0 for j in range(12)] for i in range(12)]


def perm_matrix_I() -> list[list[int]]:
    """倒置 I：w[i] = v[(-i) mod 12]。"""
    return [[1 if (-i) % 12 == j else 0 for j in range(12)] for i in range(12)]


def apply(mat, v) -> tuple[int, ...]:
    return tuple(sum(mat[i][j] * v[j] for j in range(12)) for i in range(12))


def notes_of(v) -> tuple[int, ...]:
    return tuple(i for i, x in enumerate(v) if x)


def table_transforms() -> None:
    print("\n表 4：移位与倒置作为置换矩阵（以 C 大三和弦为例）\n")
    v = chord_vec((0, 4, 7))
    widths = [10, 30, 30]
    aligns = ["left", "left", "left"]
    print(row(["变换", "作用后的向量（音级）", "和弦名"], widths, aligns))
    print("-" * 74)
    cases = [("恒等", None), ("T_4", perm_matrix_T(4)),
             ("T_7", perm_matrix_T(7)), ("I", perm_matrix_I())]
    for label, mat in cases:
        w = v if mat is None else apply(mat, v)
        print(row([label, " ".join(NAMES[n] for n in notes_of(w)),
                   chord_name(notes_of(w))], widths, aligns))
    print("\nT_n 把 {0,4,7} 送到 {n,n+4,n+7}；I 把它送到 {0,5,8}，即 F 小三和弦。")
    print("T_n ∘ T_m = T_{n+m}，且 I ∘ T_n ∘ I = T_{-n}，所以 {T_n, I} 生成 24 阶二面体群。")
    print("表 4 只展示了 4 个代表；完整群有 24 个元素（12 个平移 + 12 个倒置平移）。")


# ---------------------------------------------------------------- 表 5：功能与转移


FUNCTIONS = {
    "T": (0, 4, 7),    # C 大三
    "S": (5, 9, 0),    # F 大三
    "D": (7, 11, 2),   # G 大三
}


def circular_dist(a: int, b: int) -> int:
    d = abs(a - b) % 12
    return min(d, 12 - d)


def voice_leading(a, b) -> tuple[int, tuple[int, ...]]:
    """最优声部进行：枚举 3! 种配对，取最短总距离。"""
    best = None
    for perm in itertools.permutations(b):
        total = sum(circular_dist(x, y) for x, y in zip(a, perm))
        if best is None or total < best[0]:
            best = (total, perm)
    assert best is not None
    return best


def table_functions() -> None:
    print("\n表 5：T / S / D 的声部进行距离与转移矩阵\n")
    keys = ["T", "S", "D"]
    widths = [10, 34, 12]
    aligns = ["left", "left", "right"]
    print(row(["方向", "最优配对（起点→终点）", "总距离（半音）"], widths, aligns))
    print("-" * 60)
    dist = {}
    for i in keys:
        for j in keys:
            d, perm = voice_leading(FUNCTIONS[i], FUNCTIONS[j])
            dist[(i, j)] = d
            if i == j:
                continue
            moves = "，".join(f"{NAMES[x]}→{NAMES[y]}" for x, y in zip(FUNCTIONS[i], perm))
            print(row([f"{i}→{j}", moves, str(d)], widths, aligns))

    gravity = {"T": 1.00, "S": 0.85, "D": 0.75}
    print("\n转移矩阵 P（行 = 当前功能，列 = 下一功能）：")
    print("     " + "  ".join(f"{k:>6}" for k in keys))
    P = []
    for i in range(3):
        w = [gravity[keys[j]] * math.exp(-dist[(keys[i], keys[j])] / 2.0)
             for j in range(3)]
        s = sum(w)
        P.append([x / s for x in w])
        print(f"  {keys[i]}  " + "  ".join(f"{x:6.3f}" for x in P[i]))
    print("\nP_ij ∝ w_j · exp(−d_ij/2)，w 表示三个功能的「引力」权重（T 最大）。")
    print("对角线元都大于同行的任一非对角元：功能有惯性，不会每拍都换。")
    return P


# ---------------------------------------------------------------- 表 6：模拟


def stationary(P, steps: int = 4000) -> list[float]:
    pi = [1.0 / 3.0] * 3
    for _ in range(steps):
        pi = [sum(pi[i] * P[i][j] for i in range(3)) for j in range(3)]
    return pi


def table_walk(P) -> None:
    print("\n表 6：从 T 出发的功能序列（固定随机种子）\n")
    import random

    random.seed(2024)
    keys = ["T", "S", "D"]
    cur = 0
    seq = [cur]
    for _ in range(23):
        r = random.random()
        acc = 0.0
        for j in range(3):
            acc += P[cur][j]
            if r < acc:
                cur = j
                break
        seq.append(cur)
    print("  " + " ".join(keys[i] for i in seq[:24]))
    freq = [sum(1 for i in seq if i == k) / len(seq) for k in range(3)]
    pi = stationary(P)
    print("\n  功能   经验频率   平稳分布 π   势能 −log π")
    for k in range(3):
        print(f"   {keys[k]}     {freq[k]:.3f}      {pi[k]:.3f}       {-math.log(pi[k]):+.3f}")
    print("\n24 步只是短样本，经验频率与 π 有偏差；4000 次幂迭代使分布收敛到 π。")
    print("π 是分布动力学的吸引子；π(D) 较低来自权重与连通结构，不等于 D 的自环率低。")


# ---------------------------------------------------------------- 表 7：终止式


def table_cadence(P) -> None:
    print("\n表 7：终止式 D→T 的声部移动\n")
    d_set, t_set = FUNCTIONS["D"], FUNCTIONS["T"]
    total, perm = voice_leading(d_set, t_set)
    widths = [10, 10, 12, 10]
    aligns = ["left", "left", "right", "left"]
    print(row(["D 的音", "T 的音", "移动（半音）", "方向"], widths, aligns))
    print("-" * 44)
    for x, y in zip(d_set, perm):
        delta = (y - x) % 12
        signed = delta if delta <= 6 else delta - 12
        label = "保持" if signed == 0 else ("升" if signed > 0 else "降")
        print(row([NAMES[x], NAMES[y], f"{signed:+d}", label], widths, aligns))
    pi = stationary(P)
    print(f"\n势能差：E(D) − E(T) = −log π(D) − (−log π(T)) = "
          f"{-math.log(pi[2]) + math.log(pi[0]):.3f}。")
    print(f"三个声部的总移动 = {total} 个半音；G 保持不动、B 上行半音、D 上行两个半音。")
    print("E(T) 最低，所以 D→T 是沿势能下降方向的一步 —— 这就是「属和弦解决到主和弦」。")


# ---------------------------------------------------------------- 主程序


def main() -> None:
    print("ch06_harmony.py —— 第 6 章配套实验：和弦的线性代数\n")
    M = build_matrix()
    table_matrix(M)
    table_types(M)
    table_all_triads(M)
    table_transforms()
    P = table_functions()
    table_walk(P)
    table_cadence(P)
    print("\n关键数字：")
    print(f"  12 音级对数            = C(12,2) = {12 * 11 // 2}")
    print(f"  三音集合数            = C(12,3) = {math.comb(12, 3)}")
    print(f"  C 大三和弦内部 S 均值 = {chord_score(M, (0, 4, 7)):.4f}")
    print(f"  增三和弦内部 S 均值   = {chord_score(M, (0, 4, 8)):.4f}")
    print(f"  T→S / S→D / D→T 距离  = "
          f"{voice_leading(FUNCTIONS['T'], FUNCTIONS['S'])[0]} / "
          f"{voice_leading(FUNCTIONS['S'], FUNCTIONS['D'])[0]} / "
          f"{voice_leading(FUNCTIONS['D'], FUNCTIONS['T'])[0]}")


if __name__ == "__main__":
    main()
