---
title: 项目文档
permalink: /
---

{% include navigation.html %}

# PyGit

用 Python 实现一个小型版本控制工具，逐步理解 Git 如何保存文件、记录状态和组织历史。

这是一个学习项目。你可以从命令行操作开始，也可以直接阅读实现，跟随文件内容如何变成一个可寻址的对象。

## 从这里开始

| 我想了解…… | 阅读文档 |
| --- | --- |
| 如何初始化仓库、暂存文件 | [使用说明]({{ '/guide/' | relative_url }}) |
| Blob、SHA-1 和暂存区如何工作 | [实现原理]({{ '/internals/' | relative_url }}) |
| 如何修改页面、添加文章与发布网站 | [编辑文档]({{ '/editing/' | relative_url }}) |

## 当前进度

| 功能 | 状态 |
| --- | --- |
| `init`：创建 `.pygit/` 仓库 | 已实现 |
| `add`：暂存单个文件或递归暂存目录 | 已实现 |
| Blob 对象的 SHA-1 计算、压缩和读取 | 已实现 |
| JSON 暂存区索引 | 已实现 |
| `commit`：创建提交记录 | 参数入口已提供，提交逻辑尚未实现 |
| 查看历史、分支切换与远程同步 | 尚未实现 |

## 一个最小示例

在项目根目录执行：

```bash
python3 main.py init
printf 'Hello, PyGit!\n' > hello.txt
python3 main.py add hello.txt
```

命令会创建 `.pygit/`，将文件内容保存为压缩的 Blob 对象，并更新暂存区索引。

完整操作步骤见[使用说明]({{ '/guide/' | relative_url }})。

## 关于这份文档

网站采用官方 [Minimal 主题](https://pages-themes.github.io/minimal/)。所有正文都是仓库 `docs/` 目录里的 Markdown 文件，可以在本地编辑，也可以使用每页底部的编辑链接。

[查看项目源码](https://github.com/kosmigen/PyGit) · [MIT 许可证](https://github.com/kosmigen/PyGit/blob/main/LICENSE)

{% include edit-link.html %}
