---
title: 编辑与发布文档
permalink: /editing/
---

{% include navigation.html %}

# 编辑与发布文档

## 修改现有内容

直接用编辑器打开仓库中的 Markdown 文件：

| 文件 | 网站中的内容 |
| --- | --- |
| `docs/index.md` | 文档首页、项目介绍与功能进度 |
| `docs/guide.md` | 使用说明与命令示例 |
| `docs/internals.md` | 代码结构与实现原理 |
| `docs/editing.md` | 本页：编辑与发布方法 |
| `docs/_config.yml` | 网站标题、描述、导航和地址 |

每页开头 `---` 之间的内容是页面配置；其余正文按 Markdown 编写。页面中 `{% raw %}{% include ... %}{% endraw %}` 用于显示导航和编辑入口，修改正文时保留即可。

也可以点击每页底部的 **在 GitHub 上编辑本页**，登录 GitHub 后在线修改。有仓库写入权限时可以直接提交；其他访问者可按 GitHub 提示通过 Fork 和 Pull Request 提交修改。

GitHub Pages 展示发布后的内容，编辑入口会打开 GitHub 的源文件编辑页面。

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

## 添加一个新页面

例如，在 `docs/` 下新建 `notes.md`，内容如下：

```liquid
{% raw %}---
title: 开发笔记
permalink: /notes/
---

{% include navigation.html %}

# 开发笔记

在这里记录你的开发过程。

{% include edit-link.html %}{% endraw %}
```

然后在 `docs/_config.yml` 的 `navigation` 列表中追加：

```yaml
  - title: 开发笔记
    url: /notes/
```

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
- 当前使用 `theme: jekyll-theme-minimal`，保留该配置即可继续使用指定主题。
- `docs/assets/css/style.scss` 先导入官方主题，再补充导航与编辑入口样式。需要微调时可在文件末尾追加 CSS。
- 如果仓库改名、迁移到其他账号或更换分支，请同步更新 `_config.yml` 中的地址配置。

官方参考：[Minimal 主题](https://github.com/pages-themes/minimal) · [GitHub Pages 发布源设置](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

{% include edit-link.html %}
