# GXC Standard Library

## Built-in Functions

### print()

Outputs a value to standard output.

**Syntax:**
```gxc
print(expression)
```

**Parameters:**
- `expression`: An integer or string value to print

**Return Value:** None

**Examples:**
```gxc
func main() {
    let x = 42
    print(x)
    print("Hello, World!")
}
```

**Behavior:**
- For integers: prints the integer value followed by a newline
- For string literals: prints the string content followed by a newline
- String literals can only be used directly in `print()` statements, not assigned to variables
- The function automatically adds a newline after each output

### get_args()

Returns the number of command-line arguments passed to the program (excluding the program name).

**Syntax:**
```gxc
get_args()
```

**Parameters:** None

**Return Value:** Integer representing the count of command-line arguments

**Examples:**
```gxc
func main() {
    let arg_count = get_args()
    print(arg_count)
}
```

**Behavior:**
- Returns `argc - 1` where `argc` is the total argument count from C
- The program name is not included in the count
- If no arguments are provided, returns 0

## Special Identifiers

### args[]

Array identifier for accessing command-line arguments.

**Syntax:**
```gxc
args[index]
```

**Parameters:**
- `index`: Integer expression representing the argument index (0-based)

**Return Value:** String value of the command-line argument

**Examples:**
```gxc
func main() {
    let arg_count = get_args()
    
    if arg_count > 0 {
        let first_arg = args[0]
        print(first_arg)
    }
}
```

**Behavior:**
- Accesses command-line arguments using 0-based indexing
- `args[0]` is the first command-line argument (not the program name)
- Internally maps to `argv[index + 1]` in the generated C code
- Out-of-bounds access is not checked and may cause undefined behavior

## Complete Example

```gxc
func main() {
    let arg_count = get_args()
    print(arg_count)
    
    let i = 0
    for i = 0; i < arg_count; i = i + 1 {
        let arg = args[i]
        print(arg)
    }
}
```

## Generated C Code

The GXC compiler generates C99 code with the following standard includes:

```c
#include <stdio.h>
#include <stdlib.h>
```

### Main Function Signature

The generated C code uses the following main function signature:

```c
int main(int argc, char** argv)
```

### Special Identifier Mapping

| GXC Identifier | C Equivalent | Description |
|----------------|--------------|-------------|
| `args` | `argv` | Command-line argument array |
| `args[index]` | `argv[index + 1]` | Access specific argument (skips program name) |
| `get_args()` | `argc - 1` | Get argument count (excludes program name) |

## Limitations

- No standard library beyond `print()` and `get_args()`
- No file I/O functions
- No string manipulation functions
- No mathematical functions beyond basic operators
- No memory management functions
- Array indexing is only supported for the `args[]` identifier

## Future Extensions

The standard library may be extended to include:
- Additional I/O functions
- String manipulation
- Mathematical functions
- File operations
- Memory management