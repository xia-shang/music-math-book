"""
ch01_vibration.py —— 第 1 章配套实验：简谐振动、傅里叶级数与周期性

运行：
    python code/ch01_vibration.py

输出：
    表 1  方波的前 6 个非零傅里叶系数（奇次谐波，按 1/n 衰减）
    表 2  用 N 项部分和逼近方波的 RMS 误差与最大过冲
    图 1  一个周期内「理想方波 vs N=5 部分和」的 ASCII 对比
    表 3  方波、锯齿波、三角波的谐波结构
    表 4  周期信号与白噪声的自相关：周期性的数值判据

约定：基频 F = 100 Hz，周期 T = 10 ms；所有相位从 t = 0 开始。
"""

import math
import random
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

F0 = 100.0
PERIOD_MS = 1000.0 / F0
TWO_PI = 2.0 * math.pi


def disp_width(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def pad(text: str, width: int, align: str = "left") -> str:
    gap = max(0, width - disp_width(text))
    if align == "right":
        return " " * gap + text
    return text + " " * gap


# ---------------------------------------------------------------- 傅里叶系数


def square_coeff(n: int) -> float:
    """方波：奇次谐波，系数 4/(πn)。"""
    return 0.0 if n % 2 == 0 else 4.0 / (math.pi * n)


def saw_coeff(n: int) -> float:
    """锯齿波：所有谐波，系数 2/(πn)。"""
    return 2.0 / (math.pi * n)


def triangle_coeff(n: int) -> float:
    """三角波：奇次谐波，系数 8/(π²n²)。"""
    return 0.0 if n % 2 == 0 else 8.0 / (math.pi ** 2 * n * n)


def square_partial(t: float, n_max: int) -> float:
    """方波的前 n_max 项部分和；t 以周期为单位。"""
    total = 0.0
    for n in range(1, n_max + 1, 2):
        total += square_coeff(n) * math.sin(TWO_PI * n * t)
    return total


# ---------------------------------------------------------------- 各表


def table_square_coeffs() -> None:
    print("表 1：方波的前 6 个非零傅里叶系数（n 为奇数）\n")
    print(pad("n", 6, "right") + pad("系数 c_n", 14, "right")
          + pad("相对基频", 14, "right"))
    print("-" * 34)
    c1 = square_coeff(1)
    for n in (1, 3, 5, 7, 9, 11):
        c = square_coeff(n)
        print(pad(str(n), 6, "right") + pad(f"{c:.6f}", 14, "right")
              + pad(f"{c / c1:.3f}", 14, "right"))
    print("\n只出现奇次谐波；系数按 1/n 衰减，第 11 次谐波只剩基频的 9.1%。")


def table_synthesis() -> None:
    print("\n表 2：用部分和逼近方波（4096 个采样点，t 覆盖两个周期）\n")
    print(pad("最高谐波 N", 14) + pad("非零项数", 12, "right")
          + pad("RMS 误差", 14, "right") + pad("最大过冲", 12, "right"))
    print("-" * 52)
    samples = 4096
    for n_max in (1, 3, 5, 7, 9, 11):
        err_sq = 0.0
        peak = 0.0
        for k in range(samples):
            t = (k + 0.5) / samples * 2.0
            ideal = 1.0 if math.sin(TWO_PI * t) >= 0.0 else -1.0
            approx = square_partial(t, n_max)
            err_sq += (ideal - approx) ** 2
            peak = max(peak, abs(approx))
        rms = math.sqrt(err_sq / samples)
        terms = (n_max + 1) // 2
        print(pad(str(n_max), 14) + pad(str(terms), 12, "right")
              + pad(f"{rms:.4f}", 14, "right") + pad(f"{peak:.4f}", 12, "right"))
    print("\n项数越多，RMS 误差越小；但最大过冲稳定在 1.18 附近 ——")
    print("这就是吉布斯现象：方波有无限带宽，任何有限项和都消不掉尖角。")


def plot_waveform(width: int = 56, height: int = 17) -> None:
    print(f"\n图 1：一个周期内的波形（# 理想方波，. N=5 部分和，* 重合）\n")
    top, bottom = 1.4, -1.4
    grid = [[" "] * width for _ in range(height)]

    for col in range(width):
        t = (col + 0.5) / width
        ideal = 1.0 if math.sin(TWO_PI * t) >= 0.0 else -1.0
        approx = square_partial(t, 5)
        for value, ch in ((ideal, "#"), (approx, ".")):
            row = int(round((top - value) / (top - bottom) * (height - 1)))
            row = min(max(row, 0), height - 1)
            if grid[row][col] == " " or grid[row][col] == ch:
                grid[row][col] = ch
            else:
                grid[row][col] = "*"

    for row in range(height):
        value = top - row * (top - bottom) / (height - 1)
        prefix = f"{value:>5.1f} |" if row in (0, height // 2, height - 1) else "      |"
        print(prefix + "".join(grid[row]) + "|")


def table_waveforms() -> None:
    print("\n表 3：三种波形的谐波结构（系数绝对值）\n")
    print(pad("n", 5, "right") + pad("方波", 12, "right")
          + pad("锯齿波", 12, "right") + pad("三角波", 12, "right"))
    print("-" * 41)
    for n in range(1, 7):
        print(pad(str(n), 5, "right")
              + pad(f"{abs(square_coeff(n)):.4f}", 12, "right")
              + pad(f"{abs(saw_coeff(n)):.4f}", 12, "right")
              + pad(f"{abs(triangle_coeff(n)):.4f}", 12, "right"))
    print("\n方波与三角波只有奇次谐波；锯齿波有全部谐波。")
    print("衰减速度：方波 1/n，锯齿波 1/n，三角波 1/n² —— 三角波最「干净」。")


def autocorr(signal: list[float], lag: int) -> float:
    """归一化自相关：只用重叠段计算分母，避免端点长度带来的偏差。"""
    overlap = len(signal) - lag
    numerator = sum(signal[i] * signal[i + lag] for i in range(overlap))
    denominator = sum(signal[i] * signal[i] for i in range(overlap))
    return numerator / denominator


def table_autocorr() -> None:
    print("\n表 4：自相关——周期性的数值判据\n")
    period = 64
    samples = 256
    periodic = [
        math.sin(TWO_PI * k / period) + 0.5 * math.sin(2 * TWO_PI * k / period)
        for k in range(samples)
    ]
    print("  周期信号（T = 64 个采样点）：")
    print(f"    r(0)   = {autocorr(periodic, 0):+.3f}"
          f"    r(T/2) = {autocorr(periodic, period // 2):+.3f}")
    print(f"    r(T)   = {autocorr(periodic, period):+.3f}"
          f"    r(2T)  = {autocorr(periodic, 2 * period):+.3f}")

    random.seed(7)
    noise = [random.uniform(-1.0, 1.0) for _ in range(512)]
    print("\n  白噪声（512 个采样点，随机种子 7）：")
    print(f"    r(0)   = {autocorr(noise, 0):+.3f}"
          f"    r(128) = {autocorr(noise, 128):+.3f}")
    print("\n判据：r(T) ≈ 1 且在每个整数周期处重复，才是周期信号；")
    print("白噪声只在 lag = 0 处相关，其他滞后接近 0。")


def main() -> None:
    print(f"ch01_vibration.py —— 第 1 章配套实验"
          f"（基频 F = {F0:.0f} Hz，周期 T = {PERIOD_MS:.1f} ms）\n")
    table_square_coeffs()
    table_synthesis()
    plot_waveform()
    table_waveforms()
    table_autocorr()


if __name__ == "__main__":
    main()
