<script setup lang="ts">
import { withBase } from 'vitepress'

const props = withDefaults(
  defineProps<{
    src: string
    alt?: string
    caption?: string
    maxWidth?: string
  }>(),
  { alt: '', caption: '', maxWidth: '' }
)
</script>

<template>
  <figure class="mm-figure">
    <img
      :src="withBase(src)"
      :alt="props.alt || props.caption"
      :style="props.maxWidth ? { maxWidth: props.maxWidth } : undefined"
      loading="lazy"
    />
    <figcaption v-if="props.caption">{{ props.caption }}</figcaption>
  </figure>
</template>
