"""
ch05_scale_search.py —— 第 5 章配套实验：在 12 个音级里穷举音阶

运行：
    python code/ch05_scale_search.py

输出：
    表 1  12-TET 半音距离 d 对应的协和度 S(C4, C4·2^(d/12))
    表 2  穷举 C(12,7)=792 个七音集合（按平移去重后 66 类），给出前 5 名的得分
    表 3  三种打分口径（纯协和 / 纯均匀 / 混合）各自的冠军与取舍
    表 4  冠军音阶的 7 种调式（循环移位）与特征音程
    表 5  穷举 C(12,5)=792 个五音集合的前 5 名（附黑键五声）

约定：音级编号 C=0, C#=1, …, B=11；基准音 C4 = A4·2^(-9/12) ≈ 261.626 Hz。
协和度直接复用 common.py 的粗糙度模型（N=5 个谐波），不做任何改写。
打分对「整体平移」不变，因此 792 个集合会折叠成 66 个平移等价类。
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
MODES = ["伊奥尼亚", "多利亚", "弗里几亚", "利底亚",
         "混合利底亚", "爱奥利亚", "洛克里亚"]
MAJOR_SCALE = (0, 2, 4, 5, 7, 9, 11)


# ---------------------------------------------------------------- 表格工具


def disp_width(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def pad(text: str, width: int, align: str = "left") -> str:
    gap = max(0, width - disp_width(text))
    if align == "right":
        return " " * gap + text
    return text + " " * gap


def row(cells: list[str], widths: list[int], aligns: list[str]) -> str:
    return "  ".join(pad(t, w, a) for t, w, a in zip(cells, widths, aligns))


def note_names(notes) -> str:
    return " ".join(NAMES[n] for n in notes)


# ---------------------------------------------------------------- 协和度查表


def build_s_table() -> list[float]:
    """s_tab[d] = S(C4, C4·2^(d/12))，d = 0..12。"""
    return [consonance(C4, C4 * 2.0 ** (d / 12.0)) for d in range(13)]


def pair_s(s_tab: list[float], d: int) -> float:
    """音级距离 d 的协和度；d > 6 时按 12−d 折回（对称性）。"""
    d %= 12
    if d == 0:
        return 1.0
    return s_tab[d if d <= 6 else 12 - d]


# ---------------------------------------------------------------- 集合度量


def gaps_of(notes) -> list[int]:
    n = len(notes)
    return [(notes[(i + 1) % n] - notes[i]) % 12 for i in range(n)]


def gap_sigma(gaps: list[int]) -> float:
    mean = sum(gaps) / len(gaps)
    return math.sqrt(sum((g - mean) ** 2 for g in gaps) / len(gaps))


def triads_in(notes) -> int:
    s = set(notes)
    count = 0
    for r in notes:
        if (r + 4) % 12 in s and (r + 7) % 12 in s:
            count += 1
        if (r + 3) % 12 in s and (r + 7) % 12 in s:
            count += 1
    return count


def mean_pair_s(notes, s_tab) -> float:
    total, pairs = 0.0, 0
    for i in range(len(notes)):
        for j in range(i + 1, len(notes)):
            total += pair_s(s_tab, abs(notes[i] - notes[j]))
            pairs += 1
    return total / pairs


def metrics(notes, s_tab) -> dict:
    g = gaps_of(notes)
    s_mean = mean_pair_s(notes, s_tab)
    unif = 1.0 / (1.0 + gap_sigma(g))
    tri = triads_in(notes)
    mixed = 0.55 * s_mean + 0.25 * unif + 0.20 * (tri / 6.0)
    return {"notes": tuple(notes), "gaps": g, "s_mean": s_mean,
            "unif": unif, "tri": tri, "mixed": mixed,
            "sigma": gap_sigma(g)}


def canonical(notes) -> tuple[int, ...]:
    """12 个平移里字典序最小的那个，用作等价类代表。"""
    return min(tuple(sorted((n + t) % 12 for n in notes)) for t in range(12))


def enumerate_sets(k: int, s_tab) -> list[dict]:
    """真的穷举 C(12,k) 个集合，然后按平移等价类去重。"""
    raw = []
    for combo in itertools.combinations(range(12), k):
        m = metrics(combo, s_tab)
        m["canon"] = canonical(combo)
        raw.append(m)
    # 校验平移不变性：同一等价类内所有平移得分必须完全一致
    groups = {}
    for m in raw:
        groups.setdefault(m["canon"], []).append(m)
    worst = 0.0
    for members in groups.values():
        base = members[0]["mixed"]
        worst = max(worst, max(abs(m["mixed"] - base) for m in members))
    print(f"  穷举 {len(raw)} 个集合，折叠为 {len(groups)} 个平移等价类；"
          f"类内得分最大偏差 {worst:.2e}。")
    return [min(members, key=lambda m: m["notes"]) for members in groups.values()]


# ---------------------------------------------------------------- 各张表


def table_s(s_tab) -> None:
    print("表 1：12-TET 各级音程的协和度（基准 C4 = %.3f Hz）\n" % C4)
    widths = [9, 9, 11, 11]
    aligns = ["right"] * 4
    print(row(["距离 d", "音程 ¢", "S(C4,·)", "备注"], widths, aligns))
    print("-" * 46)
    labels = {1: "小二度", 2: "大二度", 3: "小三度", 4: "大三度",
              5: "纯四度", 6: "三全音"}
    for d in range(1, 7):
        print(row([str(d), f"{100.0 * d:.0f}", f"{s_tab[d]:.3f}", labels[d]],
                  widths, aligns))
    print("\nd > 6 用 12−d 折回：大七度读作小二度、大六度读作小三度。")
    print(f"最粗糙的是 {min(range(1,7), key=lambda d: s_tab[d]) * 100} ¢ "
          f"（S = {min(s_tab[1:7]):.3f}），不是最近的 100 ¢。")
    print("协和度不是距离的单调函数：200 ¢ 落在粗糙峰附近，100 ¢ 反而略好。")


def table_top(cands, s_tab, title) -> None:
    print(title)
    widths = [5, 28, 15, 9, 9, 8, 7, 9]
    aligns = ["right", "left", "left", "right", "right", "right", "right", "right"]
    print(row(["名次", "代表（含 C）", "半音间距", "混合", "S 均值",
               "均匀度", "三和弦", "σ 间距"], widths, aligns))
    print("-" * 92)
    top = sorted(cands, key=lambda c: c["mixed"], reverse=True)[:5]
    for i, c in enumerate(top, 1):
        print(row([str(i), note_names(c["notes"]),
                   "-".join(str(g) for g in c["gaps"]), f"{c['mixed']:.4f}",
                   f"{c['s_mean']:.4f}", f"{c['unif']:.4f}",
                   str(c["tri"]), f"{c['sigma']:.3f}"], widths, aligns))
    print("\n代表取 12 个平移里字典序最小的写法：平移不改任何音程，得分因此完全相同。")
    return top


def table_criteria(cands) -> None:
    print("\n表 3：三种打分口径的比较（同一批平移等价类）\n")
    best_s = max(cands, key=lambda c: c["s_mean"])
    best_u = max(cands, key=lambda c: c["unif"])
    best_m = max(cands, key=lambda c: c["mixed"])
    rows = [("只问协和（S 均值最高）", best_s),
            ("只问均匀（σ 最小）", best_u),
            ("协和 + 均匀 + 三和弦（本章口径）", best_m)]
    widths = [34, 26, 16, 9, 9]
    aligns = ["left", "left", "left", "right", "right"]
    print(row(["打分口径", "冠军代表", "间距", "S 均值", "三和弦"], widths, aligns))
    print("-" * 86)
    for label, c in rows:
        print(row([label, note_names(c["notes"]),
                   "-".join(str(g) for g in c["gaps"]),
                   f"{c['s_mean']:.4f}", str(c["tri"])], widths, aligns))
    print(f"\n只问协和的冠军间距型 {'-'.join(map(str, best_s['gaps']))}："
          "靠「扎堆 + 大跳」堆协和度，三和弦反而有 "
          f"{best_s['tri']} 个。")
    print(f"只问均匀的冠军 S 均值比混合冠军低 "
          f"{best_m['s_mean'] - best_u['s_mean']:.4f}，三和弦只有 {best_u['tri']} 个。")
    print(f"混合口径把两者折中：S 均值排第 "
          f"{1 + sum(1 for c in cands if c['s_mean'] > best_m['s_mean'])}"
          f"、均匀度排第 "
          f"{1 + sum(1 for c in cands if c['unif'] > best_m['unif'])}"
          f"、三和弦 {best_m['tri']} 个。")


def table_weights(cands) -> None:
    print("\n表 3b：权重灵敏度（换一组系数，冠军是否变化）\n")
    settings = [(0.55, 0.25, 0.20), (0.80, 0.10, 0.10), (0.70, 0.20, 0.10),
                (0.30, 0.50, 0.20), (0.30, 0.10, 0.60)]
    widths = [15, 28, 16, 9, 8, 8]
    aligns = ["left", "left", "left", "right", "right", "right"]
    print(row(["权重 S/U/T", "冠军代表", "间距", "得分", "S", "三和弦"],
              widths, aligns))
    print("-" * 80)
    for ws, wu, wt in settings:
        scored = [(ws * c["s_mean"] + wu * c["unif"] + wt * c["tri"] / 6.0, c)
                  for c in cands]
        total, win = max(scored, key=lambda x: x[0])
        print(row([f"{ws:.2f}/{wu:.2f}/{wt:.2f}", note_names(win["notes"]),
                   "-".join(str(g) for g in win["gaps"]), f"{total:.4f}",
                   f"{win['s_mean']:.4f}", str(win["tri"])], widths, aligns))
    print("\n协和权重 0.80 或三和弦权重 0.60 时，冠军换成 1-1-2-1-3-1-3 型；")
    print("均匀权重 0.50 时，冠军仍是 2-2-1-2-2-2-1。结论对权重敏感，但不脆弱。")


def champion_check(cands) -> None:
    champ = max(cands, key=lambda c: c["mixed"])
    print("\n冠军核对：")
    print(f"  代表写法   {note_names(champ['notes'])}"
          f"（间距 {'-'.join(map(str, champ['gaps']))}）")
    for t in range(12):
        shifted = tuple(sorted((n + t) % 12 for n in champ["notes"]))
        if shifted == MAJOR_SCALE:
            print(f"  平移到 C 大调写法：{note_names(MAJOR_SCALE)}"
                  f"（每个音 {t:+d} 个半音），间距 2-2-1-2-2-2-1。")
            break
    else:
        print("  冠军类不是 C 大调等价类。")
    print(f"  得分 {champ['mixed']:.4f} = 0.55×{champ['s_mean']:.4f} + "
          f"0.25×{champ['unif']:.4f} + 0.20×{champ['tri']}/6。")


def table_modes() -> None:
    print("\n表 4：冠军（C 大调）的 7 种调式：同一集合的循环移位\n")
    widths = [12, 28, 16, 15]
    aligns = ["left", "left", "left", "right"]
    print(row(["调式", "音级（主音起）", "半音间距", "主音→第 6 音"], widths, aligns))
    print("-" * 72)
    for r in range(7):
        rotated = tuple(MAJOR_SCALE[(r + i) % 7] for i in range(7))
        shifted = tuple((n - MAJOR_SCALE[r]) % 12 for n in rotated)
        sixth = shifted[5]
        print(row([MODES[r], note_names(rotated),
                   "-".join(str(g) for g in gaps_of(shifted)),
                   f"{100 * sixth} ¢"], widths, aligns))
    print("\n7 个调式的音级集合完全相同，只是起点不同。特征音程是第 6 音：")
    print("800 ¢（= 8 个半音，小六度）给弗里几亚 / 爱奥利亚 / 洛克里亚，")
    print("900 ¢（= 9 个半音，大六度）给伊奥尼亚 / 多利亚 / 利底亚 / 混合利底亚。")
    print("注意：同一集合的 7 个旋转不是 7 个新的音阶，而是一个对象的 7 种读法。")


def table_penta(cands5) -> None:
    print("\n表 5：五音集合（C(12,5)=792，折叠后 66 类）混合得分前 5 名\n")
    widths = [5, 24, 15, 9, 9, 8, 9]
    aligns = ["right", "left", "left", "right", "right", "right", "right"]
    print(row(["名次", "代表（含 C）", "半音间距", "混合", "S 均值",
               "均匀度", "最小间距"], widths, aligns))
    print("-" * 74)
    top = sorted(cands5, key=lambda c: c["mixed"], reverse=True)[:5]
    for i, c in enumerate(top, 1):
        print(row([str(i), note_names(c["notes"]),
                   "-".join(str(g) for g in c["gaps"]), f"{c['mixed']:.4f}",
                   f"{c['s_mean']:.4f}", f"{c['unif']:.4f}",
                   f"{min(c['gaps']) * 100} ¢"], widths, aligns))

    print("\n如果把「不含小二度」当硬约束（3.3 节：小二度最粗糙），只剩 3 类：\n")
    widths = [24, 15, 9, 9, 8]
    aligns = ["left", "left", "right", "right", "right"]
    print(row(["代表（含 C）", "半音间距", "混合", "S 均值", "三和弦"], widths, aligns))
    print("-" * 64)
    safe = sorted([c for c in cands5 if min(c["gaps"]) >= 2],
                  key=lambda c: c["mixed"], reverse=True)
    for c in safe:
        print(row([note_names(c["notes"]), "-".join(str(g) for g in c["gaps"]),
                   f"{c['mixed']:.4f}", f"{c['s_mean']:.4f}", str(c["tri"])],
                  widths, aligns))

    black_key = canonical((1, 3, 6, 8, 10))
    major_pent = canonical((0, 2, 4, 7, 9))
    black = next(c for c in safe if c["notes"] == black_key)
    major = next(c for c in safe if c["notes"] == major_pent)
    print(f"\n黑键 {note_names((1, 3, 6, 8, 10))} 与上表的 "
          f"{note_names(next(c['notes'] for c in cands5 if c['notes'] == major_pent))} "
          f"属于同一个平移等价类（整体下移 6 个半音）。")
    print(f"它的间距是 {'-'.join(str(g) for g in gaps_of((1, 3, 6, 8, 10)))}，"
          "最小间距 200 ¢ —— 这就是「黑键天然是五声音阶」的数学原因。")
    print("无约束冠军靠一个小二度换协和度，但只比 "
          f"{note_names(major['notes'])} 高 {top[0]['mixed'] - major['mixed']:.4f}：")
    print("差距小到可以忽略，于是「不含小二度」这个硬约束几乎不花成本。")
    print("七音集合则做不到：7 个点塞进 12 格，鸽笼原理保证必然出现相邻半音。")


def table_triads(cands7) -> None:
    print("\n校验：三和弦覆盖率在 66 个七音等价类上的分布\n")
    hist = {}
    for c in cands7:
        hist[c["tri"]] = hist.get(c["tri"], 0) + 1
    for tri in sorted(hist, reverse=True):
        print(f"  {tri} 个三和弦：{hist[tri]} 类")
    best = max(hist)
    print(f"\n最多 {best} 个（含大三和弦与小三和弦），共 {hist[best]} 类。")
    for c in sorted(cands7, key=lambda c: c["mixed"], reverse=True):
        if c["tri"] == best:
            print(f"  三和弦最多的一类：{note_names(c['notes'])}，间距 "
                  f"{'-'.join(str(g) for g in c['gaps'])}，混合得分 {c['mixed']:.4f}。")
    six = [c for c in cands7 if c["tri"] == 6]
    print(f"\n三和弦 6 个的类有 {len(six)} 个；它们的间距型与最大间隙：")
    for c in six:
        print(f"  {note_names(c['notes'])}：{'-'.join(str(g) for g in c['gaps'])}"
              f"（最大间隙 {max(c['gaps'])}）")
    even = [c for c in cands7 if max(c["gaps"]) <= 2]
    print(f"\n最大间隙 ≤ 2 的类有 {len(even)} 个（这是最均匀的一族），三和弦覆盖：")
    for c in even:
        print(f"  {note_names(c['notes'])}：{c['tri']} 个三和弦，"
              f"间距 {'-'.join(str(g) for g in c['gaps'])}")
    print("最均匀一族里，只有 2-2-1-2-2-2-1 拿到 6 个三和弦；其余两类只有 4 个和 2 个。")


def main() -> None:
    print("ch05_scale_search.py —— 第 5 章配套实验：在 12 个音级里穷举音阶\n")
    s_tab = build_s_table()
    table_s(s_tab)

    print("\n七音集合：")
    cands7 = enumerate_sets(7, s_tab)
    table_top(cands7, s_tab, "\n表 2：七音集合混合得分前 5 名\n")
    champion_check(cands7)
    table_criteria(cands7)
    table_weights(cands7)
    table_modes()
    table_triads(cands7)

    print("\n五音集合：")
    cands5 = enumerate_sets(5, s_tab)
    table_penta(cands5)

    champ = max(cands7, key=lambda c: c["mixed"])
    print("\n关键数字：")
    print(f"  S(纯五度 700 ¢)  = {pair_s(s_tab, 7):.4f}")
    print(f"  S(小二度 100 ¢)  = {pair_s(s_tab, 1):.4f}")
    print(f"  S(大二度 200 ¢)  = {pair_s(s_tab, 2):.4f}")
    print(f"  冠军混合得分     = {champ['mixed']:.4f}"
          f"（S {champ['s_mean']:.4f} + 均匀 {champ['unif']:.4f} + 三和弦 {champ['tri']}）")


if __name__ == "__main__":
    main()
