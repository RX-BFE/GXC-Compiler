import re
from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str


TOKEN_REGEX = [
    ("LET", r"\blet\b"),
    ("PRINT", r"\bprint\b"),
    ("FUNC", r"\bfunc\b"),
    ("RETURN", r"\breturn\b"),
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
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
    ("MISMATCH", r"."),
]

master_pattern = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_REGEX)


def lexer(code):
    # Token type mapping for direct token types
    direct_token_types = {
        "LET",
        "PRINT",
        "FUNC",
        "RETURN",
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
    }

    for match in re.finditer(master_pattern, code):
        kind = match.lastgroup
        value = match.group()

        if kind == "SKIP":
            continue
        elif kind == "NEWLINE":
            yield Token("NEWLINE", "\\n")
        elif kind in direct_token_types:
            yield Token(kind, value)
        elif kind == "MISMATCH":
            raise SyntaxError(f"Karakter tidak dikenal: {value}")
