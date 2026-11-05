<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useI18n } from '../i18n'

const { t, isEn } = useI18n()

/**
 * 欧几里得节奏实验：E(k,n) 的圆环可视化 + Web Audio 节拍试听。
 * 与正文定义 7.1 一致：p_j = floor((j·n + k − 1)/k)。
 */

const k = ref(3)
const n = ref(8)
const bpm = ref(120)

const hits = computed(() => {
  const kk = Math.min(k.value, n.value)
  return new Set(
    Array.from({ length: kk }, (_, j) => Math.floor((j * n.value + kk - 1) / kk))
  )
})

const pattern = computed(() =>
  Array.from({ length: n.value }, (_, i) => (hits.value.has(i) ? 'x' : '.')).join('')
)

const gaps = computed(() => {
  const arr = Array.from(hits.value).sort((a, b) => a - b)
  return arr.map((v, i) => {
    const next = i + 1 < arr.length ? arr[i + 1] : arr[0] + n.value
    return next - v
  })
})

const CX = 150
const CY = 140
const R = 102

function dot(i: number) {
  const a = (2 * Math.PI * i) / n.value - Math.PI / 2
  return { x: CX + R * Math.cos(a), y: CY + R * Math.sin(a) }
}

function clamp() {
  if (n.value < 1) n.value = 1
  if (n.value > 16) n.value = 16
  if (k.value < 1) k.value = 1
  if (k.value > n.value) k.value = n.value
}

watch([k, n], () => {
  clamp()
  stop()
})

watch(bpm, stop)

const playing = ref(false)
const active = ref(-1)
let audio: AudioContext | null = null
let timers: number[] = []

function stop() {
  timers.forEach((t) => window.clearTimeout(t))
  timers = []
  playing.value = false
  active.value = -1
}

function click(ac: AudioContext, at: number, accent: boolean) {
  const osc = ac.createOscillator()
  const gain = ac.createGain()
  osc.type = 'sine'
  osc.frequency.setValueAtTime(accent ? 1500 : 1100, at)
  osc.frequency.exponentialRampToValueAtTime(accent ? 700 : 520, at + 0.05)
  gain.gain.setValueAtTime(accent ? 0.5 : 0.3, at)
  gain.gain.exponentialRampToValueAtTime(0.001, at + 0.12)
  osc.connect(gain).connect(ac.destination)
  osc.start(at)
  osc.stop(at + 0.14)

  const low = ac.createOscillator()
  const lg = ac.createGain()
  low.type = 'sine'
  low.frequency.setValueAtTime(accent ? 170 : 120, at)
  lg.gain.setValueAtTime(accent ? 0.5 : 0.22, at)
  lg.gain.exponentialRampToValueAtTime(0.001, at + 0.18)
  low.connect(lg).connect(ac.destination)
  low.start(at)
  low.stop(at + 0.2)
}

function play() {
  if (playing.value) {
    stop()
    return
  }
  const Ctx = window.AudioContext || (window as any).webkitAudioContext
  if (!Ctx) return
  audio ??= new Ctx()
  if (audio.state === 'suspended') audio.resume()
  const ac = audio
  const stepDur = 60 / bpm.value / 4
  const total = n.value * 2
  const start = ac.currentTime + 0.12

  playing.value = true
  for (let s = 0; s < total; s++) {
    const pos = s % n.value
    if (hits.value.has(pos)) {
      click(ac, start + s * stepDur, pos === 0)
    }
    timers.push(
      window.setTimeout(() => {
        active.value = pos
      }, (0.12 + s * stepDur) * 1000)
    )
  }
  timers.push(
    window.setTimeout(() => {
      playing.value = false
      active.value = -1
    }, (0.12 + total * stepDur) * 1000 + 120)
  )
}

onBeforeUnmount(() => {
  stop()
  audio?.close()
  audio = null
})
</script>

<template>
  <div class="rhythm-lab">
    <div class="rhythm-lab__controls">
      <label>
        <span>{{ t('重音数', 'Accents') }} k = <b>{{ k }}</b></span>
        <input v-model.number="k" type="range" min="1" max="16" step="1" />
      </label>
      <label>
        <span>{{ t('格子数', 'Steps') }} n = <b>{{ n }}</b></span>
        <input v-model.number="n" type="range" min="1" max="16" step="1" />
      </label>
      <label>
        <span>{{ t('速度', 'Tempo') }} <b>{{ bpm }} BPM</b></span>
        <input v-model.number="bpm" type="range" min="60" max="180" step="5" />
      </label>
      <button class="rhythm-lab__play" type="button" @click="play">
        {{ playing ? t('■ 停止', '■ Stop') : t('▶ 试听两小节', '▶ Play two bars') }}
      </button>
    </div>

    <div class="rhythm-lab__body">
      <svg viewBox="0 0 300 280" role="img" :aria-label="t('欧几里得节奏圆环', 'Euclidean rhythm circle')">
        <circle :cx="CX" :cy="CY" :r="R" fill="none" stroke="var(--vp-c-divider)" stroke-width="1.5" />
        <g v-for="i in n" :key="i">
          <circle
            :cx="dot(i - 1).x"
            :cy="dot(i - 1).y"
            :r="hits.has(i - 1) ? 13 : 9"
            :class="[
              'rhythm-lab__dot',
              { 'is-hit': hits.has(i - 1), 'is-active': i - 1 === active }
            ]"
          />
          <text
            v-if="n <= 12"
            :x="dot(i - 1).x"
            :y="dot(i - 1).y + 4"
            text-anchor="middle"
            :class="['rhythm-lab__num', { 'is-hit': hits.has(i - 1) }]"
          >
            {{ i - 1 }}
          </text>
        </g>
        <text x="150" y="128" text-anchor="middle" class="rhythm-lab__center">E({{ k }},{{ n }})</text>
        <text x="150" y="150" text-anchor="middle" class="rhythm-lab__pattern">{{ pattern }}</text>
      </svg>

      <div class="rhythm-lab__info">
        <div class="rhythm-lab__stat">
          <span>{{ t('模式', 'Pattern') }}</span><b>{{ pattern }}</b>
        </div>
        <div class="rhythm-lab__stat">
          <span>{{ t('循环间隔', 'Gaps') }}</span><b>{{ gaps.join(' · ') }}</b>
        </div>
        <div class="rhythm-lab__stat">
          <span>{{ t('重音密度', 'Density') }}</span><b>{{ (k / n).toFixed(2) }}</b>
        </div>
        <p>
          <template v-if="isEn">
            The closer k/n is to a simple fraction, the more the pattern reads as an even grouping;
            coprime k and n push accents out of phase and create a rolling feel. Drag the sliders and
            listen to how the same set of dots breathes at different tempos.
          </template>
          <template v-else>
            k/n 越接近简单分数，节奏越容易被听成「整齐的分组」；互质的 k、n 会让重音在循环里错位，
            产生滚动感。拖动滑块，听同一组点在不同速度下的「呼吸」。
          </template>
        </p>
      </div>
    </div>
  </div>
</template>
