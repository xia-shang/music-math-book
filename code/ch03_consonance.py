"""
ch03_consonance.py —— 第三章配套实验：把「协和」算成一个数

运行：
    python code/ch03_consonance.py

输出：
    1) 十三个音程的粗糙度 D 与协和度 S（纯律 vs 12-TET）
    2) 0~1200 cent 扫描曲线上的局部极小值（即模型认为最协和的音程）
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    consonance,
    dissonance,
    interval_ratios,
    ratio_of_cents,
)

BASE = 330.0  # E4：这个音高下粗糙度曲线最清晰（见 3.4 节）


def table() -> None:
    print(f"基频 f1 = {BASE:.0f} Hz，谐波数 5，振幅 a_k = 1/k\n")
    print(f"{'音程':<7}{'纯律比':>9}{'纯律 D':>9}{'纯律 S':>9}{'12-TET S':>10}{'S 差':>8}")
    print("-" * 52)
    for name, just, tet, _semis in interval_ratios():
        dj = dissonance(BASE, BASE * just)
        sj = consonance(BASE, BASE * just)
        st = consonance(BASE, BASE * tet)
        print(f"{name:<7}{just:>9.4f}{dj:>9.3f}{sj:>9.3f}{st:>10.3f}{sj - st:>+8.3f}")


def curve(step_cents: float = 2.0) -> None:
    """扫描 0~1200 cent，找出粗糙度曲线的局部极小值。"""
    values = []
    c = 0.0
    while c <= 1200.0:
        values.append((c, dissonance(BASE, BASE * ratio_of_cents(c))))
        c += step_cents

    print("\n粗糙度曲线的局部极小值（越深越协和）：")
    for i in range(1, len(values) - 1):
        if values[i][1] < values[i - 1][1] and values[i][1] < values[i + 1][1]:
            c, d = values[i]
            print(f"  {c:7.1f} ¢   D = {d:.4f}   S = {1 / (1 + d):.3f}")


if __name__ == "__main__":
    table()
    curve()
