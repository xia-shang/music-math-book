<script setup lang="ts">
import { ref, computed } from 'vue'

const DEGREES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

// 7 个自然音级在三种律制下的绝对音高（cents，以 C 为 0）
const TUNINGS = [
  {
    name: '十二平均律 12-TET',
    note: '100n —— 全世界的默认值',
    values: [0, 200, 400, 500, 700, 900, 1100]
  },
  {
    name: '纯律 Just Intonation',
    note: '5 限整数比：5/4、6/5、8/5 …',
    values: [0, 203.91, 386.314, 498.858, 701.955, 884.359, 1088.269]
  },
  {
    name: '五度相生律 Pythagorean',
    note: '只由 3/2 堆叠生成',
    values: [0, 203.91, 407.82, 498.858, 701.955, 905.865, 1109.775]
  }
]

const hover = ref<string | null>(null)

const W = 640
const ROW_H = 62
const PAD_L = 78
const PAD_R = 34

const H = computed(() => TUNINGS.length * ROW_H + 34)

function x(c: number): number {
  return PAD_L + (c / 1200) * (W - PAD_L - PAD_R)
}

function dev(t: (typeof TUNINGS)[number], i: number): number {
  return t.values[i] - 100 * i
}

function fmt(d: number): string {
  const r = Math.round(d * 10) / 10
  return (r > 0 ? '+' : '') + r.toFixed(1)
}
</script>

<template>
  <div class="ruler">
    <svg :viewBox="`0 0 ${W} ${H}`" role="img" aria-label="三种律制的音高位置对比">
      <g v-for="(t, ti) in TUNINGS" :key="t.name">
        <line
          :x1="PAD_L"
          :y1="ti * ROW_H + 30"
          :x2="W - PAD_R"
          :y2="ti * ROW_H + 30"
          class="ruler-line"
        />
        <text :x="8" :y="ti * ROW_H + 26" class="ruler-name">{{ t.name }}</text>
        <text :x="8" :y="ti * ROW_H + 41" class="ruler-note">{{ t.note }}</text>
        <g v-for="(v, i) in t.values" :key="DEGREES[i]">
          <line :x1="x(v)" :y1="ti * ROW_H + 26" :x2="x(v)" :y2="ti * ROW_H + 34" class="ruler-tick" />
          <text
            :x="x(v)"
            :y="ti * ROW_H + 50"
            text-anchor="middle"
            :class="['ruler-deg', { 'is-hover': hover === `${ti}-${i}` }]"
            @mouseenter="hover = `${ti}-${i}`"
          >
            {{ DEGREES[i] }}
          </text>
          <text
            v-if="Math.abs(dev(t, i)) >= 2"
            :x="x(v)"
            :y="ti * ROW_H + 14"
            text-anchor="middle"
            class="ruler-dev"
          >
            {{ fmt(dev(t, i)) }}
          </text>
        </g>
      </g>
    </svg>
    <p class="ruler__hint">
      纵向对齐的是同一个音名。数字表示该律制相对十二平均律的偏差（cents）。
      纯律把大三度压低了 13.7 cents（386.3 → 400），五度相生律则把大三度抬高了 7.8 cents ——
      这两条曲线在第 4 章会正式求交。
    </p>
  </div>
</template>
