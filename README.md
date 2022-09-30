<h1 align="center">GitHub MD TOC</h1>
Generate table of contents for GitHub readme.md and issue. 支持中文

## Usage

```powershell
# Print the table of contents for GitHub readme.md
python main.py [file_path]

# Print the table of contents for GitHub issue, output file [file_path].convert_toc.md simultaneously
python main.py [file_path] -i
```

GitHub issue 中必须使用`<h2 id="2">`格式的标题才能定位

[>> issue example](https://github.com/Charles94jp/github-md-toc/issues/1)