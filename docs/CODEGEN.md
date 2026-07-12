# C99 Code Generator

## Overview
The C99 code generator (`c99.py`) converts the Abstract Syntax Tree (AST) into valid C99 source code. It handles variable tracking and generates a complete C program with a `main()` function.

## Class Structure

### C99Codegen
Main class responsible for code generation.

#### Attributes
- `lines: List[str]` - Generated code lines
- `variables: Set[str]` - Track declared variables to avoid redeclaration

#### Constants
- `INDENT` - Code indentation (4 spaces)
- `INCLUDE_STDIO` - Standard library include
- `MAIN_SIGNATURE` - Main function signature
- `RETURN_STATEMENT` - Return statement
- `PRINTF_FORMAT` - Printf format string

## Methods

### generate(program: Program) -> str
Entry point for code generation. Generates complete C program structure:
1. Include statements
2. Main function declaration
3. Statement compilation
4. Return statement

### statement(node) -> None
Dispatches to appropriate statement handler based on node type:
- `Let` - Variable declaration (always first declaration)
- `Assign` - Variable assignment or declaration if first use
- `Print` - Printf statement for output

### _emit_variable_declaration(name: str, value, is_first_declaration: bool) -> None
Helper method for variable handling:
- If first declaration: emits `int name = value;`
- If subsequent use: emits `name = value;`
- Tracks variables in the `variables` set

### expression(node) -> str
Recursively generates C code for expressions:
- `Number` - Returns numeric value as string
- `Identifier` - Returns variable name
- `BinaryOp` - Returns infix operation (left op right)

## Code Generation Strategy

### Variable Tracking
The generator maintains a set of declared variables to:
- Avoid redeclaring existing variables
- Emit proper `int` declarations for first use
- Emit simple assignments for subsequent uses

### Output Format
All generated statements are properly indented with 4 spaces. The output is a complete, compilable C program.