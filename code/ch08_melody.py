"""
ch08_melody.py —— 第 8 章配套实验：旋律的马尔可夫链与信息论

运行：
    python code/ch08_melody.py

输出：
    表 1  12 小节语料（每小节 4 个音，C 大调自然音级）
    表 2  一阶转移计数矩阵 7×7
    表 3  一阶转移概率矩阵（行归一化）
    表 4  边际熵、一阶条件熵、Hmax 与冗余度（含 Miller–Madow 修正）
    表 5  二阶上下文：观察到多少种、高频上下文的后继分布
    表 6  留出检验：前 6 小节训练、后 6 小节预测的交叉熵与命中率
    表 7  香农猜谜：平均名次、log2 名次与命中率
    表 8  温度参数：熵与惊讶度的权衡
    表 9  生成 8 小节旋律与每步惊讶度

约定：
    - 音级用 0..6 表示 C D E F G A B（C 大调自然音级），状态空间大小 K = 7；
    - 所有对数以 2 为底，单位 bit；
    - 随机种子固定为 8，结果可复现；
    - 只用标准库（math、random）。
"""

from __future__ import annotations

import math
import random
import unicodedata

# ---------------------------------------------------------------- 语料

NOTE = ["C", "D", "E", "F", "G", "A", "B"]
K = len(NOTE)
# 七个音级在 12-TET 里的音级坐标（半音，相对 C）。
PC = [0, 2, 4, 5, 7, 9, 11]

# 12 小节，每小节 4 个音（四分音符），共 48 个音级。
CORPUS = [
    [0, 1, 2, 3],
    [4, 5, 4, 2],
    [3, 1, 2, 0],
    [1, 2, 3, 4],
    [5, 4, 3, 2],
    [1, 2, 0, 1],
    [2, 3, 4, 5],
    [6, 4, 5, 3],
    [2, 0, 1, 2],
    [3, 4, 2, 0],
    [1, 3, 2, 1],
    [0, 1, 2, 4],
]

SEED = 8
H1 = 0.0  # 由 table_entropy() 填入


def flatten(bars):
    return [x for bar in bars for x in bar]


SEQ = flatten(CORPUS)


def pairs(seq):
    return list(zip(seq, seq[1:]))


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


# ---------------------------------------------------------------- 熵工具


def entropy(probs) -> float:
    """香农熵 H = −Σ p log2 p（bit）。"""
    h = -sum(p * math.log2(p) for p in probs if p > 0.0)
    return 0.0 if abs(h) < 1e-12 else h


def surprise(p: float) -> float:
    """惊讶度 −log2 p；p = 1 时返回 0，避免出现 −0.0000。"""
    s = -math.log2(p) if p > 0 else float("inf")
    return 0.0 if abs(s) < 1e-12 else s


def count_matrix(seq):
    C = [[0] * K for _ in range(K)]
    for a, b in pairs(seq):
        C[a][b] += 1
    return C


def row_probs(C):
    out = []
    for a in range(K):
        n = sum(C[a])
        out.append([c / n if n else 0.0 for c in C[a]])
    return out


def marginal_counts(seq):
    m = [0] * K
    for x in seq:
        m[x] += 1
    return m


# ---------------------------------------------------------------- 表 1


def table_corpus() -> None:
    print("表 1：语料 —— 12 小节、每小节 4 个音（C 大调自然音级）\n")
    widths = [6, 12, 14, 12]
    aligns = ["left", "left", "left", "left"]
    print(row(["小节", "音符", "音级坐标", "半音音程"], widths, aligns))
    print("-" * 52)
    for i, bar in enumerate(CORPUS, start=1):
        notes = "  ".join(NOTE[x] for x in bar)
        pcs = " ".join(f"{PC[x]:>2}" for x in bar)
        diffs = " ".join(f"{PC[bar[j + 1]] - PC[bar[j]]:+d}" for j in range(3))
        print(row([i, notes, pcs, diffs], widths, aligns))
    ups = sum(1 for a, b in pairs(SEQ) if PC[b] > PC[a])
    downs = sum(1 for a, b in pairs(SEQ) if PC[b] < PC[a])
    same = sum(1 for a, b in pairs(SEQ) if PC[b] == PC[a])
    steps = sum(1 for a, b in pairs(SEQ) if abs(PC[b] - PC[a]) <= 2)
    print(f"\n  48 个音，47 个相邻音程（半音）：上升 {ups} 次、下降 {downs} 次、重复 {same} 次；")
    print(f"  其中级进（半音差 ≤ 2）{steps} 次，占 {steps / 47:.4f}。")
    print("  语料是手写的固定文本，不含随机成分：每次运行得到同一组数字。")


# ---------------------------------------------------------------- 表 2、表 3


def table_counts(C) -> None:
    print("\n表 2：一阶转移计数矩阵（行 = 前一个音，列 = 后一个音）\n")
    widths = [8] + [5] * K + [7]
    aligns = ["left"] + ["right"] * (K + 1)
    print(row(["从\\到"] + NOTE + ["合计"], widths, aligns))
    print("-" * 66)
    for a in range(K):
        print(row([NOTE[a]] + C[a] + [sum(C[a])], widths, aligns))
    print(f"\n  全部计数相加 = {sum(sum(r) for r in C)}，与 48 − 1 = 47 一致。")
    zero_rows = [NOTE[a] for a in range(K) if sum(C[a]) == 0]
    if zero_rows:
        print("  没有出边的状态：" + "、".join(zero_rows))
    else:
        print("  七个音级都至少有一次作为前驱，没有「死路」状态。")


def table_probs(P) -> None:
    print("\n表 3：一阶转移概率矩阵 p(后一个 | 前一个)，每行和为 1\n")
    widths = [8] + [6] * K + [7]
    aligns = ["left"] + ["right"] * (K + 1)
    print(row(["从\\到"] + NOTE + ["行和"], widths, aligns))
    print("-" * 73)
    for a in range(K):
        print(row([NOTE[a]] + [f"{x:.3f}" for x in P[a]] + [f"{sum(P[a]):.3f}"],
                  widths, aligns))
    print("\n  行内最大的概率就是这一步「最可能被猜中」的音；")
    print("  概率 0 表示语料里从未出现过的接续，模型不会生成它们。")


# ---------------------------------------------------------------- 表 4


def table_entropy(C, P) -> None:
    global H1
    m = marginal_counts(SEQ)
    N = len(SEQ)
    MARG_P = [c / N for c in m]

    print("\n表 4：边际熵、条件熵、上界与冗余度\n")
    print("  " + pad("音符总数 N", 24) + f"= {N}")
    print("  " + pad("转移对数 N − 1", 24) + f"= {N - 1}")
    print("  " + pad("边际分布 p(x)", 24) + "= " +
          "  ".join(f"{NOTE[i]} {MARG_P[i]:.4f}" for i in range(4)))
    print("  " + " " * 24 + "  " +
          "  ".join(f"{NOTE[i]} {MARG_P[i]:.4f}" for i in range(4, K)))
    print("  " + pad("边际熵 H(X)", 24) + f"= {entropy(MARG_P):.4f} bit")
    H1 = 0.0
    for a in range(K):
        n = sum(C[a])
        if n:
            H1 += (n / (N - 1)) * entropy(P[a])
    print("  " + pad("一阶条件熵 H(X|前驱)", 24) + f"= {H1:.4f} bit")
    print("  " + pad(f"上界 Hmax = log2 {K}", 24) + f"= {math.log2(K):.4f} bit")
    print("  " + pad("冗余度 1 − H1/Hmax", 24) + f"= {1.0 - H1 / math.log2(K):.4f}")
    print("  " + pad("冗余度 1 − H(X)/Hmax", 24) + f"= {1.0 - entropy(MARG_P) / math.log2(K):.4f}")
    nonzero = sum(1 for a in range(K) for b in range(K) if C[a][b] > 0)
    mm1 = H1 + (nonzero - 1) / (2 * (N - 1) * math.log(2))
    mm0 = entropy(MARG_P) + (K - 1) / (2 * N * math.log(2))
    print("\n  直接代入频率的估计有系统性低估（样本少时尤其明显），")
    print("  Miller–Madow 修正 H + (m−1)/(2N ln 2)：")
    print(f"    H1 修正后 = {mm1:.4f} bit（m = {nonzero} 个非零格）")
    print(f"    H(X) 修正后 = {mm0:.4f} bit（m = {K} 个非零格）")
    print(f"  一阶链把熵从边际的 {entropy(MARG_P):.4f} bit 压低到 {H1:.4f} bit："
          "差额就是「语境带来的可预测性」。")


# ---------------------------------------------------------------- 表 5：二阶上下文


def table_second_order(seq) -> None:
    ctx = {}
    total = 0
    for i in range(2, len(seq)):
        key = (seq[i - 2], seq[i - 1])
        total += 1
        slot = ctx.setdefault(key, {})
        slot[seq[i]] = slot.get(seq[i], 0) + 1
    H2 = 0.0
    for key, succ in ctx.items():
        n = sum(succ.values())
        p = [succ.get(b, 0) / n for b in range(K)]
        H2 += (n / total) * entropy(p)
    print("\n表 5：二阶上下文（上下文 = 前两个音，共 7×7 = 49 种可能）\n")
    print(f"  二阶转移总数              = {total}")
    print(f"  观察到的上下文数          = {len(ctx)} / {K * K}")
    print(f"  二阶条件熵 H(X|前两个音)  = {H2:.4f} bit（直接代入频率，见下）")
    print(f"  与一阶条件熵之差          = {H1 - H2:.4f} bit")
    print("\n  出现次数最多的 8 个上下文：\n")
    widths = [10, 6, 34, 10]
    aligns = ["left", "right", "left", "right"]
    print(row(["上下文", "次数", "后继分布（音:计数）", "条件熵"], widths, aligns))
    print("-" * 66)
    top = sorted(ctx.items(), key=lambda kv: (-sum(kv[1].values()), kv[0]))
    for (a, b), succ in top[:8]:
        n = sum(succ.values())
        dist = " ".join(f"{NOTE[c]}:{succ[c]}" for c in sorted(succ))
        p = [succ.get(c, 0) / n for c in range(K)]
        print(row([f"{NOTE[a]}→{NOTE[b]}", n, dist, f"{entropy(p):.3f}"], widths, aligns))
    print("\n  49 种上下文只观察到 %d 种，其余从没出现过 —— 这正是二阶模型的麻烦：" % len(ctx))
    print("  参数个数是 7×7×6 = 294，而语料只有 46 个二阶样本。")
    return H2


# ---------------------------------------------------------------- 表 6：留出检验


def _smoothed(counts, n, alpha=1.0):
    denom = n + alpha * K
    return [(counts.get(x, 0) + alpha) / denom for x in range(K)]


def _model_probs(hist, uni_counts, uni_n, bi_counts, tri_counts, order):
    """按 order 阶模型给出下一个音的概率向量，带拉普拉斯平滑与回退。"""
    if order >= 2 and len(hist) >= 2:
        key = (hist[-2], hist[-1])
        if key in tri_counts:
            return _smoothed(tri_counts[key], sum(tri_counts[key].values()))
    if order >= 1 and hist:
        key = (hist[-1],)
        if key in bi_counts:
            return _smoothed(bi_counts[key], sum(bi_counts[key].values()))
    return _smoothed(uni_counts, uni_n)


def table_holdout(seq) -> None:
    split = 24  # 前 6 小节 = 24 个音
    train, test = seq[:split], seq[split:]
    uni_counts = {x: 0 for x in range(K)}
    for x in train:
        uni_counts[x] += 1
    bi_counts, tri_counts = {}, {}
    for i in range(1, len(train)):
        key = (train[i - 1],)
        slot = bi_counts.setdefault(key, {})
        slot[train[i]] = slot.get(train[i], 0) + 1
    for i in range(2, len(train)):
        key = (train[i - 2], train[i - 1])
        slot = tri_counts.setdefault(key, {})
        slot[train[i]] = slot.get(train[i], 0) + 1

    print("\n表 6：留出检验 —— 用第 1~6 小节训练，预测第 7~12 小节的 24 个音")
    print("（拉普拉斯平滑 α = 1；二阶模型遇到没见过的上下文时退回一阶）\n")
    widths = [14, 12, 10, 14]
    aligns = ["left", "right", "right", "left"]
    print(row(["模型", "交叉熵(bit/音)", "命中率", "猜中次数"], widths, aligns))
    print("-" * 56)
    for order, name in ((0, "0 阶（边际）"), (1, "1 阶"), (2, "2 阶")):
        loss = 0.0
        hit = 0
        for t in range(split, len(seq)):
            hist = seq[max(0, t - 2):t]
            p = _model_probs(hist, uni_counts, len(train), bi_counts, tri_counts, order)
            loss += -math.log2(p[seq[t]])
            if max(range(K), key=lambda b: (p[b], -b)) == seq[t]:
                hit += 1
        print(row([name, f"{loss / len(test):.4f}", f"{hit / len(test):.4f}", f"{hit}/{len(test)}"],
                  widths, aligns))
    print("\n  训练集只有 24 个音：2 阶模型的 49 个上下文里绝大多数没见过，")
    print("  它在测试集上的交叉熵反而最差。样本越少，阶数越高越危险。")


# ---------------------------------------------------------------- 表 7：猜谜


def table_guessing(C, P) -> None:
    ranks = []
    for a, b in pairs(SEQ):
        order = sorted(range(K), key=lambda c: (-C[a][c], c))
        ranks.append(order.index(b) + 1)
    avg_rank = sum(ranks) / len(ranks)
    avg_log = sum(math.log2(r) for r in ranks) / len(ranks)
    hits = [sum(1 for r in ranks if r <= m) / len(ranks) for m in (1, 2, 3)]
    surprises = [-math.log2(P[a][b]) for a, b in pairs(SEQ)]
    avg_surprise = sum(surprises) / len(surprises)
    print("\n表 7：香农猜谜 —— 按出现频率从高到低猜下一个音\n")
    print(f"  转移总数                    = {len(ranks)}")
    print(f"  平均名次 E[rank]            = {avg_rank:.4f}")
    print(f"  平均 log2 名次 E[log2 rank] = {avg_log:.4f} bit")
    print(f"  平均惊讶度 E[−log2 p]       = {avg_surprise:.4f} bit（等于表 4 的一阶条件熵）")
    print(f"  第 1 名命中率               = {hits[0]:.4f}（{sum(1 for r in ranks if r == 1)}/{len(ranks)}）")
    print(f"  前 2 名命中率               = {hits[1]:.4f}（{sum(1 for r in ranks if r <= 2)}/{len(ranks)}）")
    print(f"  前 3 名命中率               = {hits[2]:.4f}（{sum(1 for r in ranks if r <= 3)}/{len(ranks)}）")
    print(f"  名次分布                    = " +
          "  ".join(f"{m}:{sum(1 for r in ranks if r == m)}" for m in range(1, K + 1)))
    print("\n  平均惊讶度 %.4f bit 不小于平均 log2 名次 %.4f bit：这就是定理 8.4 的数值影子。" % (avg_surprise, avg_log))


# ---------------------------------------------------------------- 表 8：温度


def tempered(P, temperature):
    out = []
    for a in range(K):
        w = [p ** (1.0 / temperature) for p in P[a]]
        s = sum(w)
        out.append([x / s for x in w])
    return out


def generate(P, seed, bars=8, temperature=1.0, start=0):
    rng = random.Random(seed)
    Q = tempered(P, temperature)
    seq, steps = [start], []
    for _ in range(bars * 4 - 1):
        prev = seq[-1]
        q = Q[prev]
        r = rng.random()
        acc, nxt = 0.0, K - 1
        for idx, x in enumerate(q):
            acc += x
            if r < acc:
                nxt = idx
                break
        steps.append((prev, nxt, q[nxt]))
        seq.append(nxt)
    return seq, steps


def stationary(P):
    """马尔可夫链的平稳分布：π = πP，用幂迭代求，归一化后返回。"""
    pi = [1.0 / K] * K
    for _ in range(5000):
        new = [sum(pi[a] * P[a][b] for a in range(K)) for b in range(K)]
        if max(abs(new[i] - pi[i]) for i in range(K)) < 1e-15:
            pi = new
            break
        pi = new
    total = sum(pi)
    return [x / total for x in pi]


def table_temperature(P) -> None:
    print("\n表 8：温度 T 与「意外—可预测」的权衡（种子 8，生成 32 个音）\n")
    widths = [5, 11, 11, 8, 9]
    aligns = ["right"] * 5
    print(row(["T", "期望惊讶度", "生成惊讶度", "音级种数", "平均音程"], widths, aligns))
    print("-" * 52)
    for T in (0.5, 1.0, 2.0):
        Q = tempered(P, T)
        expected = sum(p * entropy(Q[a]) for a, p in enumerate(stationary(Q)))
        seqT, stepsT = generate(P, SEED, temperature=T)
        emp = sum(surprise(p) for _, _, p in stepsT) / len(stepsT)
        used = len({x for x in seqT})
        leaps = sum(abs(PC[b] - PC[a]) for a, b in pairs(seqT)) / (len(seqT) - 1)
        print(row([f"{T:.1f}", f"{expected:.4f}", f"{emp:.4f}", used, f"{leaps:.3f}"],
                  widths, aligns))
    pi = stationary(tempered(P, 1.0))
    print("\n  " + pad("T = 1.0 链的平稳分布 π", 24) + "= " +
          "  ".join(f"{NOTE[i]} {pi[i]:.3f}" for i in range(4)))
    print("  " + " " * 24 + "  " +
          "  ".join(f"{NOTE[i]} {pi[i]:.3f}" for i in range(4, K)))
    print("  期望惊讶度 = Σ π_i H(第 i 行)，单位 bit，是把 −log2 p 对平稳分布取期望；")
    print("  生成惊讶度是 32 个音的经验均值，样本小，±0.2 bit 的波动很正常；")
    print("  平均音程的单位是半音（12-TET）。")
    print("  T 变小：分布变尖，期望惊讶度下降，旋律更「可预测」；")
    print("  T 变大：分布变平，期望惊讶度上升，但很快接近均匀乱走（上界 log2 7 = 2.8074）。")


# ---------------------------------------------------------------- 表 9：生成旋律


def table_generated(P) -> None:
    seq, steps = generate(P, SEED, temperature=1.0)
    print("\n表 9：生成旋律（T = 1.0，种子 8，8 小节 32 个音）\n")
    print("  小节旋律：")
    for b in range(8):
        bar = seq[b * 4:(b + 1) * 4]
        print(f"    {b + 1}   " + "  ".join(NOTE[x] for x in bar))
    print()
    widths = [4, 5, 5, 5, 12, 11]
    aligns = ["right", "right", "left", "left", "right", "right"]
    print(row(["步", "小节", "音", "前驱", "p(音|前驱)", "惊讶度(bit)"], widths, aligns))
    print("-" * 52)
    for i, (prev, nxt, p) in enumerate(steps, start=1):
        print(row([i, (i - 1) // 4 + 1, NOTE[nxt], NOTE[prev], f"{p:.4f}",
                   f"{surprise(p):.4f}"], widths, aligns))
    print("-" * 52)
    total = sum(surprise(p) for _, _, p in steps)
    print(f"  总惊讶度 = {total:.4f} bit，平均 = {total / len(steps):.4f} bit/音")
    print(f"  出现的音级 = {len(set(seq))} 种：" + "、".join(NOTE[x] for x in sorted(set(seq))))
    leaps = sum(abs(PC[b] - PC[a]) for a, b in pairs(seq))
    print(f"  半音音程绝对值之和 = {leaps} 个半音，平均 {leaps / (len(seq) - 1):.3f} 半音")
    return seq, total


# ---------------------------------------------------------------- 主程序


def main() -> None:
    print("ch08_melody.py —— 第 8 章配套实验：旋律的统计与信息\n")
    table_corpus()
    C = count_matrix(SEQ)
    P = row_probs(C)
    table_counts(C)
    table_probs(P)
    table_entropy(C, P)
    table_second_order(SEQ)
    table_holdout(SEQ)
    table_guessing(C, P)
    table_temperature(P)
    seq, total = table_generated(P)

    print("\n关键数字：")
    print("  " + pad("语料长度", 26) + f"= {len(SEQ)}（12 小节 × 4）")
    print("  " + pad("转移对数", 26) + f"= {len(SEQ) - 1}")
    print("  " + pad("一阶条件熵 H1", 26) + f"= {H1:.4f} bit")
    print("  " + pad("上界 Hmax", 26) + f"= {math.log2(K):.4f} bit")
    print("  " + pad("冗余度 1 − H1/Hmax", 26) + f"= {1.0 - H1 / math.log2(K):.4f}")
    print("  " + pad("生成 32 个音的总惊讶度", 26) + f"= {total:.4f} bit")
    print("  " + pad("随机种子", 26) + f"= {SEED}")


if __name__ == "__main__":
    main()
