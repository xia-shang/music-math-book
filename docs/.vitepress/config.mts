import { defineConfig } from 'vitepress'

const repoUrl = process.env.GITHUB_REPOSITORY
  ? `https://github.com/${process.env.GITHUB_REPOSITORY}`
  : 'https://github.com/your-name/music-math-book'
const base = process.env.BASE_PATH || '/'

export default defineConfig({
  lang: 'zh-CN',
  title: '理科生的乐理书',
  description:
    '《音乐的数理逻辑：从振动到结构的公理化乐理》—— 用物理、数学与代码重写乐理。程序员版。',
  base,
  cleanUrls: true,
  // 本地没有安装 git 时跳过「最后更新」查询；CI 环境下开启
  lastUpdated: Boolean(process.env.CI),
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: `${base}logo.svg` }],
    ['meta', { name: 'theme-color', content: '#0f766e' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: '理科生的乐理书 · 程序员版' }],
    [
      'meta',
      {
        property: 'og:description',
        content: '从振动到结构：音乐的数理逻辑公理化推导。'
      }
    ]
  ],
  markdown: {
    math: true,
    lineNumbers: true,
    image: { lazyLoading: true }
  },
  themeConfig: {
    logo: { src: '/logo.svg', width: 24, height: 24 },
    siteTitle: '理科生的乐理书',
    nav: [
      { text: '导读', link: '/guide/', activeMatch: '/guide/' },
      { text: '章节', link: '/chapters/00-introduction', activeMatch: '/chapters/' },
      { text: '附录', link: '/appendix/a-math', activeMatch: '/appendix/' },
      { text: '关于', link: '/about' }
    ],
    sidebar: {
      '/guide/': [
        {
          text: '开始之前',
          items: [
            { text: '如何使用本书', link: '/guide/' },
            { text: '符号与约定', link: '/guide/notation' },
            { text: '学习路线图', link: '/guide/roadmap' }
          ]
        }
      ],
      '/chapters/': [
        {
          text: '第一部 · 声与音',
          collapsed: false,
          items: [
            { text: '第 0 章 · 导论：音乐作为接口', link: '/chapters/00-introduction' },
            { text: '第 1 章 · 振动的数学', link: '/chapters/01-vibration' },
            { text: '第 2 章 · 音高的物理与几何', link: '/chapters/02-pitch' }
          ]
        },
        {
          text: '第二部 · 协和与律制',
          collapsed: false,
          items: [
            { text: '第 3 章 · 协和与不协和', link: '/chapters/03-consonance' },
            { text: '第 4 章 · 律制的数学优化', link: '/chapters/04-tuning' },
            { text: '第 5 章 · 音阶的生成算法', link: '/chapters/05-scales' }
          ]
        },
        {
          text: '第三部 · 结构与时间',
          collapsed: false,
          items: [
            { text: '第 6 章 · 和声的线性代数', link: '/chapters/06-harmony' },
            { text: '第 7 章 · 节奏的分形与混沌', link: '/chapters/07-rhythm' },
            { text: '第 8 章 · 旋律的统计学', link: '/chapters/08-melody' },
            { text: '第 9 章 · 调性的拓扑学', link: '/chapters/09-topology' }
          ]
        }
      ],
      '/appendix/': [
        {
          text: '附录',
          items: [
            { text: 'A · 数学工具速查', link: '/appendix/a-math' },
            { text: 'B · 代码与实验环境', link: '/appendix/b-code' },
            { text: 'C · 术语与符号表', link: '/appendix/c-glossary' },
            { text: 'D · 延伸阅读', link: '/appendix/d-reading' },
            { text: 'E · 习题与答案', link: '/appendix/e-exercises' }
          ]
        }
      ]
    },
    outline: { level: [2, 3], label: '本章目录' },
    socialLinks: [{ icon: 'github', link: repoUrl }],
    search: { provider: 'local' },
    footer: {
      message: '以 CC BY-NC-SA 4.0 协议发布 · 代码示例采用 MIT 协议',
      copyright: '理科生的乐理书 · 程序员版'
    },
    docFooter: { prev: '上一章', next: '下一章' },
    darkModeSwitchLabel: '外观',
    sidebarMenuLabel: '目录',
    returnToTopLabel: '回到顶部',
    lastUpdatedText: '最后更新于',
    notFound: {
      title: '这一页不在调上',
      quote: '404：你要找的页面可能被转调到了别的空间。',
      linkLabel: '回到首页',
      linkText: '回到首页'
    }
  }
})
