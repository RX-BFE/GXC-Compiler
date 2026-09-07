from dataclasses import dataclass
from typing import Optional


@dataclass
class CompileError(Exception):
    message: str
    source: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None

    def __str__(self) -> str:
        parts = []

        if self.source:
            parts.append(self.source)

        if self.line is not None and self.column is not None:
            parts.append(f"{self.line}:{self.column}")

        location = ":".join(parts)
        if location:
            return f"{location}: {self.message}"
        return self.message

    def has_position(self) -> bool:
        """Return True when the error carries line/column information."""
        return self.source is not None and self.line is not None and self.column is not None


def format_compile_error(error: CompileError, source_text: Optional[str] = None) -> str:
    """Render a concise compiler diagnostic with optional source context."""
    if not error.has_position():
        return f"Error: {error.message}"

    assert error.source is not None
    assert error.line is not None
    assert error.column is not None

    lines = [f"Error: {error.message}", f" --> {error.source}:{error.line}:{error.column}"]

    if source_text is None:
        return "\n".join(lines)

    source_lines = source_text.splitlines()
    if error.line < 1 or error.line > len(source_lines):
        return "\n".join(lines)

    line_text = source_lines[error.line - 1].replace("\t", "    ")
    line_no = str(error.line)
    gutter_width = len(str(len(source_lines)))
    caret_offset = max(error.column - 1, 0)
    caret_line = " " * caret_offset + "^"

    lines.append(f"{line_no.rjust(gutter_width)} | {line_text}")
    lines.append(f"{' ' * gutter_width} | {caret_line}")
    return "\n".join(lines)


class LexError(CompileError):
    pass


class ParseError(CompileError):
    pass


class CodegenError(CompileError):
    pass
