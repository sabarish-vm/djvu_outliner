import argparse
from pathlib import Path
from djvu_outliner.loader import parser
import sys


def cli(argv):
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-i",
        required=True,
        nargs=1,
        type=Path,
        help="Path to the input file",
        dest="input",
    )
    argparser.add_argument(
        "-o",
        required=True,
        nargs=1,
        type=Path,
        help="Path to the output file",
        dest="output",
    )

    args = argparser.parse_args(argv[1:])
    return args


def djvu_outline(obj, indent=""):
    result = []

    title_line = f'{indent}("{obj.data.sub}" "#{obj.data.page}"'

    if obj.children:
        result.append(title_line + "\n")
        for child in obj.children:
            result.extend(djvu_outline(child, indent + "  "))
        result.append(f"{indent})\n")
    else:
        result.append(title_line + ")\n")

    return result


def runner(args):
    root = parser(inputfile=args.input[0])
    final = "(bookmarks\n"
    for child in root.children:
        final += "".join(djvu_outline(child, "  ")) + "\n"
    final += ")"

    with open(args.output[0], "w") as f:
        f.write(final)


def main():
    runner(cli(sys.argv))


if __name__ == "__main__":
    main()
