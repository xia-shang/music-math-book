import { defineConfig } from 'vitepress'

const VERSION = '1.1.0'
const repoUrl = process.env.GITHUB_REPOSITORY
  ? `https://github.com/${process.env.GITHUB_REPOSITORY}`
  : 'https://github.com/your-name/music-math-book'
const base = process.env.BASE_PATH || '/'

const zhThemeConfig = {
  logo: { src: '/logo.svg', width: 24, height: 24 },
  siteTitle: '理科生的乐理书',
  nav: [
    { text: '导读', link: '/guide/', activeMatch: '/guide/' },
    { text: '章节', link: '/chapters/00-introduction', activeMatch: '/chapters/' },
    { text: '附录', link: '/appendix/a-math', activeMatch: '/appendix/' },
    { text: '关于', link: '/about' },
    { text: `v${VERSION}`, link: '/releases' }
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
  search: {
    provider: 'local',
    options: {
      translations: {
        button: { buttonText: '搜索本书', buttonAriaLabel: '搜索本书' },
        modal: {
          displayDetails: '显示详情',
          resetButtonTitle: '清除搜索',
          backButtonTitle: '返回',
          noResultsText: '没有找到相关内容，试试「音程」「协和度」或「马尔可夫」。',
          footer: {
            selectText: '打开',
            selectKeyAriaLabel: '回车键',
            navigateText: '切换结果',
            navigateUpKeyAriaLabel: '向上箭头',
            navigateDownKeyAriaLabel: '向下箭头',
            closeText: '关闭',
            closeKeyAriaLabel: 'Esc 键'
          }
        }
      }
    }
  },
  footer: {
    message: '以 CC BY-NC-SA 4.0 协议发布 · 代码示例采用 MIT 协议',
    copyright: `理科生的乐理书 · 程序员版 · v${VERSION}`
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

const enThemeConfig = {
  logo: { src: '/logo.svg', width: 24, height: 24 },
  siteTitle: 'Music as Math',
  nav: [
    { text: 'Guide', link: '/en/guide/', activeMatch: '/en/guide/' },
    { text: 'Chapters', link: '/en/chapters/00-introduction', activeMatch: '/en/chapters/' },
    { text: 'Appendices', link: '/en/appendix/a-math', activeMatch: '/en/appendix/' },
    { text: 'About', link: '/en/about' },
    { text: `v${VERSION}`, link: '/en/releases' }
  ],
  sidebar: {
    '/en/guide/': [
      {
        text: 'Before You Start',
        items: [
          { text: 'How to Read This Book', link: '/en/guide/' },
          { text: 'Notation and Conventions', link: '/en/guide/notation' },
          { text: 'Reading Roadmap', link: '/en/guide/roadmap' }
        ]
      }
    ],
    '/en/chapters/': [
      {
        text: 'Part I · Sound and Pitch',
        collapsed: false,
        items: [
          { text: 'Ch. 0 · Introduction: Music as Interface', link: '/en/chapters/00-introduction' },
          { text: 'Ch. 1 · The Mathematics of Vibration', link: '/en/chapters/01-vibration' },
          { text: 'Ch. 2 · The Physics and Geometry of Pitch', link: '/en/chapters/02-pitch' }
        ]
      },
      {
        text: 'Part II · Consonance and Tuning',
        collapsed: false,
        items: [
          { text: 'Ch. 3 · Consonance and Dissonance', link: '/en/chapters/03-consonance' },
          { text: 'Ch. 4 · Tuning as Optimization', link: '/en/chapters/04-tuning' },
          { text: 'Ch. 5 · Algorithms for Scales', link: '/en/chapters/05-scales' }
        ]
      },
      {
        text: 'Part III · Structure and Time',
        collapsed: false,
        items: [
          { text: 'Ch. 6 · Harmony as Linear Algebra', link: '/en/chapters/06-harmony' },
          { text: 'Ch. 7 · Rhythm: Fractals and Chaos', link: '/en/chapters/07-rhythm' },
          { text: 'Ch. 8 · Melody: Statistics and Information', link: '/en/chapters/08-melody' },
          { text: 'Ch. 9 · Tonality and Atonality: A Topology', link: '/en/chapters/09-topology' }
        ]
      }
    ],
    '/en/appendix/': [
      {
        text: 'Appendices',
        items: [
          { text: 'A · Mathematical Toolkit', link: '/en/appendix/a-math' },
          { text: 'B · Code and Experiments', link: '/en/appendix/b-code' },
          { text: 'C · Glossary and Notation', link: '/en/appendix/c-glossary' },
          { text: 'D · Further Reading', link: '/en/appendix/d-reading' },
          { text: 'E · Exercises and Answers', link: '/en/appendix/e-exercises' }
        ]
      }
    ]
  },
  outline: { level: [2, 3], label: 'On this page' },
  socialLinks: [{ icon: 'github', link: repoUrl }],
  search: {
    provider: 'local',
    options: {
      translations: {
        button: { buttonText: 'Search the book', buttonAriaLabel: 'Search the book' },
        modal: {
          displayDetails: 'Show details',
          resetButtonTitle: 'Clear search',
          backButtonTitle: 'Back',
          noResultsText: 'No results. Try “interval”, “roughness”, or “Markov”.',
          footer: {
            selectText: 'Open',
            selectKeyAriaLabel: 'Enter',
            navigateText: 'Switch results',
            navigateUpKeyAriaLabel: 'Arrow up',
            navigateDownKeyAriaLabel: 'Arrow down',
            closeText: 'Close',
            closeKeyAriaLabel: 'Escape'
          }
        }
      }
    }
  },
  footer: {
    message: 'Text licensed CC BY-NC-SA 4.0 · Code licensed MIT',
    copyright: `Music as Math · Programmer's Edition · v${VERSION}`
  },
  docFooter: { prev: 'Previous', next: 'Next' },
  darkModeSwitchLabel: 'Appearance',
  sidebarMenuLabel: 'Contents',
  returnToTopLabel: 'Back to top',
  lastUpdatedText: 'Last updated',
  notFound: {
    title: 'This page is out of tune',
    quote: '404: the page you requested may have been modulated into another key.',
    linkLabel: 'Back to home',
    linkText: 'Back to home'
  }
}

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
  themeConfig: zhThemeConfig,
  locales: {
    root: { label: '简体中文', lang: 'zh-CN' },
    en: {
      label: 'English',
      lang: 'en-US',
      link: '/en/',
      title: 'Music as Math',
      description:
        'Music as Mathematical Logic: An Axiomatic Theory of Music from Vibration to Structure. Programmer’s Edition.',
      themeConfig: enThemeConfig
    }
  }
})
