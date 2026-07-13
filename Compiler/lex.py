# lex.py

import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str

TOKEN_REGEX = [
    ("LET",      r"\blet\b"),
    ("PRINT",    r"\bprint\b"),
    ("FUNC",     r"\bfunc\b"),
    ("RETURN",   r"\breturn\b"),
    ("NUMBER",   r"\b\d+\b"),
    ("IDENT",    r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("STRING",   r'"[^"]*"'),
    ("PLUS",     r"\+"),
    ("EQUAL",    r"="),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("LBRACE",   r"\{"),
    ("RBRACE",   r"\}"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("COMMA",    r","),
    ("NEWLINE",  r"\n"),
    ("SKIP",     r"[ \t]+"),
    ("MISMATCH", r"."),
]

master_pattern = "|".join(
    f"(?P<{name}>{pattern})"
    for name, pattern in TOKEN_REGEX
)

def lexer(code):
    for match in re.finditer(master_pattern, code):
        kind = match.lastgroup
        value = match.group()

        # Pattern Matching
        match kind:
            case "SKIP":
                continue

            case "NEWLINE":
                yield Token("NEWLINE", "\\n")

            case "LET":
                yield Token("LET", value)

            case "PRINT":
                yield Token("PRINT", value)

            case "FUNC":
                yield Token("FUNC", value)

            case "RETURN":
                yield Token("RETURN", value)

            case "NUMBER":
                yield Token("NUMBER", value)

            case "IDENT":
                yield Token("IDENT", value)

            case "STRING":
                yield Token("STRING", value)

            case "PLUS":
                yield Token("PLUS", value)

            case "EQUAL":
                yield Token("EQUAL", value)

            case "LPAREN":
                yield Token("LPAREN", value)

            case "RPAREN":
                yield Token("RPAREN", value)

            case "LBRACE":
                yield Token("LBRACE", value)

            case "RBRACE":
                yield Token("RBRACE", value)

            case "LBRACKET":
                yield Token("LBRACKET", value)

            case "RBRACKET":
                yield Token("RBRACKET", value)

            case "COMMA":
                yield Token("COMMA", value)

            case "MISMATCH":
                raise SyntaxError(f"Karakter tidak dikenal: {value}")


