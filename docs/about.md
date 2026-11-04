# 关于这本书

## 它是什么

《**音乐的数理逻辑：从振动到结构的公理化乐理**》是一个开源网络书籍项目。它试图用一本「计算机科学教材」的组织方式重写音乐理论：

- **公理化**：定义、公设、定理，而不是「记住这条规则」；
- **可计算**：每个结论都有对应的 Python 实现；
- **可交互**：关键概念配有可拖动的演示组件；
- **可部署**：VitePress + GitHub Actions，fork 之后 push 一下就能有自己的版本。

## 它不是什么

这不是一本教你怎么弹琴的书，也不是一本音乐史。它不会告诉你「这个和弦要这样按」，但会告诉你「为什么这样按在声学上是划算的」。

## 作者与致谢

本书由一群相信「审美可以被部分解释」的人共同完成。章节结构参考了 Helmholtz《On the Tones of Sensation》、Sethares《Tuning, Timbre, Spectrum, Scale》与 Plomp & Levelt 1965 年的经典论文；数学处理上尽量保持可手算。

## 许可

| 内容 | 协议 |
| --- | --- |
| 正文与插图 | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh) |
| 代码示例 | [MIT](https://opensource.org/licenses/MIT) |

你可以自由地复制、分发、改编本书用于非商业目的，只需保留署名并以相同协议共享。

## 技术栈

```text
VitePress 1.6  →  Markdown + Vue 3 + MathJax 渲染
GitHub Actions →  构建 + 部署到 Pages
Python 3.12    →  所有数值验证
```

## 参与贡献

发现公式写错了、代码跑不通、或者某一章的解释不够清楚？欢迎提 Issue 或 PR：

1. Fork 本仓库；
2. 新建分支 `fix/ch03-typo`；
3. 修改 `docs/` 下的 Markdown；
4. 本地 `pnpm dev` 预览无误后提交 PR。

> 所有贡献默认接受上述 CC BY-NC-SA 4.0 协议。
