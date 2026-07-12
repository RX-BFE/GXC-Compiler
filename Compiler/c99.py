from typing import Set, List
from nodes import *

class C99Codegen:
    """C99 code generator for AST nodes."""
    
    # Constants for C code generation
    INDENT = "    "
    INCLUDE_STDIO = "#include <stdio.h>"
    MAIN_SIGNATURE = "int main(void)"
    RETURN_STATEMENT = "return 0;"
    PRINTF_FORMAT = "%d\\n"
    
    def __init__(self) -> None:
        self.lines: List[str] = []
        self.variables: Set[str] = set()

    def emit(self, text: str) -> None:
        """Add a line to the generated code."""
        self.lines.append(text)

    def generate(self, program: Program) -> str:
        """Generate C99 code from the AST program."""
        self.emit(self.INCLUDE_STDIO)
        self.emit("")
        self.emit(self.MAIN_SIGNATURE)
        self.emit("{")

        for stmt in program.body:
            self.statement(stmt)

        self.emit(f"{self.INDENT}{self.RETURN_STATEMENT}")
        self.emit("}")

        return "\n".join(self.lines)

    # -------------------------

    def statement(self, node) -> None:
        """Generate C code for a statement node."""
        match node:
            case Let(name=name, value=value):
                self._emit_variable_declaration(name, value, is_first_declaration=True)

            case Assign(name=name, value=value):
                is_first = name not in self.variables
                self._emit_variable_declaration(name, value, is_first_declaration=is_first)

            case Print(value=value):
                expr = self.expression(value)
                self.emit(f'{self.INDENT}printf("{self.PRINTF_FORMAT}", {expr});')

            case _:
                raise RuntimeError(f"Unknown statement type: {type(node).__name__}")

    def _emit_variable_declaration(self, name: str, value, is_first_declaration: bool) -> None:
        """Emit variable declaration or assignment based on whether it's first use."""
        expr = self.expression(value)
        
        if is_first_declaration:
            self.variables.add(name)
            self.emit(f"{self.INDENT}int {name} = {expr};")
        else:
            self.emit(f"{self.INDENT}{name} = {expr};")

    # -------------------------

    def expression(self, node) -> str:
        """Generate C code for an expression node."""
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
                raise RuntimeError(f"Unknown expression type: {type(node).__name__}")
