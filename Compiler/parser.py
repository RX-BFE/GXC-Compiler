from nodes import *

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def eat(self, token_type):
        token = self.current()

        if token is None:
            raise SyntaxError("Unexpected EOF")

        if token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, got {token.type}"
            )

        self.pos += 1
        return token

    def skip_newlines(self):
        while self.current() and self.current().type == "NEWLINE":
            self.pos += 1

    # ----------------------

    def parse(self):
        body = []

        self.skip_newlines()

        while self.current():
            body.append(self.statement())
            self.skip_newlines()

        return Program(body)

    # ----------------------

    def statement(self):

        token = self.current()

        match token.type:

            case "LET":
                return self.let_statement()

            case "IDENT":
                return self.assign_statement()

            case "PRINT":
                return self.print_statement()

            case _:
                raise SyntaxError(
                    f"Unexpected token {token.type}"
                )

    # ----------------------

    def let_statement(self):

        self.eat("LET")

        name = self.eat("IDENT").value

        self.eat("EQUAL")

        expr = self.expression()

        return Let(name, expr)

    # ----------------------

    def assign_statement(self):

        name = self.eat("IDENT").value

        self.eat("EQUAL")

        expr = self.expression()

        return Assign(name, expr)

    # ----------------------

    def print_statement(self):

        self.eat("PRINT")

        self.eat("LPAREN")

        expr = self.expression()

        self.eat("RPAREN")

        return Print(expr)

    # ----------------------

    def expression(self):

        left = self.term()

        while self.current() and self.current().type == "PLUS":

            op = self.eat("PLUS").value

            right = self.term()

            left = BinaryOp(left, op, right)

        return left

    # ----------------------

    def term(self):

        token = self.current()

        match token.type:

            case "NUMBER":
                return Number(
                    int(self.eat("NUMBER").value)
                )

            case "IDENT":
                return Identifier(
                    self.eat("IDENT").value
                )

            case _:
                raise SyntaxError(
                    f"Unexpected token {token.type}"
                )
