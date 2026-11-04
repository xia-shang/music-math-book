"""
common.py —— 《音乐的数理逻辑》公共数值工具

全书所有实验脚本都从这里导入，保证使用同一套参数。
只依赖 Python 标准库。

约定：
- 频率单位 Hz；音高坐标单位 cent（1 个八度 = 1200 ¢）。
- 参考频率 A4 = 440 Hz，参考音高 p = 0 ¢。
"""

from __future__ import annotations

import math

A4 = 440.0

# ---------------------------------------------------------------- 频率 / 音高


def cents_of_ratio(ratio: float) -> float:
    """把频率比翻译成音程（cent）。"""
    return 1200.0 * math.log2(ratio)


def ratio_of_cents(cents: float) -> float:
    """把音程（cent）翻译回频率比。"""
    return 2.0 ** (cents / 1200.0)


def pitch_of_freq(f: float, f_ref: float = A4) -> float:
    """频率 -> 音高坐标（相对 f_ref）。"""
    return cents_of_ratio(f / f_ref)


def freq_of_pitch(p: float, f_ref: float = A4) -> float:
    """音高坐标 -> 频率。"""
    return f_ref * ratio_of_cents(p)


def hz_to_cents(f1: float, f2: float) -> float:
    """两个频率之间的音程。"""
    return cents_of_ratio(f2 / f1)


# ---------------------------------------------------------------- 听觉模型

KERNEL_PEAK = 0.25  # 粗糙度核的峰值位置：Δf = 0.25 · CB
PARTIALS = 5  # 参与计算的谐波个数


def critical_band(f: float) -> float:
    """临界带宽 CB(f)，Zwicker 近似，单位 Hz。

        CB(f) ≈ 94 + 71.3 · (f / 1 kHz)^0.69

    注意：这是对听生理实验数据的拟合公式，属于本书的「公设」，不是推导结果。
    """
    return 94.0 + 71.3 * (max(f, 1.0) / 1000.0) ** 0.69


def roughness_kernel(df: float, bw: float) -> float:
    """单个谐波对的粗糙度贡献 W(Δf)。

    形状：W(x) = x² · exp(1 − x²)，其中 x = Δf / (0.25 · CB)。

    - Δf → 0    : W → 0（同频只改变音量，不产生粗糙）
    - Δf = 0.25·CB : W = 1（最粗糙）
    - Δf ≫ CB   : W → 0（两音已被听觉系统分开）
    """
    x = abs(df) / (KERNEL_PEAK * bw)
    if x == 0.0:
        return 0.0
    return x * x * math.exp(1.0 - x * x)


def dissonance(f1: float, f2: float, partials: int = PARTIALS) -> float:
    """两音的总不协和度 D（正值，越大越粗糙）。

    D = Σ_i Σ_j a_i a_j · W(f_i − f_j),  a_k = 1/k

    不做归一化：D 的绝对值就是「单位粗糙度」的总和，
    因此不同音区、不同谐波数都可以直接比较。
    """
    total = 0.0
    for i in range(1, partials + 1):
        for j in range(1, partials + 1):
            fi, fj = i * f1, j * f2
            total += (1.0 / i) * (1.0 / j) * roughness_kernel(
                fi - fj, critical_band(min(fi, fj))
            )
    return total


def consonance(f1: float, f2: float, partials: int = PARTIALS) -> float:
    """协和度评分 S = 1 / (1 + D)，落在 (0, 1]。"""
    return 1.0 / (1.0 + dissonance(f1, f2, partials))


# ---------------------------------------------------------------- 音程表

# (名称, 纯律分子, 纯律分母, 12-TET 半音数)
INTERVALS = [
    ("纯一度", 1, 1, 0),
    ("小二度", 16, 15, 1),
    ("大二度", 9, 8, 2),
    ("小三度", 6, 5, 3),
    ("大三度", 5, 4, 4),
    ("纯四度", 4, 3, 5),
    ("三全音", 45, 32, 6),
    ("纯五度", 3, 2, 7),
    ("小六度", 8, 5, 8),
    ("大六度", 5, 3, 9),
    ("小七度", 16, 9, 10),
    ("大七度", 15, 8, 11),
    ("纯八度", 2, 1, 12),
]


def interval_ratios():
    """返回 [(名称, 纯律比值, 12-TET 比值, 半音数)]。"""
    out = []
    for name, num, den, semis in INTERVALS:
        out.append((name, num / den, ratio_of_cents(100.0 * semis), semis))
    return out


def tet_ratios(n: int = 12) -> list[float]:
    """n 平均律的各级频率比（不含 1.0）。"""
    return [ratio_of_cents(1200.0 * k / n) for k in range(n)]


# ---------------------------------------------------------------- 律制

def pythagorean_major_ratios() -> list[float]:
    """五度相生律自然大调 C-D-E-F-G-A-B 的频率比。"""
    return [1 / 1, 9 / 8, 81 / 64, 4 / 3, 3 / 2, 27 / 16, 243 / 128]


def just_major_ratios() -> list[float]:
    """纯律自然大调（C 为主音）的频率比。"""
    return [1 / 1, 9 / 8, 5 / 4, 4 / 3, 3 / 2, 5 / 3, 15 / 8]


def deviations(ratios: list[float]) -> list[float]:
    """一组音阶各级相对 12-TET 的偏差（cent）。"""
    return [cents_of_ratio(r) - 100.0 * i for i, r in enumerate(ratios)]
