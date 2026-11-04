"""
ch09_topology.py —— 第 9 章配套实验：五度圈、调性图与随机游走

运行：
    python code/ch09_topology.py

输出：
    表 1  五度圈的 12 个位置：位置 n 的主音、调号与音级
    表 2  二音和弦空间：音程类的无序集合数与有序和弦数（商掉 T 与 T/I 之后）
    表 3  24 个大小调：调号位置、与 C 大调的共同音数、到 C 大调的最短代价
    表 4  两条最短转调路径：C 大调 → F♯ 小调、C 大调 → B♭ 小调
    表 5  调性图的统计：节点、边、直径与平均最短路
    表 6  无调性与有调性随机游走：平稳熵、圆重心、行熵

约定：
    - 音级用 0..11（12-TET，C = 0）；
    - 每个调用「调号位置 n ∈ Z_12 + 模式」表示：位置 n 的大调主音是 7n mod 12，
      位置 n 的小调主音是 (7n + 9) mod 12（关系大调低小三度）；
      因此 A 小调与 C 大调同在位置 0，F♯ 小调与 A 大调同在位置 3。
    - 等音异名按调号位置取一种写法（位置 7 取 D♭ 而不是 C♯），不影响任何计算；
    - 一次转调最多跨 2 个五度（|Δn| ≤ 2），跨模式另加 3 的罚分；
    - 随机种子固定为 9，结果可复现。
"""

from __future__ import annotations

import heapq
import math
import random
import unicodedata

# ---------------------------------------------------------------- 常量

MAJOR_NAMES = ["C", "G", "D", "A", "E", "B", "F♯", "D♭", "A♭", "E♭", "B♭", "F"]
MINOR_NAMES = ["A", "E", "B", "F♯", "C♯", "G♯", "D♯", "B♭", "F", "C", "G", "D"]
MAJOR_STEPS = [0, 2, 4, 5, 7, 9, 11]
MINOR_STEPS = [0, 2, 3, 5, 7, 8, 10]
MODE_PENALTY = 3.0
STEP_LIMIT = 2  # 一次转调最多跨几个五度
SEED = 9
STEPS = 10000

KEYS = [(n, "M") for n in range(12)] + [(n, "m") for n in range(12)]
N = len(KEYS)
C_MAJOR = 0


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


def sharps_text(n: int) -> str:
    if n <= 6:
        return f"{n} 个升号"
    return f"{12 - n} 个降号"


# ---------------------------------------------------------------- 调与图


def tonic_of(i: int) -> int:
    n, mode = KEYS[i]
    return (7 * n) % 12 if mode == "M" else (7 * n + 9) % 12


def key_name(i: int) -> str:
    n, mode = KEYS[i]
    name = MAJOR_NAMES[n] if mode == "M" else MINOR_NAMES[n]
    return f"{name} {'大调' if mode == 'M' else '小调'}"


def scale_pcs(i: int) -> set[int]:
    _, mode = KEYS[i]
    steps = MAJOR_STEPS if mode == "M" else MINOR_STEPS
    return {(tonic_of(i) + s) % 12 for s in steps}


def circ_dist(a: int, b: int) -> int:
    d = abs(a - b) % 12
    return min(d, 12 - d)


def edge_weight(i: int, j: int):
    """返回 (边权, 调号差, 模式罚分)；不可一步转调时返回 None。"""
    d = circ_dist(KEYS[i][0], KEYS[j][0])
    mode_diff = 0 if KEYS[i][1] == KEYS[j][1] else 1
    if d > STEP_LIMIT:
        return None
    return d + MODE_PENALTY * mode_diff, d, int(MODE_PENALTY * mode_diff)


def build_graph():
    adj = [[] for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            w = edge_weight(i, j)
            if w is not None and w[0] > 0:
                adj[i].append((j, w[0]))
                adj[j].append((i, w[0]))
    return adj


def dijkstra(src: int, adj):
    dist = [float("inf")] * N
    prev = [-1] * N
    dist[src] = 0.0
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u] + 1e-12:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v] - 1e-12:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev


# ---------------------------------------------------------------- 表 1


def table_circle() -> None:
    print("表 1：五度圈的 12 个位置（位置 n 的大调主音 pc = 7n mod 12）\n")
    widths = [7, 8, 6, 11]
    aligns = ["right", "right", "left", "left"]
    print(row(["位置 n", "主音 pc", "调名", "调号"], widths, aligns))
    print("-" * 40)
    pcs = []
    for n in range(12):
        pc = (7 * n) % 12
        pcs.append(pc)
        print(row([n, pc, MAJOR_NAMES[n], sharps_text(n)], widths, aligns))
    twelve_fifths = 12 * 1200 * math.log2(1.5)
    print(f"\n  12 个位置的主音序列 = {pcs}")
    print(f"  去重后 {len(set(pcs))} 个：恰好覆盖 Z_12 的全部音级。")
    print("  因为 gcd(7,12) = 1，映射 n ↦ 7n 是 Z_12 上的置换，")
    print("  所以五度圈走 12 步就回到原点，不会提前闭合。")
    print(f"  12 个五度 = {twelve_fifths:.2f} ¢，7 个八度 = 8400 ¢，"
          f"差 {twelve_fifths - 8400:.2f} ¢（第 4 章的毕达哥拉斯音差）。")


# ---------------------------------------------------------------- 表 2


def table_dyads() -> None:
    print("\n表 2：二音和弦空间 —— 音程类、无序集合数与有序和弦数\n")
    names = ["纯一度", "小二度 / 大七度", "大二度 / 小七度", "小三度 / 大六度",
             "大三度 / 小六度", "纯四度 / 纯五度", "三全音"]
    widths = [8, 16, 12, 12]
    aligns = ["right", "right", "right", "right"]
    print(row(["音程类 d", "音程名", "无序集合数", "有序和弦数"], widths, aligns))
    print("-" * 54)
    total_unordered, total_ordered = 0, 0
    for d in range(7):
        unord = 6 if d == 6 else 12
        ordered = 12 if d in (0, 6) else 24
        total_unordered += unord
        total_ordered += ordered
        print(row([d, names[d], unord, ordered], widths, aligns))
    print(f"\n  无序二音集合共 {total_unordered} 个（= C(12,2) + 12 个同度对 = 66 + 12）。")
    print(f"  有序二音和弦共 {total_ordered} 个（= 12 × 12，含 (x,x) 的 12 个）。")
    print("  把顺序商掉（无序），144 个有序和弦折成 78 个集合；")
    print("  再把倒置 q ↦ −q 商掉，音程类只剩 0..6 这 7 类。")
    print("  连续化之后，无序二音对的空间是环面沿对角线粘合的结果 —— 一张莫比乌斯带；")
    print("  但离散计数只告诉你 7 个类，带子的「扭转」属于连续模型，不属于整数。")


# ---------------------------------------------------------------- 表 3


def table_keys(adj) -> None:
    dist, _ = dijkstra(C_MAJOR, adj)
    c_scale = scale_pcs(C_MAJOR)
    print("\n表 3：24 个大小调 —— 调号位置、与 C 大调的共同音数、最短转调代价\n")
    widths = [10, 7, 11, 9, 13]
    aligns = ["left", "right", "left", "right", "right"]
    print(row(["调", "位置", "调号", "共同音数", "到 C 大调代价"], widths, aligns))
    print("-" * 58)
    for i in range(N):
        n = KEYS[i][0]
        common = len(scale_pcs(i) & c_scale)
        cost = "—" if dist[i] == 0 else f"{dist[i]:.1f}"
        print(row([key_name(i), n, sharps_text(n), common, cost], widths, aligns))
    far = [i for i in range(N) if dist[i] > 0]
    avg = sum(dist[i] for i in far) / len(far)
    worst = max(far, key=dist.__getitem__)
    print(f"\n  从 C 大调出发，其余 23 个调的平均最短代价 = {avg:.4f}；")
    print(f"  最远的调是 {key_name(worst)}（位置 {KEYS[worst][0]}），代价 {dist[worst]:.1f}。")


# ---------------------------------------------------------------- 表 4


def path_table(src: int, dst: int, adj) -> None:
    dist, prev = dijkstra(src, adj)
    path, u = [], dst
    while u != -1:
        path.append(u)
        u = prev[u]
    path.reverse()
    direct = edge_weight(src, dst)
    direct_text = "不可一步到达" if direct is None else f"{direct[0]:.1f}"
    print(f"\n  {key_name(src)} → {key_name(dst)}：最短代价 {dist[dst]:.1f}（直连代价 {direct_text}）")
    total = 0.0
    for a, b in zip(path, path[1:]):
        w, d, pen = edge_weight(a, b)
        total += w
        common = len(scale_pcs(a) & scale_pcs(b))
        print(f"    {key_name(a)} → {key_name(b)}   调号差 {d} + 模式罚分 {pen}"
              f" = {w:.0f}   （共同音 {common}，累计 {total:.0f}）")
    print(f"  路径经过 {len(path)} 个调，{len(path) - 1} 次转调。")


# ---------------------------------------------------------------- 表 5


def table_graph(adj) -> None:
    edges = sum(len(a) for a in adj) // 2
    best = (0.0, -1, -1)
    total = 0.0
    count = 0
    for i in range(N):
        dist, _ = dijkstra(i, adj)
        for j in range(N):
            if i == j:
                continue
            total += dist[j]
            count += 1
            if dist[j] > best[0]:
                best = (dist[j], i, j)
    print("\n表 5：调性图的统计\n")
    print("  " + pad("节点数（24 个大小调）", 26) + f"= {N}")
    print("  " + pad("无向边数", 26) + f"= {edges}")
    print("  " + pad("图是否连通", 26) + f"= {'是' if best[0] < float('inf') else '否'}")
    print("  " + pad("直径（最长最短路径）", 26) + f"= {best[0]:.1f}"
          f"（{key_name(best[1])} → {key_name(best[2])}）")
    print("  " + pad("平均最短路（有向平均）", 26) + f"= {total / count:.4f}")
    print("\n  边权 = |调号位置差| + 3 × [模式不同]，且只保留 |Δn| ≤ 2 的边。")
    print("  邻接限制让绕路成为常态：直连往往更便宜，但一步最多跨两个五度。")
    return best[0]


# ---------------------------------------------------------------- 表 6

ATONAL_NOTE = 0.1  # 10 个非零步长，每个 0.1


def pi_of(P):
    pi = [1.0 / 12] * 12
    for _ in range(5000):
        new = [sum(pi[a] * P[a][b] for a in range(12)) for b in range(12)]
        if max(abs(new[i] - pi[i]) for i in range(12)) < 1e-15:
            pi = new
            break
        pi = new
    s = sum(pi)
    return [x / s for x in pi]


def entropy(p) -> float:
    h = -sum(x * math.log2(x) for x in p if x > 0)
    return 0.0 if abs(h) < 1e-12 else h


def resultant(p) -> float:
    z = sum(x * complex(math.cos(2 * math.pi * i / 12), math.sin(2 * math.pi * i / 12))
            for i, x in enumerate(p))
    return abs(z)


def atonal_matrix():
    P = [[0.0] * 12 for _ in range(12)]
    for x in range(12):
        for step in range(1, 6):
            for s in (step, -step):
                P[x][(x + s) % 12] += ATONAL_NOTE
    return P


def tonal_matrix(T=1.5):
    P = [[0.0] * 12 for _ in range(12)]
    for x in range(12):
        cands = [(x + 1) % 12, (x - 1) % 12, (x + 2) % 12, (x - 2) % 12]
        w = [math.exp(-circ_dist(y, 0) / T) for y in cands]
        s = sum(w)
        for y, wi in zip(cands, w):
            P[x][y] += wi / s
    return P


def walk(P, seed, steps):
    rng = random.Random(seed)
    x = 0
    counts = [0] * 12
    counts[x] += 1
    for _ in range(steps):
        q = P[x]
        r = rng.random()
        acc = 0.0
        nxt = 11
        for i, val in enumerate(q):
            acc += val
            if r < acc:
                nxt = i
                break
        x = nxt
        counts[x] += 1
    total = sum(counts)
    return [c / total for c in counts]


def table_walks() -> None:
    print("\n表 6：无调性与有调性随机游走（各 10000 步，种子 9）\n")
    widths = [8, 9, 9, 7, 8, 10, 12]
    aligns = ["left"] + ["right"] * 6
    print(row(["模型", "平稳熵", "模拟熵", "R", "P(C)", "平均行熵", "行熵范围"], widths, aligns))
    print("-" * 75)
    A = atonal_matrix()
    piA = pi_of(A)
    simA = walk(A, SEED, STEPS)
    row_hA = [entropy(A[x]) for x in range(12)]
    print(row(["无调性", f"{entropy(piA):.4f}", f"{entropy(simA):.4f}",
               f"{resultant(simA):.4f}", f"{simA[0]:.4f}",
               f"{sum(piA[i] * row_hA[i] for i in range(12)):.4f}",
               f"{min(row_hA):.3f}–{max(row_hA):.3f}"], widths, aligns))
    B = tonal_matrix()
    piB = pi_of(B)
    simB = walk(B, SEED, STEPS)
    row_hB = [entropy(B[x]) for x in range(12)]
    print(row(["有调性", f"{entropy(piB):.4f}", f"{entropy(simB):.4f}",
               f"{resultant(simB):.4f}", f"{simB[0]:.4f}",
               f"{sum(piB[i] * row_hB[i] for i in range(12)):.4f}",
               f"{min(row_hB):.3f}–{max(row_hB):.3f}"], widths, aligns))

    print("\n  无调性：步长在 ±1..±5 上均匀，每步一次；")
    print("  有调性：只走 ±1/±2，并带一个以 C 为中心、温度 T = 1.5 的重力井。")

    print(f"\n  无调性：平稳分布 π = 均匀（1/12 = {1 / 12:.4f}），"
          f"熵 = log2 12 = {math.log2(12):.4f} bit；")
    print(f"  每个状态的行熵都等于 log2 10 = {math.log2(10):.4f} bit，与位置无关。")
    print("  有调性的 π（按音级 0..11） =")
    for start in (0, 6):
        chunk = "  ".join(f"{piB[i]:.3f}" for i in range(start, start + 6))
        print("    " + chunk)
    print(f"  圆重心 R（解析值）= {resultant(piB):.4f}，方向指向 C：分布不再旋转对称。")
    print(f"  模拟 10000 步的圆重心：无调性 {resultant(simA):.4f}，有调性 {resultant(simB):.4f}。")
    print("  R 是「有没有中心」的度量：无调性 R ≈ 0，有调性 R > 0。")
    return entropy(piB), resultant(piB)


# ---------------------------------------------------------------- 主程序


def main() -> None:
    print("ch09_topology.py —— 第 9 章配套实验：拓扑、转调与随机游走\n")
    table_circle()
    table_dyads()
    adj = build_graph()
    table_keys(adj)
    print("\n表 4：两条最短转调路径")
    fsharp_minor = KEYS.index((3, "m"))
    bflat_minor = KEYS.index((7, "m"))
    path_table(C_MAJOR, fsharp_minor, adj)
    path_table(C_MAJOR, bflat_minor, adj)
    diameter = table_graph(adj)
    h_tonal, r_tonal = table_walks()

    print("\n关键数字：")
    print("  12 个五度 = 7 个八度 + 23.46 ¢（毕达哥拉斯音差）")
    print(f"  24 个大小调、{sum(len(a) for a in adj) // 2} 条无向边、图的直径 {diameter:.1f}")
    print(f"  无调性平稳熵 = log2 12 = {math.log2(12):.4f} bit，圆重心 R ≈ 0")
    print(f"  有调性平稳熵 = {h_tonal:.4f} bit，圆重心 R = {r_tonal:.4f}")
    print(f"  种子 = {SEED}，模拟步数 = {STEPS}")


if __name__ == "__main__":
    main()
