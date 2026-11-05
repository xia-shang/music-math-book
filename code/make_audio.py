"""
make_audio.py —— 生成书中可试听的对照音频（WAV）

运行：
    python code/make_audio.py

输出目录：
    docs/public/audio/

设计：
- 采样率 22050 Hz、单声道、16 bit，纯标准库（wave + struct + math）；
- 谐波合成：默认 6 个谐波、振幅按 1/k 衰减；
- 对照一律成对生成：纯律 vs 12-TET、钢琴 vs 小提琴、乐音 vs 噪声；
- 节奏与旋律也由程序生成：欧几里得节奏、复合节奏、马尔可夫链旋律；
- 每个文件归一化到 0.85 峰值，保证 A/B 对比时响度接近。

用法：改参数后重新运行即可；脚本会打印每个文件的时长与体积。
"""

from __future__ import annotations

import math
import random
import struct
import sys
import wave
from pathlib import Path

SR = 22050
PARTIALS = 6
C4 = 261.6255653005986

OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "public" / "audio"

TET_M3 = 2 ** (4 / 12)
TET_P5 = 2 ** (7 / 12)

sys.path.insert(0, str(Path(__file__).resolve().parent))


def envelope(t: float, dur: float, attack: float, release: float, decay: float | None) -> float:
    a = min(1.0, t / attack) if attack > 0 else 1.0
    r = min(1.0, (dur - t) / release) if release > 0 else 1.0
    d = math.exp(-t / decay) if decay else 1.0
    return a * r * d


def add_note(
    buf: list[float],
    start: float,
    freq: float,
    dur: float,
    amp: float,
    *,
    partials: int = PARTIALS,
    attack: float = 0.02,
    release: float = 0.08,
    decay: float | None = None,
    amp_exp: float = 1.0,
    vibrato: float = 0.0,
    vibrato_rate: float = 5.0,
) -> None:
    """把一条合成音符叠加进缓冲区。"""
    start_i = int(start * SR)
    n = int(dur * SR)
    phases = [0.0] * partials
    for i in range(n):
        t = i / SR
        vib = 1.0 + vibrato * math.sin(2 * math.pi * vibrato_rate * t)
        env = envelope(t, dur, attack, release, decay)
        s = 0.0
        for k in range(1, partials + 1):
            fk = freq * k * vib
            if fk >= SR / 2:
                break
            phases[k - 1] += 2 * math.pi * fk / SR
            s += (k ** -amp_exp) * math.sin(phases[k - 1])
        idx = start_i + i
        if idx >= len(buf):
            break
        buf[idx] += amp * env * s


def blank(duration: float) -> list[float]:
    return [0.0] * int(duration * SR)


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
    return name, len(buf) / SR, path.stat().st_size


def interval_pair(name: str, ratio_just: float, ratio_tet: float, dur: float = 1.8) -> None:
    """两个音同时发声：纯律版与 12-TET 版。"""
    for label, ratio in (("just", ratio_just), ("tet", ratio_tet)):
        buf = blank(dur)
        add_note(buf, 0.0, C4, dur, 0.5, attack=0.03, release=0.25)
        add_note(buf, 0.0, C4 * ratio, dur, 0.5, attack=0.03, release=0.25)
        normalize(buf)
        write_wav(f"{name}-{label}.wav", buf)


def chord_once(name: str, dur: float = 2.0) -> None:
    """单个 C 大三和弦：纯律（5:4、3:2）与 12-TET。"""
    for label in ("just", "tet"):
        buf = blank(dur)
        if label == "just":
            notes = [C4, C4 * 5 / 4, C4 * 3 / 2]
        else:
            notes = [C4, C4 * TET_M3, C4 * TET_P5]
        for f in notes:
            add_note(buf, 0.0, f, dur, 0.4, attack=0.03, release=0.25, decay=1.2)
        normalize(buf)
        write_wav(f"{name}-{label}.wav", buf)


def cadence_pair(name: str = "cadence", dur: float = 0.85) -> None:
    """C–F–G–C 的终止式：纯律与 12-TET。"""
    roots = [C4, C4 * 4 / 3, C4 * 3 / 2, C4 * 2]
    for label in ("just", "tet"):
        buf = blank(dur * len(roots))
        for idx, root in enumerate(roots):
            if label == "just":
                notes = [root, root * 5 / 4, root * 3 / 2]
            else:
                notes = [root, root * TET_M3, root * TET_P5]
            for f in notes:
                add_note(buf, idx * dur, f, dur, 0.4, attack=0.03, release=0.18, decay=1.2)
        normalize(buf)
        write_wav(f"{name}-{label}.wav", buf)


def scale_pair(dur: float = 0.34) -> None:
    """C 大调音阶：纯律 5 限 vs 12-TET。"""
    just = [1, 9 / 8, 5 / 4, 4 / 3, 3 / 2, 5 / 3, 15 / 8, 2]
    tet = [2 ** (s / 12) for s in (0, 2, 4, 5, 7, 9, 11, 12)]
    for label, ratios in (("just", just), ("tet", tet)):
        buf = blank(dur * len(ratios) + 0.25)
        for i, r in enumerate(ratios):
            add_note(buf, i * dur, C4 * r, dur * 0.92, 0.6, attack=0.01, release=0.12, decay=0.8)
        normalize(buf)
        write_wav(f"scale-{label}.wav", buf)


def timbre_pair(dur: float = 2.2) -> None:
    """同一个 A4，两种谐波包络与包络形状。"""
    piano = blank(dur)
    add_note(piano, 0.0, 440.0, dur, 0.8, attack=0.004, release=0.25, decay=0.7, amp_exp=1.4)
    normalize(piano)
    write_wav("timbre-piano.wav", piano)

    violin = blank(dur)
    add_note(
        violin, 0.0, 440.0, dur, 0.8,
        attack=0.12, release=0.3, amp_exp=0.75, vibrato=0.004, vibrato_rate=5.2,
    )
    normalize(violin)
    write_wav("timbre-violin.wav", violin)


def noise_tone() -> None:
    random.seed(2013)
    noise = [random.uniform(-1.0, 1.0) for _ in range(int(1.8 * SR))]
    normalize(noise, 0.7)
    write_wav("noise.wav", noise)
    tone = blank(1.8)
    add_note(tone, 0.0, 440.0, 1.8, 0.8, attack=0.03, release=0.25)
    normalize(tone)
    write_wav("tone-440.wav", tone)


def euclid_hits(k: int, n: int) -> set[int]:
    return {int(math.floor((j * n + k - 1) / k)) for j in range(k)}


def rhythm(k: int, n: int, name: str, step: float = 0.14, cycles: int = 2) -> None:
    total = n * cycles * step + 0.3
    buf = blank(total)
    hits = euclid_hits(k, n)
    for cycle in range(cycles):
        for s in range(n):
            if s in hits:
                t = (cycle * n + s) * step
                accent = 1.0 if s == 0 else 0.65
                add_note(buf, t, 1700.0, 0.05, 0.5 * accent, partials=1, attack=0.001, release=0.04, decay=0.02)
                add_note(buf, t, 190.0, 0.16, 0.9 * accent, partials=1, attack=0.001, release=0.12, decay=0.08)
    normalize(buf)
    write_wav(name, buf)


def polymeter() -> None:
    """3:4 复合节奏：一条每 4 步落一次，另一条每 3 步落一次。"""
    step = 0.15
    cycle = 12
    cycles = 2
    total = cycle * cycles * step + 0.4
    buf = blank(total)
    for c in range(cycles):
        for s in range(0, cycle, 4):
            t = (c * cycle + s) * step
            add_note(buf, t, 880.0, 0.14, 0.45, partials=2, attack=0.004, release=0.1, decay=0.08)
        for s in range(0, cycle, 3):
            t = (c * cycle + s) * step
            add_note(buf, t, 440.0, 0.14, 0.4, partials=2, attack=0.004, release=0.1, decay=0.08)
    normalize(buf)
    write_wav("polymeter-3-4.wav", buf)


def markov_melody() -> None:
    """直接复用第 8 章的语料与转移矩阵，生成一段固定种子的旋律。"""
    import ch08_melody as m8

    counts = m8.count_matrix(m8.SEQ)
    probs = m8.row_probs(counts)
    seq, _steps = m8.generate(probs, seed=8, bars=8, temperature=1.0, start=0)
    step = 0.3
    buf = blank(len(seq) * step + 0.4)
    for i, note in enumerate(seq):
        freq = C4 * 2 ** (m8.PC[note] / 12)
        add_note(buf, i * step, freq, step * 0.88, 0.55, attack=0.01, release=0.12, decay=0.5)
    normalize(buf)
    write_wav("markov-melody.wav", buf)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []

    # 1. 音程对照
    interval_pair("fifth", 3 / 2, TET_P5)
    interval_pair("third", 5 / 4, TET_M3)
    interval_pair("tritone", 45 / 32, 2 ** (6 / 12))

    # 2. 和弦、终止式、音阶、音色
    chord_once("chord")
    cadence_pair()
    scale_pair()
    timbre_pair()
    noise_tone()

    # 3. 节奏
    rhythm(3, 8, "euclid-3-8.wav")
    rhythm(5, 8, "euclid-5-8.wav")
    rhythm(5, 13, "euclid-5-13.wav")
    polymeter()

    # 4. 由马尔可夫链生成的旋律
    markov_melody()

    print(f"输出目录：{OUT_DIR}")
    print(f"{'文件':<22}{'时长(s)':>8}{'体积(KB)':>10}")
    print("-" * 42)
    for path in sorted(OUT_DIR.glob("*.wav")):
        with wave.open(str(path), "r") as w:
            dur = w.getnframes() / w.getframerate()
        print(f"{path.name:<22}{dur:>8.2f}{path.stat().st_size / 1024:>10.1f}")
        rows.append(path.stat().st_size)
    print("-" * 42)
    print(f"{'合计 ' + str(len(rows)) + ' 个文件':<22}{'':>8}{sum(rows) / 1024:>10.1f}")


if __name__ == "__main__":
    main()
