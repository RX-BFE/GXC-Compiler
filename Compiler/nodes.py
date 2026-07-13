from dataclasses import dataclass

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
    left: object
    op: str
    right: object

@dataclass
class Parenthesized:
    expr: object

@dataclass
class FunctionCall:
    name: str
    args: list

@dataclass
class Index:
    target: object
    index: object

@dataclass
class FunctionDecl:
    name: str
    params: list
    body: list

@dataclass
class Return:
    value: object


# ===== Statements =====

@dataclass
class Let:
    name: str
    value: object

@dataclass
class Assign:
    name: str
    value: object

@dataclass
class Print:
    value: object

@dataclass
class Program:
    body: list
