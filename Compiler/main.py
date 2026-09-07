import sys
from pathlib import Path

try:
    from .errors import CompileError, format_compile_error
    from .lex import lexer
    from .parser import Parser
    from .c99 import C99Codegen
except ImportError:  # pragma: no cover - direct script execution fallback
    from errors import CompileError, format_compile_error
    from lex import lexer
    from parser import Parser
    from c99 import C99Codegen


def compile_file(source_path: Path) -> int:
    """Compile a .gxc file to .c file. Returns exit code."""
    try:
        code = source_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"Error: Unable to read file (encoding issue): {source_path}")
        return 1
    except IOError as e:
        print(f"Error: Unable to read file: {e}")
        return 1

    try:
        tokens = list(lexer(code, source=str(source_path)))
        ast = Parser(tokens).parse()
        c_code = C99Codegen().generate(ast)
    except CompileError as e:
        print(format_compile_error(e, code))
        return 1
    except Exception as e:
        print(f"Compilation Error: {e}")
        return 1

    try:
        output_path = source_path.with_suffix(".c")
        output_path.write_text(c_code, encoding="utf-8")
        print(f"Compiled: {source_path}")
        print(f"Output  : {output_path}")
    except IOError as e:
        print(f"Error: Unable to write output file: {e}")
        return 1

    return 0


def main() -> int:
    """Main entry point. Returns exit code."""
    if len(sys.argv) != 2:
        print("Usage:")
        print("    gxc <file.gxc>")
        return 1

    source = Path(sys.argv[1])

    if not source.exists():
        print(f"Error: File not found: {source}")
        return 1

    if not source.is_file():
        print(f"Error: Path is not a file: {source}")
        return 1

    if source.suffix != ".gxc":
        print("Error: Input file must have .gxc extension")
        return 1

    return compile_file(source)


if __name__ == "__main__":
    sys.exit(main())
