<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from '../i18n'

const props = withDefaults(defineProps<{ kind?: string; title?: string }>(), {
  kind: 'note',
  title: ''
})

const { t } = useI18n()

const label = computed(() => {
  const labels: Record<string, string> = {
    axiom: t('公设', 'Axiom'),
    definition: t('定义', 'Definition'),
    theorem: t('定理', 'Theorem'),
    lemma: t('引理', 'Lemma'),
    proof: t('证明', 'Proof'),
    experiment: t('可运行实验', 'Runnable experiment'),
    exercise: t('习题', 'Exercises'),
    answer: t('解答', 'Answer'),
    algorithm: t('算法', 'Algorithm'),
    note: t('注', 'Note'),
    pitfall: t('坑', 'Common misconception'),
    checkpoint: t('自检', 'Self-check')
  }
  return labels[props.kind] ?? props.kind
})
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
