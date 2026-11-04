---
title: 实现原理
permalink: /internals/
---

{% include navigation.html %}

# 实现原理

## 代码入口

| 文件或类 | 职责 |
| --- | --- |
| `main.py` | 使用 `argparse` 解析 `init`、`add`、`commit` 并调用仓库对象 |
| `GitObject` | 计算对象哈希，压缩与反序列化对象数据 |
| `Blob` | 表示文件原始内容，继承自 `GitObject` |
| `GitRepository` | 初始化仓库、存储对象、维护暂存区索引 |

对象与仓库类位于 `object.py`。

## 仓库数据结构

```text
.pygit/
├── HEAD
├── index
├── objects/
│   └── <哈希前两位>/
│       └── <哈希剩余部分>
└── refs/
    └── heads/
```

- `HEAD`：初始化时写入 `ref: refs/heads/kosmigen`。目前尚未创建实际的分支引用文件。
- `index`：JSON 文件，记录“文件相对路径 → Blob 哈希”。
- `objects/`：按内容哈希保存的压缩对象。
- `refs/heads/`：为后续分支引用预留的目录。

这里的 `index` 是为了便于学习使用的 JSON 格式，与正式 Git 的二进制索引格式不同。

## 文件如何变成 Blob

暂存文件时，程序先读取文件的原始字节，再构造对象数据：

```text
<type> <size>\0<content>
```

对于 Blob，`type` 为 `blob`，`size` 为内容的字节长度，`\0` 表示一个空字节。

程序对这份数据计算 SHA-1，并用 zlib 压缩同样的数据。哈希的前两位作为子目录名，剩余部分作为文件名，最后更新暂存区索引。

文件路径保存到索引中，不包含在 Blob 内容里。因此，同样的内容即使来自不同文件，也会得到同样的对象哈希。

## add 的执行过程

1. 读取单个文件，或递归遍历目录中的文件。
2. 根据文件字节创建 `Blob`。
3. 调用 `_store_object()` 计算哈希并写入压缩对象。
4. 更新路径与哈希的对应关系。
5. 将索引保存到 `.pygit/index`。

`GitObject.deserialize()` 会执行相反的操作：解压数据，分离头部与内容，校验声明长度，返回对象。

## 后续可补充的内容

下面是供后续开发时扩写的文档位置，尚不代表已实现的功能：

- Tree 对象如何组织目录与文件。
- Commit 对象如何关联 Tree、父提交与作者信息。
- 提交后如何更新分支引用。
- 如何查看历史、还原文件与管理分支。

{% include edit-link.html %}
