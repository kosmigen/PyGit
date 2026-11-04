---
title: 使用说明
permalink: /guide/
---

{% include navigation.html %}

# 使用说明

## 运行环境

- 建议使用 Python 3.9 或更新版本。
- 当前程序只使用 Python 标准库，无需安装额外的 Python 依赖。
- 以下命令示例适用于 macOS / Linux，默认在 PyGit 项目根目录运行。

查看帮助：

```bash
python3 main.py --help
python3 main.py add --help
```

## 初始化仓库

```bash
python3 main.py init
```

默认在当前目录创建 `.pygit/`。也可以初始化一个已经存在的目录：

```bash
mkdir -p demo
python3 main.py init demo
```

当前实现不会自动创建不存在的父目录，所以应先创建目标目录。

## 暂存文件和目录

```bash
printf 'Hello, PyGit!\n' > hello.txt
python3 main.py add hello.txt
```

一次暂存多个路径：

```bash
python3 main.py add main.py object.py
```

递归暂存目录：

```bash
python3 main.py add test/
```

暂存后，文件内容写入 `.pygit/objects/`，相对路径与对象哈希的对应关系写入 `.pygit/index`。修改文件后重新运行 `add`，可以更新该文件在索引中的哈希值。

## 查看暂存区

```bash
python3 -m json.tool .pygit/index
```

索引是一个 JSON 字典，键为仓库内的相对路径，值为对应 Blob 对象的 SHA-1 哈希值。

## 在另一个目录使用 PyGit

`add` 等命令以当前工作目录作为仓库位置。如果初始化了 `demo/`，需要切换到该目录后操作：

```bash
mkdir -p demo
python3 main.py init demo
cd demo
printf 'Hello from demo!\n' > hello.txt
python3 ../main.py add hello.txt
cd ..
```

当前实现不会向上查找父目录中的 `.pygit/`。

## 关于 commit

命令行已经接受下面的参数：

```bash
python3 main.py commit -m "第一次提交"
```

**当前 `GitRepository.commit()` 只有占位内容，运行此命令还不会生成提交记录。** 等提交逻辑实现后，可在这里补充实际输出和操作示例。

## 当前限制

- 使用 `.pygit/` 数据目录，目前不能替代完整 Git，也不能直接推送到 GitHub。
- 递归暂存目录会跳过 `.git/` 和 `.pygit/`，尚未解析 `.gitignore`。
- 当前没有完整的文件删除、提交、历史与分支操作。
- 重复暂存修改后的文件会留下旧对象，目前没有垃圾回收功能。

项目源码与文档的提交、推送仍需使用真正的 Git。

{% include edit-link.html %}
