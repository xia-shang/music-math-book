<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{ kind?: string; title?: string }>(), {
  kind: 'note',
  title: ''
})

const LABELS: Record<string, string> = {
  axiom: '公设',
  definition: '定义',
  theorem: '定理',
  lemma: '引理',
  proof: '证明',
  experiment: '可运行实验',
  exercise: '习题',
  answer: '解答',
  algorithm: '算法',
  note: '注',
  pitfall: '坑',
  checkpoint: '自检'
}

const label = computed(() => LABELS[props.kind] ?? props.kind)
</script>

<template>
  <div :class="['mathbox', `mathbox--${kind}`]">
    <div class="mathbox__head">
      <span class="mathbox__label">{{ label }}</span>
      <span v-if="title" class="mathbox__title">{{ title }}</span>
    </div>
    <div class="mathbox__body"><slot /></div>
  </div>
</template>
