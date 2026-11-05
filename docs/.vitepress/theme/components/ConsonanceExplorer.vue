<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useI18n } from '../i18n'

const { t, isEn } = useI18n()

/**
 * 与 code/roughness 模型（common.py）完全一致的教学模型：
 *   CB(f) = 94 + 71.3 · (f/1kHz)^0.69            —— 临界带宽（公设）
 *   W(Δf) = x²·e^(1−x²),  x = Δf / (0.25·CB)     —— 粗糙度核
 *   D     = Σ_i Σ_j (1/i)(1/j) W(...)             —— 不协和度
 *   S     = 1 / (1 + D)                           —— 协和度
 * 谐波数固定为 5，振幅 a_k = 1/k。
 */

const CB_BASE = 94
const CB_SLOPE = 71.3
const CB_EXP = 0.69
const PEAK = 0.25
const PARTIALS = 5

function cb(f: number): number {
  return CB_BASE + CB_SLOPE * Math.pow(Math.max(f, 1) / 1000, CB_EXP)
}

function kernel(df: number, bw: number): number {
  const x = Math.abs(df) / (PEAK * bw)
  if (x === 0) return 0
  return x * x * Math.exp(1 - x * x)
}

function dissonance(f1: number, f2: number): number {
  let sum = 0
  for (let i = 1; i <= PARTIALS; i++) {
    for (let j = 1; j <= PARTIALS; j++) {
      const fi = i * f1
      const fj = j * f2
      sum += (1 / i) * (1 / j) * kernel(fi - fj, cb(Math.min(fi, fj)))
    }
  }
  return sum
}

const base = ref(330)
const detune = ref(0)

const INTERVALS = [
  { name: '纯一度', nameEn: 'Unison', ratio: 1, symbol: '1:1' },
  { name: '小二度', nameEn: 'Minor 2nd', ratio: 16 / 15, symbol: '16:15' },
  { name: '大二度', nameEn: 'Major 2nd', ratio: 9 / 8, symbol: '9:8' },
  { name: '小三度', nameEn: 'Minor 3rd', ratio: 6 / 5, symbol: '6:5' },
  { name: '大三度', nameEn: 'Major 3rd', ratio: 5 / 4, symbol: '5:4' },
  { name: '纯四度', nameEn: 'Perfect 4th', ratio: 4 / 3, symbol: '4:3' },
  { name: '三全音', nameEn: 'Tritone', ratio: 45 / 32, symbol: '45:32' },
  { name: '纯五度', nameEn: 'Perfect 5th', ratio: 3 / 2, symbol: '3:2' },
  { name: '小六度', nameEn: 'Minor 6th', ratio: 8 / 5, symbol: '8:5' },
  { name: '大六度', nameEn: 'Major 6th', ratio: 5 / 3, symbol: '5:3' },
  { name: '小七度', nameEn: 'Minor 7th', ratio: 16 / 9, symbol: '16:9' },
  { name: '大七度', nameEn: 'Major 7th', ratio: 15 / 8, symbol: '15:8' },
  { name: '纯八度', nameEn: 'Octave', ratio: 2, symbol: '2:1' }
]

const idx = ref(7) // 纯五度

const current = computed(() => INTERVALS[idx.value])
const ratio = computed(() => current.value.ratio * Math.pow(2, detune.value / 1200))
const cents = computed(() => 1200 * Math.log2(ratio.value))

const D = computed(() => dissonance(base.value, base.value * ratio.value))
const score = computed(() => 1 / (1 + D.value))
const beats = computed(() => Math.abs(base.value * ratio.value - base.value))

const W = 620
const H = 230
const PAD_L = 40
const PAD_B = 34
const PAD_T = 14

const samples = computed(() => {
  const pts: { c: number; d: number }[] = []
  for (let c = 0; c <= 1200; c += 4) {
    pts.push({ c, d: dissonance(base.value, base.value * Math.pow(2, c / 1200)) })
  }
  return pts
})

const maxD = computed(() => Math.max(...samples.value.map((p) => p.d), 0.001))

function x(c: number): number {
  return PAD_L + (c / 1200) * (W - PAD_L - 10)
}
const plotH = H - PAD_T - PAD_B
function y(d: number): number {
  return PAD_T + plotH - (d / maxD.value) * plotH
}

const path = computed(() =>
  samples.value
    .map((p, i) => `${i === 0 ? 'M' : 'L'}${x(p.c).toFixed(1)},${y(p.d).toFixed(1)}`)
    .join(' ')
)

const LANDMARKS = computed(() => [
  { c: 0, name: t('一度', 'unison') },
  { c: 1200 * Math.log2(5 / 4), name: t('大三度', 'M3') },
  { c: 1200 * Math.log2(4 / 3), name: t('四度', 'P4') },
  { c: 1200 * Math.log2(3 / 2), name: t('五度', 'P5') },
  { c: 1200, name: t('八度', 'octave') }
])

/** 前 8 阶谐波里，两列频率相差不到 0.5% 的对数。 */
const coincidences = computed(() => {
  let n = 0
  for (let i = 1; i <= 8; i++) {
    for (let j = 1; j <= 8; j++) {
      const a = i * base.value
      const b = j * base.value * ratio.value
      if (Math.abs(a - b) / Math.max(a, b) < 0.005) n++
    }
  }
  return n
})

/** 谐波梳的坐标：把两列前 8 阶谐波画在同一条频率轴上。 */
const comb = computed(() => {
  const maxF = Math.max(8 * base.value, 8 * base.value * ratio.value)
  const rx = (f: number) => 22 + (f / maxF) * (W - 44)
  const first = Array.from({ length: 8 }, (_, i) => ({
    x: rx((i + 1) * base.value),
    f: (i + 1) * base.value
  }))
  const second = Array.from({ length: 8 }, (_, i) => ({
    x: rx((i + 1) * base.value * ratio.value),
    f: (i + 1) * base.value * ratio.value
  }))
  return { first, second }
})

const playing = ref(false)
let audio: AudioContext | null = null
let voices: OscillatorNode[] = []
let stopTimer: number | null = null

function stopAudio() {
  voices.forEach((voice) => {
    try {
      voice.stop()
    } catch {
      /* 已经停止 */
    }
  })
  voices = []
  if (stopTimer !== null) {
    window.clearTimeout(stopTimer)
    stopTimer = null
  }
  playing.value = false
}

function playInterval() {
  if (playing.value) {
    stopAudio()
    return
  }
  const Ctx = window.AudioContext || (window as any).webkitAudioContext
  if (!Ctx) return
  audio ??= new Ctx()
  if (audio.state === 'suspended') audio.resume()

  const now = audio.currentTime + 0.04
  const dur = 2.2
  const master = audio.createGain()
  master.gain.value = 0.22
  master.connect(audio.destination)

  for (const f of [base.value, base.value * ratio.value]) {
    for (let k = 1; k <= 6; k++) {
      if (f * k >= 11000) break
      const osc = audio.createOscillator()
      const gain = audio.createGain()
      const level = 0.5 / k
      osc.type = 'sine'
      osc.frequency.value = f * k
      gain.gain.setValueAtTime(0, now)
      gain.gain.linearRampToValueAtTime(level, now + 0.03)
      gain.gain.setValueAtTime(level, now + dur - 0.3)
      gain.gain.linearRampToValueAtTime(0, now + dur)
      osc.connect(gain).connect(master)
      osc.start(now)
      osc.stop(now + dur)
      voices.push(osc)
    }
  }
  playing.value = true
  stopTimer = window.setTimeout(() => {
    playing.value = false
    voices = []
  }, dur * 1000)
}

watch([base, ratio], stopAudio)
onBeforeUnmount(() => {
  stopAudio()
  audio?.close()
  audio = null
})
</script>

<template>
  <div class="explorer">
    <div class="explorer__controls">
      <label>
        <span>{{ t('基线频率', 'Base frequency') }} f₁ = <b>{{ base }} Hz</b></span>
        <input v-model.number="base" type="range" min="165" max="660" step="5" />
      </label>
      <label>
        <span>{{ t('选择音程（纯律比值）', 'Interval (just ratio)') }}</span>
        <select v-model.number="idx">
          <option v-for="(iv, i) in INTERVALS" :key="iv.name" :value="i">
            <template v-if="isEn">{{ iv.nameEn }} ({{ iv.symbol }})</template>
            <template v-else>{{ iv.name }}（{{ iv.symbol }}）</template>
          </option>
        </select>
      </label>
      <label>
        <span>{{ t('微调', 'Detune') }} <b>{{ detune > 0 ? '+' : '' }}{{ detune }} ¢</b></span>
        <input v-model.number="detune" type="range" min="-100" max="100" step="1" />
      </label>
    </div>

    <div class="explorer__actions">
      <button class="explorer__play" type="button" @click="playInterval">
        {{ playing ? t('■ 停止', '■ Stop') : t('▶ 试听这个音程', '▶ Play this interval') }}
      </button>
      <span class="explorer__note">{{ t('6 个谐波合成 · 约 2.2 秒', '6-harmonic synth · ~2.2 s') }}</span>
    </div>

    <div class="explorer__stats">
      <div class="stat">
        <span class="stat__k">f₂ / f₁</span>
        <span class="stat__v">{{ ratio.toFixed(4) }}</span>
      </div>
      <div class="stat">
        <span class="stat__k">{{ t('音程', 'Interval') }}</span>
        <span class="stat__v">{{ cents.toFixed(1) }} ¢</span>
      </div>
      <div class="stat">
        <span class="stat__k">{{ t('拍频', 'Beat') }} |Δf|</span>
        <span class="stat__v">{{ beats.toFixed(1) }} Hz</span>
      </div>
      <div class="stat">
        <span class="stat__k">{{ t('粗糙度', 'Roughness') }} D</span>
        <span class="stat__v">{{ D.toFixed(3) }}</span>
      </div>
      <div class="stat stat--score">
        <span class="stat__k">{{ t('协和度', 'Consonance') }} S</span>
        <span class="stat__v">{{ score.toFixed(3) }}</span>
      </div>
      <div class="stat">
        <span class="stat__k">{{ t('前 8 阶重合', 'Coincidences (first 8)') }}</span>
        <span class="stat__v">{{ coincidences }} {{ t('对', 'pairs') }}</span>
      </div>
    </div>

    <div class="explorer__meter">
      <div class="explorer__meter-fill" :style="{ width: `${Math.min(score * 100, 100)}%` }"></div>
    </div>

    <svg class="explorer__plot" :viewBox="`0 0 ${W} ${H}`" role="img" :aria-label="t('粗糙度随音程变化曲线', 'Roughness versus interval')">
      <line :x1="PAD_L" :y1="H - PAD_B" :x2="W - 10" :y2="H - PAD_B" class="axis" />
      <line :x1="PAD_L" :y1="PAD_T" :x2="PAD_L" :y2="H - PAD_B" class="axis" />
      <text :x="PAD_L - 8" :y="PAD_T + 8" text-anchor="end" class="axis-label">D</text>
      <text :x="W - 12" :y="H - 10" text-anchor="end" class="axis-label">{{ t('音程（cents）', 'interval (cents)') }}</text>
      <line
        v-for="lm in LANDMARKS"
        :key="lm.name"
        :x1="x(lm.c)"
        :y1="H - PAD_B"
        :x2="x(lm.c)"
        :y2="H - PAD_B + 6"
        class="tick"
      />
      <text
        v-for="lm in LANDMARKS"
        :key="lm.name + 't'"
        :x="x(lm.c)"
        :y="H - PAD_B + 19"
        text-anchor="middle"
        class="tick-label"
      >
        {{ lm.name }}
      </text>
      <path :d="path" class="curve" />
      <line :x1="x(cents)" :y1="PAD_T" :x2="x(cents)" :y2="H - PAD_B" class="marker" />
      <circle :cx="x(cents)" :cy="y(D)" r="4" class="dot" />
    </svg>

    <svg class="explorer__comb" viewBox="0 0 620 112" role="img" :aria-label="t('两列谐波在频率轴上的分布', 'Two harmonic series on a frequency axis')">
      <text x="6" y="14" class="tick-label">{{ t('谐波梳：每个点是一次谐波，靠近的点会产生拍频', 'Harmonic comb: each dot is one harmonic; nearby dots beat') }}</text>
      <line x1="22" y1="44" x2="598" y2="44" class="axis" />
      <line x1="22" y1="80" x2="598" y2="80" class="axis" />
      <text x="16" y="41" text-anchor="end" class="tick-label">f₁</text>
      <text x="16" y="77" text-anchor="end" class="tick-label">f₂</text>
      <circle
        v-for="(p, i) in comb.first"
        :key="'a' + i"
        :cx="p.x"
        cy="44"
        r="3.2"
        class="comb-dot comb-dot--a"
      />
      <circle
        v-for="(p, i) in comb.second"
        :key="'b' + i"
        :cx="p.x"
        cy="80"
        r="3.2"
        class="comb-dot comb-dot--b"
      />
      <text x="22" y="106" class="tick-label">{{ t('越向右频率越高；两列点越接近，对应的谐波对拍频越慢、越容易被听成「摇晃」。', 'Higher frequency to the right. Closer dots beat more slowly and read as “wobble”.') }}</text>
    </svg>

    <p class="explorer__hint">
      <template v-if="isEn">
        The valleys mark maximum harmonic coincidence: 384 ¢ (5:4), 500 ¢ (4:3), 702 ¢ (3:2),
        886 ¢ (5:3), 970 ¢ (7:4). Changing the base frequency moves neither the valleys nor their
        pitch-class positions, but it does change their depth: the critical bandwidth grows with
        frequency, though not fast enough to change the normalized distance.
      </template>
      <template v-else>
        曲线上的谷底就是「谐波重合最多」的位置：384 ¢（5:4）、500 ¢（4:3）、702 ¢（3:2）、
        886 ¢（5:3）、970 ¢（7:4）。改变基线频率，谷底的位置不变、深浅会变 ——
        因为临界带宽随频率增长，但没有快到来得及改变归一化距离。
      </template>
    </p>
  </div>
</template>
