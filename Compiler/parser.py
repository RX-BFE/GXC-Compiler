from typing import List, Optional
from lex import Token
from nodes import (
    Program,
    Let,
    Assign,
    Print,
    FunctionDecl,
    Return,
    Number,
    String,
    Identifier,
    BinaryOp,
    Parenthesized,
    FunctionCall,
    Index,
    Expression,
    Statement,
    If,
    Elif,
    Else,
)


class Parser:
    """Parser for converting token stream into AST."""

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Optional[Token]:
        """Get current token without consuming it."""
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def eat(self, token_type: str) -> Token:
        """Consume and return current token if it matches expected type."""
        token = self.current()

        if token is None:
            raise SyntaxError(f"Unexpected EOF, expected {token_type}")

        if token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, got {token.type} at position {self.pos}"
            )

        self.pos += 1
        return token

    def skip_newlines(self) -> None:
        """Skip NEWLINE tokens."""
        while self.current() and self.current().type == "NEWLINE":
            self.pos += 1

    # ----------------------

    def parse(self) -> Program:
        """Parse entire token stream into a Program AST node."""
        body = []

        self.skip_newlines()

        while self.current():
            token = self.current()
            if token.type != "FUNC":
                raise SyntaxError(
                    f"Top-level statements are not allowed; expected FUNC, got {token.type} at position {self.pos}"
                )

            func_decl = self.func_declaration()
            if func_decl.name == "main" and func_decl.params:
                raise SyntaxError("main() must not take parameters")

            body.append(func_decl)
            self.skip_newlines()

        if not any(
            isinstance(stmt, FunctionDecl) and stmt.name == "main" for stmt in body
        ):
            raise SyntaxError("Program must define func main() { ... }")

        return Program(body)

    # ----------------------

    def statement(self) -> Statement:
        """Parse a single statement."""
        token = self.current()

        if token is None:
            raise SyntaxError("Unexpected EOF in statement")

        statement_map = {
            "LET": self.let_statement,
            "IDENT": self.assign_statement,
            "PRINT": self.print_statement,
            "FUNC": self.func_declaration,
            "RETURN": self.return_statement,
            "IF": self.if_statement,
        }

        parser_method = statement_map.get(token.type)
        if parser_method is None:
            raise SyntaxError(f"Unexpected token {token.type} at position {self.pos}")

        return parser_method()

    # ----------------------

    def let_statement(self) -> Let:
        """Parse let statement: let IDENT = expr"""
        self.eat("LET")
        name = self.eat("IDENT").value
        self.eat("EQUAL")
        expr = self.expression()
        return Let(name, expr)

    # ----------------------

    def assign_statement(self) -> Assign:
        """Parse assignment statement: IDENT = expr"""
        name = self.eat("IDENT").value
        self.eat("EQUAL")
        expr = self.expression()
        return Assign(name, expr)

    # ----------------------

    def print_statement(self) -> Print:
        """Parse print statement: print(expr)"""
        self.eat("PRINT")
        self.eat("LPAREN")
        expr = self.expression()
        self.eat("RPAREN")
        return Print(expr)

    # ----------------------

    def func_declaration(self) -> FunctionDecl:
        """Parse function declaration: func name(params) { body }"""
        self.eat("FUNC")
        name = self.eat("IDENT").value
        self.eat("LPAREN")

        # Parse parameters
        params = []
        if self.current() and self.current().type == "IDENT":
            params.append(self.eat("IDENT").value)
            while self.current() and self.current().type == "COMMA":
                self.eat("COMMA")
                params.append(self.eat("IDENT").value)

        self.eat("RPAREN")
        body = self.block("function body")
        return FunctionDecl(name, params, body)

    # ----------------------

    def return_statement(self) -> Return:
        """Parse return statement: return expr"""
        self.eat("RETURN")
        expr = self.expression()
        return Return(expr)

    # ----------------------

    def if_statement(self) -> If:
        """Parse if-elif-else statement: if cond { body } elif cond { body } else { body }"""
        self.eat("IF")
        condition = self.expression()
        body = self.block("if body")

        # Parse elif clauses
        elifs = []
        self.skip_newlines()
        while self.current() and self.current().type == "ELIF":
            elif_clause = self.elif_statement()
            elifs.append(elif_clause)
            self.skip_newlines()

        # Parse else clause (optional)
        else_body = None
        if self.current() and self.current().type == "ELSE":
            self.eat("ELSE")
            else_body = self.block("else body")

        return If(condition, body, elifs, else_body)

    def elif_statement(self) -> Elif:
        """Parse elif clause: elif cond { body }"""
        self.eat("ELIF")
        condition = self.expression()
        body = self.block("elif body")
        return Elif(condition, body)

    def block(self, context: str) -> List[Statement]:
        """Parse a required brace-delimited block."""
        self.skip_newlines()
        self.eat("LBRACE")

        body = []
        self.skip_newlines()
        while self.current() and self.current().type != "RBRACE":
            body.append(self.statement())
            self.skip_newlines()

        if self.current() is None:
            raise SyntaxError(f"Unexpected EOF, expected RBRACE to close {context}")

        self.eat("RBRACE")
        return body

    # ----------------------

    def expression(self) -> Expression:
        """Parse expression with comparison operators (lowest precedence)."""
        return self.comparison()

    def comparison(self) -> Expression:
        """Parse comparison operators: ==, !=, <, >, <=, >="""
        left = self.additive()
        while self.current() and self.current().type == "COMPARE":
            op = self.eat("COMPARE").value
            right = self.additive()
            left = BinaryOp(left, op, right)
        return left

    def additive(self) -> Expression:
        """Parse addition and subtraction."""
        left = self.term()

        while self.current() and self.current().type in ("PLUS", "MINUS"):
            op = self.eat(self.current().type).value
            right = self.term()
            left = BinaryOp(left, op, right)

        return left

    # ----------------------

    def term(self) -> Expression:
        """Parse expression with multiplication, division, and modulo operations."""
        left = self.factor()

        while self.current() and self.current().type in ("STAR", "SLASH", "PERCENT"):
            op = self.eat(self.current().type).value
            right = self.factor()
            left = BinaryOp(left, op, right)

        return left

    # ----------------------

    def factor(self) -> Expression:
        """Parse atomic expressions (numbers, strings, identifiers, function calls, index operations, and parenthesized expressions)."""
        token = self.current()

        if token is None:
            raise SyntaxError("Unexpected EOF in expression")

        if token.type == "NUMBER":
            return Number(int(self.eat("NUMBER").value))
        elif token.type == "STRING":
            # Remove quotes from string literal
            str_value = self.eat("STRING").value
            return String(str_value[1:-1])  # Remove surrounding quotes
        elif token.type == "LPAREN":
            # Parenthesized expression: (expr)
            self.eat("LPAREN")
            expr = self.expression()
            self.eat("RPAREN")
            return Parenthesized(expr)
        elif token.type == "IDENT":
            ident = Identifier(self.eat("IDENT").value)

            # Check for function call: ident()
            if self.current() and self.current().type == "LPAREN":
                self.eat("LPAREN")
                args = []
                # Parse arguments if present
                if self.current() and self.current().type != "RPAREN":
                    args.append(self.expression())
                    while self.current() and self.current().type == "COMMA":
                        self.eat("COMMA")
                        args.append(self.expression())
                self.eat("RPAREN")
                return FunctionCall(ident.name, args)

            # Check for index operation: ident[expr]
            elif self.current() and self.current().type == "LBRACKET":
                self.eat("LBRACKET")
                index_expr = self.expression()
                self.eat("RBRACKET")
                return Index(ident, index_expr)

            return ident
        else:
            raise SyntaxError(
                f"Unexpected token {token.type} in expression at position {self.pos}"
            )
