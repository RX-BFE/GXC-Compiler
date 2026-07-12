from nodes import *

class C99Codegen:

    def __init__(self):
        self.lines = []
        self.variables = set()

    def emit(self, text):
        self.lines.append(text)

    def generate(self, program: Program):

        self.emit("#include <stdio.h>")
        self.emit("")
        self.emit("int main(void)")
        self.emit("{")

        for stmt in program.body:
            self.statement(stmt)

        self.emit("    return 0;")
        self.emit("}")

        return "\n".join(self.lines)

    # -------------------------

    def statement(self, node):

        match node:

            case Let(name=name, value=value):
                expr = self.expression(value)

                self.variables.add(name)

                self.emit(f"    int {name} = {expr};")

            case Assign(name=name, value=value):
                expr = self.expression(value)

                if name not in self.variables:
                    self.variables.add(name)
                    self.emit(f"    int {name} = {expr};")
                else:
                    self.emit(f"    {name} = {expr};")

            case Print(value=value):
                expr = self.expression(value)

                self.emit(f'    printf("%d\\n", {expr});')

            case _:
                raise RuntimeError(f"Unknown statement: {node}")

    # -------------------------

    def expression(self, node):

        match node:

            case Number(value=v):
                return str(v)

            case Identifier(name=n):
                return n

            case BinaryOp(left=l, op=op, right=r):
                left = self.expression(l)
                right = self.expression(r)

                return f"{left} {op} {right}"

            case _:
                raise RuntimeError(f"Unknown expression: {node}")
