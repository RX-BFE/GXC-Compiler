# GXC Programming Language Documentation

GXC is a small programming language that compiles to C99. It provides a simple syntax for writing programs that are compiled to efficient C code.

## Overview

GXC features:
- **Function-based structure**: All code must be inside functions
- **Integer type**: Primary data type for numeric operations
- **String literals**: Supported in print statements
- **Control flow**: if-elif-else conditionals and for loops
- **Functions**: User-defined functions with parameters
- **Command-line access**: Built-in support for command-line arguments
- **C99 output**: Compiles to standard C99 code

## Quick Example

```gxc
func main() {
    let a = 10
    let b = 20
    let result = a + b
    print(result)
}
```

## Documentation

- [Getting Started](getting-started.md) - Installation and basic usage
- [Language Reference](language-reference.md) - Complete syntax and semantics
- [Examples](examples.md) - Code examples by category
- [Standard Library](stdlib.md) - Built-in functions and special identifiers

## Language Characteristics

- **Entry point**: Programs must define `func main() { ... }`
- **No top-level statements**: All code must be inside functions
- **Block syntax**: Uses curly braces `{}` for blocks
- **C compilation**: Output is C99 code that can be compiled with GCC

## Compilation Process

1. Write GXC source code (`.gxc` files)
2. Compile with GXC compiler to generate C code (`.c` files)
3. Compile C code with GCC to create executable
4. Run the executable

## Getting Help

For detailed information about specific language features, see the [Language Reference](language-reference.md).