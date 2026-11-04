# PyGit

用 Python 实现一个小型版本控制工具，逐步理解 Git 的对象存储、暂存区和提交机制。

当前已实现仓库初始化、文件与目录暂存、Blob 对象的 SHA-1 寻址和 zlib 压缩；`commit` 命令已提供参数入口，提交逻辑尚未实现。

## 快速开始

在项目根目录执行（示例使用 macOS / Linux 命令）：

```bash
python3 main.py --help
python3 main.py init
printf 'Hello, PyGit!\n' > hello.txt
python3 main.py add hello.txt
```

PyGit 使用 `.pygit/` 存放数据，与 Git 的 `.git/` 目录区分。建议使用 Python 3.9 或更新版本，运行只依赖 Python 标准库。

## 项目文档

- [文档首页](docs/index.md)
- [使用说明](docs/guide.md)
- [实现原理](docs/internals.md)
- [编辑与发布指南](docs/editing.md)

文档网站采用 [GitHub Pages Minimal 主题](https://pages-themes.github.io/minimal/)，源文件位于 `docs/`，可以直接编辑 Markdown。

启用 GitHub Pages 后，网站预期地址为 <https://kosmigen.github.io/PyGit/>。首次发布设置见[编辑与发布指南](docs/editing.md#首次发布到-github-pages)。

## 项目结构

```text
PyGit/
├── main.py          # 命令行参数与命令分发
├── object.py        # 对象模型、仓库与暂存区
├── test/            # 示例与练习文件
└── docs/            # 可编辑的项目文档与 Minimal 主题配置
```

## 许可证

[MIT](LICENSE)
