from typing import Set, List, Optional
from errors import CodegenError
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
    For,
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
        self.variables_stack: List[Set[str]] = []

    def emit(self, text: str) -> None:
        """Add a line to the generated code."""
        self.lines.append(text)

    def generate(self, program: Program) -> str:
        """Generate C99 code from the AST program."""
        main_decl = None
        helper_functions: List[FunctionDecl] = []

        self.emit(self.INCLUDE_STDIO)
        self.emit(self.INCLUDE_STDLIB)
        self.emit("")

        for stmt in program.body:
            if isinstance(stmt, FunctionDecl):
                if stmt.name == "main":
                    if main_decl is not None:
                        raise CodegenError("Multiple main functions are not allowed")
                    main_decl = stmt
                else:
                    helper_functions.append(stmt)
            else:
                raise CodegenError(
                    "Top-level statements are not allowed; expected only function declarations"
                )

        if main_decl is None:
            raise CodegenError("Program must define func main() { ... }")

        for index, func in enumerate(helper_functions):
            if index > 0:
                self.emit("")
            self._generate_function_decl(func)

        if helper_functions:
            self.emit("")
        self._generate_main_decl(main_decl)

        return "\n".join(self.lines)

    # -------------------------

    def _generate_function_decl(self, node: FunctionDecl) -> None:
        """Generate C function declaration."""
        self._push_scope()
        try:
            # Generate function signature
            params_str = ", ".join(f"int {param}" for param in node.params)
            self.emit(f"int {node.name}({params_str})")
            self.emit("{")

            # Generate function body
            for stmt in node.body:
                self.statement(stmt)

            self.emit("}")
        finally:
            self._pop_scope()

    def _generate_main_decl(self, node: FunctionDecl) -> None:
        """Generate the explicit program entry point."""
        self._push_scope()
        try:
            self.emit(self.MAIN_SIGNATURE)
            self.emit("{")

            for stmt in node.body:
                self.statement(stmt)

            self.emit(f"{self.INDENT}{self.RETURN_STATEMENT}")
            self.emit("}")
        finally:
            self._pop_scope()

    def _push_scope(self) -> None:
        """Start a new variable scope."""
        self.variables_stack.append(set())

    def _pop_scope(self) -> None:
        """End the current variable scope."""
        if not self.variables_stack:
            raise CodegenError("Variable scope underflow")
        self.variables_stack.pop()

    def _current_variables(self) -> Set[str]:
        """Get the current variable scope."""
        if not self.variables_stack:
            raise CodegenError("No active variable scope")
        return self.variables_stack[-1]

    def _is_variable_defined(self, name: str) -> bool:
        """Check whether a variable is visible in any active scope."""
        return any(name in scope for scope in reversed(self.variables_stack))

    def statement(self, node: Statement) -> None:
        """Generate C code for a statement node."""
        match node:
            case Let(name=name, value=value):
                self._emit_variable_declaration(name, value, is_first_declaration=True)

            case Assign(name=name, value=value):
                is_first = not self._is_variable_defined(name)
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

            case If(condition=condition, body=body, elifs=elifs, else_body=else_body):
                self._generate_if_statement(condition, body, elifs, else_body)

            case For(init=init, condition=condition, post=post, body=body):
                self._generate_for_statement(init, condition, post, body)

            case _:
                raise CodegenError(f"Unknown statement type: {type(node).__name__}")

    def _emit_variable_declaration(
        self, name: str, value: Expression, is_first_declaration: bool
    ) -> None:
        """Emit variable declaration or assignment based on whether it's first use."""
        expr = self.expression(value)
        variables = self._current_variables()

        if is_first_declaration:
            variables.add(name)
            self.emit(f"{self.INDENT}int {name} = {expr};")
        else:
            self.emit(f"{self.INDENT}{name} = {expr};")

    # -------------------------

    def _generate_if_statement(
        self,
        condition: Expression,
        body: List[Statement],
        elifs: List[Elif],
        else_body: Optional[List[Statement]],
    ) -> None:
        """Generate C if-elif-else statement."""
        cond_expr = self.expression(condition)
        self.emit(f"{self.INDENT}if ({cond_expr}) {{")

        # Generate if body
        for stmt in body:
            self.statement(stmt)

        self.emit(f"{self.INDENT}}}")

        # Generate elif clauses
        for elif_clause in elifs:
            elif_cond = self.expression(elif_clause.condition)
            self.emit(f"{self.INDENT}else if ({elif_cond}) {{")

            for stmt in elif_clause.body:
                self.statement(stmt)

            self.emit(f"{self.INDENT}}}")

        # Generate else clause
        if else_body:
            self.emit(f"{self.INDENT}else {{")

            for stmt in else_body:
                self.statement(stmt)

            self.emit(f"{self.INDENT}}}")

    def _generate_for_statement(
        self,
        init: Statement,
        condition: Expression,
        post: Statement,
        body: List[Statement],
    ) -> None:
        """Generate C for-loop statement."""
        self._push_scope()
        try:
            init_expr = self._render_for_clause(init, is_post=False)
            cond_expr = self.expression(condition)
            post_expr = self._render_for_clause(post, is_post=True)

            self.emit(f"{self.INDENT}for ({init_expr}; {cond_expr}; {post_expr}) {{")

            for stmt in body:
                self.statement(stmt)

            self.emit(f"{self.INDENT}}}")
        finally:
            self._pop_scope()

    def _render_for_clause(self, node: Statement, is_post: bool) -> str:
        """Render a for-loop header clause without trailing semicolon."""
        match node:
            case Let(name=name, value=value):
                if is_post:
                    raise CodegenError("for-loop post clause cannot be a declaration")

                expr = self.expression(value)
                if self._is_variable_defined(name):
                    return f"{name} = {expr}"

                self._current_variables().add(name)
                return f"int {name} = {expr}"

            case Assign(name=name, value=value):
                expr = self.expression(value)
                if self._is_variable_defined(name):
                    return f"{name} = {expr}"

                if is_post:
                    raise CodegenError(
                        f"for-loop post variable '{name}' must be declared before the loop"
                    )

                self._current_variables().add(name)
                return f"int {name} = {expr}"

            case _:
                raise CodegenError(
                    f"Unsupported for-loop clause: {type(node).__name__}"
                )

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
                raise CodegenError(f"Unknown expression type: {type(node).__name__}")

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
