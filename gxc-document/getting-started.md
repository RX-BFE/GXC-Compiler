# Getting Started with GXC

## Prerequisites

- Python 3.12 or higher
- uv (Python package manager)
- GCC (C compiler)

## Installation

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install GXC Compiler

```bash
cd GXC-Compiler
uv sync
uv sync --group dev
```

## Basic Usage

### Compile a GXC File

```bash
uv run gxc path/to/file.gxc
```

This generates a `.c` file with the same name as the input file.

### Compile the Generated C Code

```bash
gcc path/to/file.c -o path/to/file
```

### Run the Executable

```bash
./path/to/file
```

## Complete Workflow Example

Create a file `hello.gxc`:

```gxc
func main() {
    let a = 10
    let b = 20
    let result = a + b
    print(result)
}
```

Compile and run:

```bash
uv run gxc hello.gxc
gcc hello.c -o hello
./hello
```

Output: `30`

## Error Messages

The GXC compiler provides detailed error messages with source location:

```
Error: Expected IDENT, got NUMBER
 --> hello.gxc:3:10
  3 |     let 10 = x
           ^
```

## Testing Your Installation

Run the test suite to verify your installation:

```bash
make test
```

This compiles and runs all test files in the `test/` directory.

## Common Issues

### File Not Found

Ensure the `.gxc` file exists and the path is correct:

```bash
uv run gxc nonexist.gxc
# Error: File not found: nonexist.gxc
```

### Wrong File Extension

The compiler only accepts `.gxc` files:

```bash
uv run gxc program.txt
# Error: Input file must have .gxc extension
```

### Compilation Errors

Check the error message for line and column information. Common errors include:
- Missing `func main()` entry point
- Syntax errors in expressions
- Missing braces or semicolons
- Invalid variable names

## Next Steps

- [Language Reference](language-reference.md) - Complete syntax documentation
- [Examples](examples.md) - Sample programs by category
- [Standard Library](stdlib.md) - Built-in functions