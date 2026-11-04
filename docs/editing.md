---
title: 编辑与发布文档
permalink: /editing/
---

## 修改现有内容

直接用编辑器打开仓库中的 Markdown 文件：

| 文件 | 网站中的内容 |
| --- | --- |
| `docs/index.md` | 文档首页、项目介绍与章节目录 |
| `docs/guide.md` | 使用说明与命令示例 |
| `docs/internals.md` | 代码结构与实现原理 |
| `docs/editing.md` | 本页：编辑与发布方法 |
| `docs/_data/chapters.yml` | 首页章节目录、章节顺序和上下篇 |
| `docs/_config.yml` | 网站标题、描述、系列介绍卡片和网站地址 |
| `docs/_includes/series-card.html` | 使用 daisyUI 图片卡片的左侧系列介绍 |
| `docs/wheels.md`、`docs/_data/wheels.yml` | “More Projects”的系列目录及项目列表 |

每页开头 `---` 之间的内容是页面配置；其余正文按 Markdown 编写。模板会自动显示页面标题、侧边导航、上下篇和编辑入口，正文中不需要重复编写它们。正文的小节从 `##` 开始即可。

也可以点击每页底部的 **Edit this page**，登录 GitHub 后在线修改。有仓库写入权限时可以直接提交；其他访问者可按 GitHub 提示通过 Fork 和 Pull Request 提交修改。

GitHub Pages 展示发布后的内容，编辑入口会打开 GitHub 的源文件编辑页面。

## 章节目录与上下篇如何生成

首页目录和每篇文章开头、结尾的上下篇，共用 `docs/_data/chapters.yml`。列表的先后顺序就是阅读顺序，不依赖文件名和发布日期：

```yaml
- title: 使用说明
  url: /guide/
  description: 从初始化仓库开始，动手暂存文件和目录。
- title: 实现原理
  url: /internals/
  description: 理解 Blob 对象、内容寻址与暂存区索引。
```

调整这里的顺序，首页目录和所有文章的上下篇会一起更新。首篇只显示 **Next**，末篇只显示 **Previous**，不会循环跳转。文章标题和目录自动使用 `Part 1 - 标题` 的格式，页面不显示 `1/3` 这样的进度计数。左侧 **Overview** 始终返回首页。

只有加入这份列表的页面才显示上下篇。普通介绍页可以只创建 Markdown，不加入列表。左侧只保留 **Overview** 和 **View on GitHub** 两个导航入口，定义在 `docs/_includes/navigation.html`；正文顶部不再显示单独的菜单栏。

## 常用 Markdown 写法

````markdown
## 一个小节

这里写正文，可以使用 **加粗**、*斜体* 和 `行内代码`。

- 第一项
- 第二项

```python
print("Hello, PyGit!")
```

[外部链接](https://github.com/kosmigen/PyGit)
````

图片可以保存在 `docs/assets/images/`，再使用下面的写法引用：

```liquid
{% raw %}![图片说明]({{ '/assets/images/example.png' | relative_url }}){% endraw %}
```

上面的图片路径是示例，使用前请放入自己的图片。`relative_url` 会自动加上 `/PyGit` 项目路径。

## 添加一个新章节

例如，在 `docs/` 下新建 `notes.md`，内容如下：

```markdown
---
title: 开发笔记
permalink: /notes/
---

在这里记录你的开发过程。

## 第一次实现记录

这里写这一小节的正文。
```

然后在 `docs/_data/chapters.yml` 的适当位置加入：

```yaml
- title: 开发笔记
  url: /notes/
  description: 记录开发过程、遇到的问题和解决方法。
```

这里的 `url` 必须与新文件的 `permalink` 完全一致，包括结尾的 `/`。提交并推送新文件和章节列表后，首页就会出现新章节，上下篇链接也会自动更新，无需修改其他文章。

正文中链接到该页面时，使用：

```liquid
{% raw %}[开发笔记]({{ '/notes/' | relative_url }}){% endraw %}
```

## 首次发布到 GitHub Pages

1. 使用真正的 Git，将这些文档文件提交并推送到 `kosmigen/PyGit` 仓库的 `main` 分支。
2. 在 GitHub 仓库中打开 **Settings → Pages**。
3. 在 **Build and deployment → Source** 选择 **Deploy from a branch**。
4. 分支选择 **main**，文件夹选择 **/docs**，点击 **Save**。
5. 等待构建完成后，从 Pages 设置页打开网站。

按当前仓库地址，网站预期发布到：<https://kosmigen.github.io/PyGit/>。首次发布可能需要数分钟，实际状态以 GitHub 的 Pages 设置和 Actions 记录为准。

启用后，每次将文档变更推送到 `main`，GitHub Pages 会重新构建网站。只有本地编辑、尚未提交推送时，线上页面不会更新。

## 本地预览（可选）

只编辑 Markdown 不需要安装 Ruby。若要在电脑上预览完整的 Minimal 主题，需要先安装兼容的 Ruby 和 Bundler，然后在项目根目录运行：

```bash
cd docs
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve
```

在浏览器打开 <http://localhost:4000/PyGit/>。按 `Ctrl+C` 停止预览；修改 `_config.yml` 后需要重启预览服务。

Ruby 依赖只用于文档网站的本地预览，不影响 Python 程序。构建产物与本地依赖已由 `docs/.gitignore` 忽略。

## 修改网站名称与主题样式

- 在 `docs/_config.yml` 修改 `title` 和 `description`。
- 左侧“Build Your Own X From Scratch”使用 [daisyUI 官方 Card](https://daisyui.com/components/card/) 和 [Button](https://daisyui.com/components/button/)。文案由 `_config.yml` 中的 `series` 配置控制：`title` 是卡片标题，`description` 是正文，`image` 和 `image_alt` 控制图片区，`link_text` 和 `url` 控制按钮。所有保留的配置字段都会实际用于页面。
- 当前使用 `theme: jekyll-theme-minimal`，保留该配置即可继续使用指定主题。
- `docs/assets/css/style.scss` 先导入官方主题，再补充侧栏、正文和纯文字导航样式。页面顶部和上下篇之间不添加分隔线。
- `docs/_layouts/default.html` 定义左侧网站信息、系列卡片和右侧正文区域。`docs/_includes/series-card.html` 是系列卡片模板；标题和说明保持普通文字，只有阅读入口使用链接。
- `docs/assets/vendor/daisyui-5.7.50/` 保存由官方 daisyUI 插件和 Tailwind CSS 编译的卡片、按钮样式，以及版本和构建记录。卡片使用默认 light 主题，站点样式只设置它在侧栏中的宽度和位置。
- “More Projects”指向本站 `/wheels/`。要加入新项目，在 `docs/_data/wheels.yml` 添加项目名、简介、语言和地址即可。
- `docs/_layouts/documentation.html` 负责统一组合标题、正文、上下篇和编辑入口。普通内容修改不需要编辑模板。
- 如果仓库改名、迁移到其他账号或更换分支，请同步更新 `_config.yml` 中的地址配置。

官方参考：[Minimal 主题](https://github.com/pages-themes/minimal) · [GitHub Pages 发布源设置](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
