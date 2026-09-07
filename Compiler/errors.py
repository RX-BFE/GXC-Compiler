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


class LexError(CompileError):
    pass


class ParseError(CompileError):
    pass


class CodegenError(CompileError):
    pass
