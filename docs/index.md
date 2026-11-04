---
title: Git 是如何工作的？
permalink: /
---

- Git 如何保存一个文件的内容？
- 相同内容为什么会得到相同的对象哈希？
- 文件修改后，旧版本保存在什么地方？
- `add` 之后，暂存区究竟记录了什么？
- 一个目录如何被组织成完整的快照？
- 提交记录、分支和 `HEAD` 之间是什么关系？

为了理解这些问题，我用 Python 实现一个小型版本控制工具，并在这里记录它的实现过程。

PyGit 从最简单的对象存储开始，逐步探索暂存区、目录快照与提交历史。当前已经实现仓库初始化、文件暂存和 Blob 存储，提交逻辑仍在开发中。

<h2 class="contents-heading" id="chapters">Table of Contents</h2>

{% include chapter-list.html %}

你可以从第一篇开始阅读，也可以直接选择感兴趣的部分。每篇文章的开头和结尾都提供 Previous / Next 导航。
