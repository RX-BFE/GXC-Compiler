from dataclasses import dataclass
from typing import List, Union, Optional

# ===== Expression Types =====

Expression = Union[
    "Number",
    "String",
    "Identifier",
    "BinaryOp",
    "Parenthesized",
    "FunctionCall",
    "Index",
]

# ===== Statement Types =====

Statement = Union[
    "Let",
    "Assign",
    "Print",
    "FunctionDecl",
    "Return",
    "If",
    "Elif",
    "Else",
    "For",
]

# ===== Expressions =====


@dataclass
class Number:
    value: int


@dataclass
class String:
    value: str


@dataclass
class Identifier:
    name: str


@dataclass
class BinaryOp:
    left: Expression
    op: str
    right: Expression


@dataclass
class Parenthesized:
    expr: Expression


@dataclass
class FunctionCall:
    name: str
    args: List[Expression]


@dataclass
class Index:
    target: Expression
    index: Expression


@dataclass
class FunctionDecl:
    name: str
    params: List[str]
    body: List[Statement]


@dataclass
class Return:
    value: Expression


@dataclass
class If:
    condition: Expression
    body: List[Statement]
    elifs: List["Elif"]
    else_body: Optional[List[Statement]]


@dataclass
class Elif:
    condition: Expression
    body: List[Statement]


@dataclass
class Else:
    body: List[Statement]


@dataclass
class For:
    init: Statement
    condition: Expression
    post: Statement
    body: List[Statement]


# ===== Statements =====


@dataclass
class Let:
    name: str
    value: Expression


@dataclass
class Assign:
    name: str
    value: Expression


@dataclass
class Print:
    value: Expression


@dataclass
class Program:
    body: List[Statement]
