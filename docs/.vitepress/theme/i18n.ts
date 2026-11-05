import { computed } from 'vue'
import { useData } from 'vitepress'

/**
 * 站点级中英切换：根据 VitePress locale 的 lang 判断。
 * 组件内所有可见文案都应通过 t('中文', 'English') 或字典获取。
 */
export function useI18n() {
  const { lang } = useData()
  const isEn = computed(() => String(lang.value || '').toLowerCase().startsWith('en'))
  const t = (zh: string, en: string) => (isEn.value ? en : zh)
  return { isEn, t }
}
