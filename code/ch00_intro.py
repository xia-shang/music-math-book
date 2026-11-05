"""
ch00_intro.py —— 第 0 章配套实验：音名、频率、cent 与「对数耳朵」

运行：
    python code/ch00_intro.py

输出：
    表 1  A3 ~ A5 的音名 / 频率 / 相对 A4 的音高坐标（cent）对照
    表 2  三组「同样 +10 Hz」的音程对比：听觉比较的是比值
    表 3  算术中点与几何中点：耳朵认定的「中点」是几何中点
    表 4  把连续频率离散成 12 个音级，能省掉多少信息
    表 5  三个常用比值与毕达哥拉斯音差（第 4 章伏笔）
"""

import math
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import A4, cents_of_ratio, freq_of_pitch  # noqa: E402

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def disp_width(text: str) -> int:
    """按终端显示宽度计算：全角字符占两格。"""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def pad(text: str, width: int, align: str = "left") -> str:
    """用空格补齐到指定显示宽度，保证中文表头也能对齐。"""
    gap = max(0, width - disp_width(text))
    if align == "right":
        return " " * gap + text
    return text + " " * gap


def note_name(semitones_from_a4: int) -> str:
    """以 A4 为 0，按 12-TET 的半音数给出音名。"""
    index = 9 + semitones_from_a4
    pitch_class = index % 12
    octave = 4 + index // 12
    return f"{NOTE_NAMES[pitch_class]}{octave}"


def table_notes() -> None:
    print("表 1：A3 ~ A5 的音名、频率与音高坐标（A4 = 440 Hz，12-TET）\n")
    print(pad("音名", 8) + pad("频率 (Hz)", 14, "right") + pad("相对 A4 (cent)", 20, "right"))
    print("-" * 42)
    for semis in range(-12, 13):
        f = freq_of_pitch(100.0 * semis)
        print(pad(note_name(semis), 8)
              + pad(f"{f:.3f}", 14, "right")
              + pad(f"{100.0 * semis:.1f}", 20, "right"))
    print("\n注意首尾两行：A3 与 A5 都叫 A，坐标恰好相差 2400 cent（两个八度）。")


def table_log_ear() -> None:
    print("\n表 2：同样 +10 Hz，听起来差多少？\n")
    print(pad("频率变化", 22) + pad("音程 (cent)", 14, "right"))
    print("-" * 36)
    for f0 in (220.0, 440.0, 880.0):
        c = cents_of_ratio((f0 + 10.0) / f0)
        pair = f"{f0:>7.0f} → {f0 + 10.0:<7.0f}"
        print(pad(pair, 22) + pad(f"{c:.1f}", 14, "right"))
    print("\n同样 +10 Hz，低音区接近一个半音，高音区只剩五分之一。")
    print("听觉比较的是「比值」，不是「差值」。")


def table_midpoint() -> None:
    print("\n表 3：220 Hz 与 880 Hz 的「中点」在哪里？\n")
    lo, hi = 220.0, 880.0
    arithmetic = (lo + hi) / 2.0
    geometric = math.sqrt(lo * hi)
    print(f"  算术中点 (220+880)/2       = {arithmetic:7.3f} Hz"
          f"   相对 220 Hz = {cents_of_ratio(arithmetic / lo):7.1f} cent")
    print(f"  几何中点 sqrt(220×880)     = {geometric:7.3f} Hz"
          f"   相对 220 Hz = {cents_of_ratio(geometric / lo):7.1f} cent")
    print(f"  两段音程应该相等：几何中点把 {cents_of_ratio(hi / lo):.1f} cent"
          " 平分成两个 1200 cent。")
    print(f"  算术中点偏出的 {cents_of_ratio(arithmetic / geometric):.1f} cent"
          "，就是「线性频率轴」的谎言。")


def table_entropy() -> None:
    print("\n表 4：把连续频率离散成音级，省掉多少信息？\n")
    continuum_bits = math.log2(20000 - 20 + 1)   # 20~20000 Hz，1 Hz 一格
    scale_bits = math.log2(12)                   # 12 个等概率音级
    print("  " + pad("连续频率（20~20000 Hz，1 Hz 分辨率）", 40)
          + pad(f"{continuum_bits:.2f} bit", 12, "right"))
    print("  " + pad("12 个音级（等概率）", 40)
          + pad(f"{scale_bits:.2f} bit", 12, "right"))
    print("  " + pad("压缩比", 40)
          + pad(f"{continuum_bits / scale_bits:.2f} 倍", 12, "right"))
    print("\n音阶把「无限种可能」压成「12 个可预测的标签」，这就是它好用的原因。")


def table_ratios() -> None:
    print("\n表 5：三个常用比值与毕达哥拉斯音差\n")
    values = [
        ("3:2（纯五度）", cents_of_ratio(3 / 2)),
        ("5:4（纯律大三度）", cents_of_ratio(5 / 4)),
        ("2^(1/12)（12-TET 半音）", cents_of_ratio(2.0 ** (1 / 12))),
    ]
    for label, c in values:
        print("  " + pad(label, 30) + pad(f"{c:.3f} cent", 16, "right"))
    twelve_fifths = 12 * cents_of_ratio(3 / 2)
    seven_octaves = 7 * 1200.0
    print(f"\n  12 个纯五度 = {twelve_fifths:9.3f} cent")
    print(f"  7 个纯八度  = {seven_octaves:9.3f} cent")
    print(f"  差值（毕达哥拉斯音差）= {twelve_fifths - seven_octaves:6.3f} cent")
    print("\n纯五度链走 12 步回不到原点：第 4 章要解决的就是这 23.4 cent；12-TET 的五度圈则闭合。")


def main() -> None:
    print(f"ch00_intro.py —— 导论配套实验（A4 = {A4:.0f} Hz）\n")
    table_notes()
    table_log_ear()
    table_midpoint()
    table_entropy()
    table_ratios()


if __name__ == "__main__":
    main()
