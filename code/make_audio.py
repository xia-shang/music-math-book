"""
make_audio.py —— 生成书中可试听的对照音频（WAV）

运行：
    python code/make_audio.py

输出目录：
    docs/public/audio/

设计：
- 采样率 22050 Hz、单声道、16 bit，每个文件约 1.8 秒，体积 ~80 KB；
- 音色统一为 6 个谐波、振幅 1/k（接近弦乐/钢琴的衰减谱）；
- 统一使用 C4 = 261.626 Hz 为根音，方便 A/B 对比；
- 所有文件都做 40 ms 淡入 / 250 ms 淡出，避免爆音；
- 纯标准库（wave + struct + math），不依赖任何音频库。

用法：改参数后重新运行即可；脚本会打印每个文件的时长、峰值与体积。
"""

from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

SR = 22050
DUR = 1.8
PARTIALS = 6
C4 = 261.6255653005986

OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "public" / "audio"

# 12-TET 的两个常用音程
TET_M3 = 2 ** (4 / 12)
TET_P5 = 2 ** (7 / 12)


def synth(tones: list[tuple[float, float]]) -> list[float]:
    """把若干个 (频率, 振幅) 叠加成一段波形。"""
    n = int(SR * DUR)
    buf = [0.0] * n
    for freq, amp in tones:
        for k in range(1, PARTIALS + 1):
            fk = freq * k
            if fk >= SR / 2:
                break
            level = amp / k
            step = 2 * math.pi * fk / SR
            for i in range(n):
                buf[i] += level * math.sin(step * i)
    return buf


def envelope(buf: list[float]) -> None:
    """原地施加淡入淡出，防止起止爆音。"""
    n = len(buf)
    na = int(0.04 * SR)
    nr = int(0.25 * SR)
    for i in range(na):
        buf[i] *= i / na
    for i in range(nr):
        buf[n - 1 - i] *= i / nr


def normalize(buf: list[float], peak: float = 0.85) -> None:
    m = max(abs(x) for x in buf) or 1.0
    scale = peak / m
    for i in range(len(buf)):
        buf[i] *= scale


def write_wav(name: str, buf: list[float]) -> tuple[str, float, int]:
    path = OUT_DIR / name
    frames = struct.pack("<%dh" % len(buf), *(int(max(-1.0, min(1.0, x)) * 32767) for x in buf))
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(frames)
    rms = math.sqrt(sum(x * x for x in buf) / len(buf))
    return name, rms, path.stat().st_size


def build(name: str, tones: list[tuple[float, float]]) -> None:
    buf = synth(tones)
    envelope(buf)
    normalize(buf)
    write_wav(name, buf)


def noise(name: str) -> None:
    """白噪声：与乐音对照用。"""
    import random

    random.seed(2013)
    n = int(SR * DUR)
    buf = [random.uniform(-1.0, 1.0) for _ in range(n)]
    envelope(buf)
    normalize(buf, 0.7)
    write_wav(name, buf)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pairs = [
        ("fifth-just.wav", [(C4, 0.5), (C4 * 3 / 2, 0.5)]),
        ("fifth-tet.wav", [(C4, 0.5), (C4 * TET_P5, 0.5)]),
        ("third-just.wav", [(C4, 0.5), (C4 * 5 / 4, 0.5)]),
        ("third-tet.wav", [(C4, 0.5), (C4 * TET_M3, 0.5)]),
        ("chord-just.wav", [(C4, 0.4), (C4 * 5 / 4, 0.4), (C4 * 3 / 2, 0.4)]),
        ("chord-tet.wav", [(C4, 0.4), (C4 * TET_M3, 0.4), (C4 * TET_P5, 0.4)]),
    ]
    rows = []
    for name, tones in pairs:
        build(name, tones)
        path = OUT_DIR / name
        rows.append((name, DUR, path.stat().st_size))

    # 乐音 vs 噪声
    build("tone-440.wav", [(440.0, 0.8)])
    noise("noise.wav")
    for name in ("tone-440.wav", "noise.wav"):
        path = OUT_DIR / name
        rows.append((name, DUR, path.stat().st_size))

    print(f"输出目录：{OUT_DIR}")
    print(f"{'文件':<20}{'时长(s)':>8}{'体积(KB)':>10}")
    print("-" * 40)
    for name, dur, size in rows:
        print(f"{name:<20}{dur:>8.1f}{size / 1024:>10.1f}")
    total = sum(r[2] for r in rows) / 1024
    print("-" * 40)
    print(f"{'合计':<20}{'':>8}{total:>10.1f}")

    # 拍频提示：把两个版本之间的“可听差异”量化
    print("\n对照提示：")
    print(f"  纯五度   纯律 701.955 ¢ vs 12-TET 700.000 ¢，相差 {701.955 - 700:.3f} ¢")
    d_third = 1200 * math.log2((5 / 4) / TET_M3)
    print(f"  大三度   纯律 386.314 ¢ vs 12-TET 400.000 ¢，相差 {abs(d_third):.3f} ¢")
    print(f"  大三度的拍频 ≈ {round(abs(C4 * TET_M3 - C4 * 1.25))} Hz（基频差），高次谐波上还会翻倍")


if __name__ == "__main__":
    main()
