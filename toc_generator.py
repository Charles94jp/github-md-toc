import re


class TOCGenerator:
    def __init__(self, path: str) -> None:
        self._path = path
        self._compile = re.compile(r'(#{1,}) (.*)')
        self._toc = {}

    def generate(self, issue=False):
        self._issue() if issue else self._readme()

    def _readme(self):
        """
        为GitHub readme.md中的markdown生成目录, 如果有vscode，可以使用 Markdown All in One 插件生成

        :return:
        """
        print('Generate TOC for GitHub README.md\n')
        with open(self._path, 'r', encoding='utf-8') as f:
            l = f.readline()
            while l:
                match = self._compile.match(l)
                if match:
                    level = len(match.group(1))
                    self._toc[match.group(2).strip()] = level
                l = f.readline()
        for k, v in self._toc.items():
            print(rf'{(v - 1) * 2 * " "}- [{k}](#{TOCGenerator._generate_link(k)})')

    def _issue(self):
        """
        为GitHub Issue中的markdown生成目录，由于Issue中的 ## 标题无法定位，需要改写为<h2 id="">的形式，所以会输出一个替换好标题的文件

        :return:
        """
        print('Generate TOC for GitHub issue\n')
        out_path = self._path + '.convert_toc.md'
        with open(self._path, 'r', encoding='utf-8') as fin:
            with open(out_path, 'w', encoding='utf-8') as fout:
                l = fin.readline()
                while l:
                    match = self._compile.match(l)
                    if match:
                        level = len(match.group(1))
                        title = match.group(2).strip()
                        tag_id = TOCGenerator._generate_link(title)
                        self._toc[title.replace('[', r'\[').replace(']', r'\]')] = {'level': level,
                                                                                    'link': f'user-content-{tag_id}'}
                        l = f'<h{level} id="{tag_id}">{title}</h{level}>\n'
                    fout.write(l)
                    l = fin.readline()
        for k, v in self._toc.items():
            print(rf'{(v.get("level") - 1) * 2 * " "}- [{k}](#{v.get("link")})')

    @staticmethod
    def _generate_link(title: str):
        """
        删除标题中的特殊字符

        :param title:
        :return:
        """
        title = title.lower().strip()
        r = []
        for s in title:
            if s == '-' or s == '_':
                r.append(s)
                continue
            if s == ' ':
                r.append('-')
                continue
            i = ord(s)
            if 32 < i < 48 or 57 < i < 65 or 90 < i < 97 or 122 < i < 127:
                continue
            r.append(s)
        return ''.join(r)
