import re
from dataclasses import dataclass
from typing import Optional

from errors import LexError


@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int
    source: Optional[str] = None

TOKEN_REGEX = [
    ("LET", r"\blet\b"),
    ("PRINT", r"\bprint\b"),
    ("FUNC", r"\bfunc\b"),
    ("RETURN", r"\breturn\b"),
    ("IF", r"\bif\b"),
    ("ELIF", r"\belif\b"),
    ("ELSE", r"\belse\b"),
    ("FOR", r"\bfor\b"),
    ("COMPARE", r"==|!=|<=|>=|<|>"),
    ("NUMBER", r"\b\d+\b"),
    ("IDENT", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("STRING", r'"[^"]*"'),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("STAR", r"\*"),
    ("SLASH", r"/"),
    ("PERCENT", r"%"),
    ("EQUAL", r"="),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("COMMA", r","),
    ("SEMICOLON", r";"),
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
    ("MISMATCH", r"."),
]


master_pattern = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_REGEX)


def lexer(code, source: Optional[str] = None):
    return _lexer(code, source=source)


def _lexer(code, source: Optional[str] = None):
    # Token type mapping for direct token types
    direct_token_types = {
        "LET",
        "PRINT",
        "FUNC",
        "RETURN",
        "IF",
        "ELIF",
        "ELSE",
        "FOR",
        "COMPARE",
        "NUMBER",
        "IDENT",
        "STRING",
        "PLUS",
        "MINUS",
        "STAR",
        "SLASH",
        "PERCENT",
        "EQUAL",
        "LPAREN",
        "RPAREN",
        "LBRACE",
        "RBRACE",
        "LBRACKET",
        "RBRACKET",
        "COMMA",
        "SEMICOLON",
    }

    line = 1
    column = 1

    for match in re.finditer(master_pattern, code):
        kind = match.lastgroup
        value = match.group()
        token_line = line
        token_column = column

        for char in value:
            if char == "\n":
                line += 1
                column = 1
            else:
                column += 1

        if kind == "SKIP":
            continue
        elif kind == "NEWLINE":
            yield Token("NEWLINE", "\\n", token_line, token_column, source)
        elif kind in direct_token_types:
            yield Token(kind, value, token_line, token_column, source)
        elif kind == "MISMATCH":
            raise LexError(f"Karakter tidak dikenal: {value}", source, token_line, token_column)
