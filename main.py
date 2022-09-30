import sys

from toc_generator import TOCGenerator


def main():
    """
    脚本总是需要一个文件目录参数，如果在目录参数后还有参数，则将启用issue模式，否则启用readme模式

    :return:
    """
    generator = TOCGenerator(sys.argv[1])
    generator.generate(issue=True if len(sys.argv) ==3 and sys.argv[2] == '-i' else False)


if __name__ == '__main__':
    main()
