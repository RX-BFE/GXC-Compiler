from typing import Set, List
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
)


class C99Codegen:
    """C99 code generator for AST nodes."""

    # Constants for C code generation
    INDENT = "    "
    INCLUDE_STDIO = "#include <stdio.h>"
    INCLUDE_STDLIB = "#include <stdlib.h>"
    MAIN_SIGNATURE = "int main(int argc, char** argv)"
    RETURN_STATEMENT = "return 0;"
    PRINTF_FORMAT = "%d\\n"
    PRINTF_STRING_FORMAT = "%s\\n"

    def __init__(self) -> None:
        self.lines: List[str] = []
        self.variables: Set[str] = set()

    def emit(self, text: str) -> None:
        """Add a line to the generated code."""
        self.lines.append(text)

    def generate(self, program: Program) -> str:
        """Generate C99 code from the AST program."""
        self.emit(self.INCLUDE_STDIO)
        self.emit(self.INCLUDE_STDLIB)
        self.emit("")

        # Generate function declarations first
        for stmt in program.body:
            if isinstance(stmt, FunctionDecl):
                self._generate_function_decl(stmt)

        self.emit("")
        self.emit(self.MAIN_SIGNATURE)
        self.emit("{")

        # Generate non-function statements in main
        for stmt in program.body:
            if not isinstance(stmt, FunctionDecl):
                self.statement(stmt)

        self.emit(f"{self.INDENT}{self.RETURN_STATEMENT}")
        self.emit("}")

        return "\n".join(self.lines)

    # -------------------------

    def _generate_function_decl(self, node: FunctionDecl) -> None:
        """Generate C function declaration."""
        # Generate function signature
        params_str = ", ".join(f"int {param}" for param in node.params)
        self.emit(f"int {node.name}({params_str})")
        self.emit("{")

        # Generate function body
        for stmt in node.body:
            self.statement(stmt)

        self.emit("}")

    # -------------------------

    def statement(self, node: Statement) -> None:
        """Generate C code for a statement node."""
        match node:
            case Let(name=name, value=value):
                self._emit_variable_declaration(name, value, is_first_declaration=True)

            case Assign(name=name, value=value):
                is_first = name not in self.variables
                self._emit_variable_declaration(
                    name, value, is_first_declaration=is_first
                )

            case Print(value=value):
                # Check if the value is a string literal to use proper format
                if isinstance(value, String):
                    expr = self.expression(value)
                    self.emit(
                        f'{self.INDENT}printf("{self.PRINTF_STRING_FORMAT}", {expr});'
                    )
                else:
                    expr = self.expression(value)
                    self.emit(f'{self.INDENT}printf("{self.PRINTF_FORMAT}", {expr});')

            case Return(value=value):
                expr = self.expression(value)
                self.emit(f"{self.INDENT}return {expr};")

            case _:
                raise RuntimeError(f"Unknown statement type: {type(node).__name__}")

    def _emit_variable_declaration(
        self, name: str, value: Expression, is_first_declaration: bool
    ) -> None:
        """Emit variable declaration or assignment based on whether it's first use."""
        expr = self.expression(value)

        if is_first_declaration:
            self.variables.add(name)
            self.emit(f"{self.INDENT}int {name} = {expr};")
        else:
            self.emit(f"{self.INDENT}{name} = {expr};")

    # -------------------------

    def expression(self, node: Expression) -> str:
        """Generate C code for an expression node."""
        match node:
            case Number(value=v):
                return str(v)

            case String(value=v):
                # Generate C string literal with escaped quotes
                return f'"{v}"'

            case Identifier(name=n):
                return self._handle_identifier(n)

            case BinaryOp(left=l, op=op, right=r):
                left = self.expression(l)
                right = self.expression(r)
                return f"{left} {op} {right}"

            case Parenthesized(expr=e):
                expr_str = self.expression(e)
                return f"({expr_str})"

            case FunctionCall(name=name, args=args):
                return self._handle_function_call(name, args)

            case Index(target=target, index=index):
                return self._handle_index(target, index)

            case _:
                raise RuntimeError(f"Unknown expression type: {type(node).__name__}")

    def _handle_identifier(self, name: str) -> str:
        """Handle identifier with special cases."""
        if name == "args":
            # args is a special identifier that maps to argv
            return "argv"
        return name

    def _handle_function_call(self, name: str, args: List[Expression]) -> str:
        """Handle function call with special cases."""
        if name == "get_args":
            # get_args() generates code to return argc-1 (skip program name)
            return "argc - 1"

        # For other function calls, generate function call syntax
        args_str = ", ".join(self.expression(arg) for arg in args)
        return f"{name}({args_str})"

    def _handle_index(self, target: Expression, index: Expression) -> str:
        """Handle array indexing with special cases."""
        if isinstance(target, Identifier) and target.name == "args":
            # args[index] generates argv[index+1] (skip program name)
            index_expr = self.expression(index)
            return f"argv[{index_expr} + 1]"

        # Generate array indexing: target[index]
        target_expr = self.expression(target)
        index_expr = self.expression(index)
        return f"{target_expr}[{index_expr}]"
