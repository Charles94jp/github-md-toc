import re
import sys


class TOCGenerator:
    def __init__(self, path: str) -> None:
        self._path = path
        self._compile = re.compile(r'(#{1,}) (.*)')
        self._cm_compile = re.compile(r'(`{3,}).*')
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
            comment = -1
            while l:
                match = self._compile.match(l)
                cmatch = self._cm_compile.match(l)
                if cmatch:
                    if comment == -1:
                        comment = len(cmatch.group(1))
                    elif comment == len(cmatch.group(1)):
                        comment = -1
                if comment == -1 and match:
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
                comment = -1
                while l:
                    # 判断是否是标题
                    match = self._compile.match(l)
                    # 判断是否是注释
                    cmatch = self._cm_compile.match(l)
                    if cmatch:
                        if comment == -1:
                            comment = len(cmatch.group(1))
                        elif comment == len(cmatch.group(1)):
                            comment = -1
                    if comment == -1 and match:
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


def main():
    """
    脚本总是需要一个文件目录参数，如果在目录参数后还有参数，则将启用issue模式，否则启用readme模式

    :return:
    """
    generator = TOCGenerator(sys.argv[1])
    generator.generate(issue=True if len(sys.argv) == 3 and sys.argv[2] == '-i' else False)


if __name__ == '__main__':
    main()
