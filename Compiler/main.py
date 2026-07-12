import sys
from pathlib import Path

from lex import lexer
from parser import Parser
from c99 import C99Codegen


def compile_file(source_path: Path):
    code = source_path.read_text(encoding="utf-8")

    tokens = list(lexer(code))
    ast = Parser(tokens).parse()

    c_code = C99Codegen().generate(ast)

    output_path = source_path.with_suffix(".c")
    output_path.write_text(c_code, encoding="utf-8")

    print(f"Compiled: {source_path}")
    print(f"Output  : {output_path}")


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("    python main.py <file.gcx>")
        sys.exit(1)

    source = Path(sys.argv[1])

    if not source.exists():
        print(f"File not found: {source}")
        sys.exit(1)

    if source.suffix != ".gcx":
        print("Input file must have .gcx extension")
        sys.exit(1)

    compile_file(source)


if __name__ == "__main__":
    main()
