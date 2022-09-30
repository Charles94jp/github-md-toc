<h1 align="center">GitHub MD TOC</h1>
Generate table of contents for GitHub readme.md and issue. 支持中文

## Usage

```powershell
# Print the table of contents for GitHub readme.md
python main.py [file_path]

# Print the table of contents for GitHub issue, output file [file_path].convert_toc.md simultaneously
python main.py [file_path] -i
```

In GitHub issues, only titles in `<h2 id="2">` format can be located and jumped, using the `-i` option will generate a copy file where the title has been converted from `# xxx` to `<h id="xxx">xxx</h>`

GitHub issue 中必须使用`<h2 id="2">`格式的标题才能定位和跳转，使用`-i`选项会生成一个副本文件，其中的标题已经从`# xxx`转换为`<h id="xxx">xxx</h>`

[>> issue example](https://github.com/Charles94jp/github-md-toc/issues/1)