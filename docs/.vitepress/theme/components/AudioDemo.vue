<script setup lang="ts">
import { withBase } from 'vitepress'

const props = withDefaults(
  defineProps<{
    src: string
    title?: string
    hint?: string
    badge?: string
  }>(),
  { title: '', hint: '', badge: 'WAV' }
)
</script>

<template>
  <div class="audio-demo">
    <div class="audio-demo__head">
      <span class="audio-demo__badge">{{ props.badge }}</span>
      <span v-if="props.title" class="audio-demo__title">{{ props.title }}</span>
    </div>
    <audio controls preload="none" :src="withBase(props.src)"></audio>
    <p v-if="props.hint" class="audio-demo__hint">{{ props.hint }}</p>
  </div>
</template>
