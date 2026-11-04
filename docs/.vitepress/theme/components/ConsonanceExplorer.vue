<script setup lang="ts">
import { computed, ref } from 'vue'

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
  { name: '纯一度', ratio: 1, symbol: '1:1' },
  { name: '小二度', ratio: 16 / 15, symbol: '16:15' },
  { name: '大二度', ratio: 9 / 8, symbol: '9:8' },
  { name: '小三度', ratio: 6 / 5, symbol: '6:5' },
  { name: '大三度', ratio: 5 / 4, symbol: '5:4' },
  { name: '纯四度', ratio: 4 / 3, symbol: '4:3' },
  { name: '三全音', ratio: 45 / 32, symbol: '45:32' },
  { name: '纯五度', ratio: 3 / 2, symbol: '3:2' },
  { name: '小六度', ratio: 8 / 5, symbol: '8:5' },
  { name: '大六度', ratio: 5 / 3, symbol: '5:3' },
  { name: '小七度', ratio: 16 / 9, symbol: '16:9' },
  { name: '大七度', ratio: 15 / 8, symbol: '15:8' },
  { name: '纯八度', ratio: 2, symbol: '2:1' }
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

const LANDMARKS = [
  { c: 0, name: '一度' },
  { c: 1200 * Math.log2(5 / 4), name: '大三度' },
  { c: 1200 * Math.log2(4 / 3), name: '四度' },
  { c: 1200 * Math.log2(3 / 2), name: '五度' },
  { c: 1200, name: '八度' }
]
</script>

<template>
  <div class="explorer">
    <div class="explorer__controls">
      <label>
        <span>基线频率 f₁ = <b>{{ base }} Hz</b></span>
        <input v-model.number="base" type="range" min="165" max="660" step="5" />
      </label>
      <label>
        <span>选择音程（纯律比值）</span>
        <select v-model.number="idx">
          <option v-for="(iv, i) in INTERVALS" :key="iv.name" :value="i">
            {{ iv.name }}（{{ iv.symbol }}）
          </option>
        </select>
      </label>
      <label>
        <span>微调 <b>{{ detune > 0 ? '+' : '' }}{{ detune }} ¢</b></span>
        <input v-model.number="detune" type="range" min="-100" max="100" step="1" />
      </label>
    </div>

    <div class="explorer__stats">
      <div class="stat">
        <span class="stat__k">f₂ / f₁</span>
        <span class="stat__v">{{ ratio.toFixed(4) }}</span>
      </div>
      <div class="stat">
        <span class="stat__k">音程</span>
        <span class="stat__v">{{ cents.toFixed(1) }} ¢</span>
      </div>
      <div class="stat">
        <span class="stat__k">拍频 |Δf|</span>
        <span class="stat__v">{{ beats.toFixed(1) }} Hz</span>
      </div>
      <div class="stat">
        <span class="stat__k">粗糙度 D</span>
        <span class="stat__v">{{ D.toFixed(3) }}</span>
      </div>
      <div class="stat stat--score">
        <span class="stat__k">协和度 S</span>
        <span class="stat__v">{{ score.toFixed(3) }}</span>
      </div>
    </div>

    <div class="explorer__meter">
      <div class="explorer__meter-fill" :style="{ width: `${Math.min(score * 100, 100)}%` }"></div>
    </div>

    <svg class="explorer__plot" :viewBox="`0 0 ${W} ${H}`" role="img" aria-label="粗糙度随音程变化曲线">
      <line :x1="PAD_L" :y1="H - PAD_B" :x2="W - 10" :y2="H - PAD_B" class="axis" />
      <line :x1="PAD_L" :y1="PAD_T" :x2="PAD_L" :y2="H - PAD_B" class="axis" />
      <text :x="PAD_L - 8" :y="PAD_T + 8" text-anchor="end" class="axis-label">D</text>
      <text :x="W - 12" :y="H - 10" text-anchor="end" class="axis-label">音程（cents）</text>
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

    <p class="explorer__hint">
      曲线上的谷底就是「谐波重合最多」的位置：383 ¢（5:4）、498 ¢（4:3）、702 ¢（3:2）、
      884 ¢（5:3）、969 ¢（7:4）。把基线频率从 330 Hz 拖到 440 Hz，谷底会整体变浅 ——
      这就是「高音区更宽容」的数学解释。
    </p>
  </div>
</template>
