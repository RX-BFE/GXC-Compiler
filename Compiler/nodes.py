from dataclasses import dataclass
from typing import List, Union

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

Statement = Union["Let", "Assign", "Print", "FunctionDecl", "Return"]

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
