# GXC Language Reference

## Program Structure

### Entry Point

Every GXC program must define a `main` function with no parameters:

```gxc
func main() {
    // program code
}
```

### Top-Level Rules

- All code must be inside functions
- No top-level statements are allowed
- Multiple functions can be defined, but `main()` is required
- `main()` must not take parameters

## Data Types

### Integers

Integer literals are written as decimal numbers:

```gxc
let x = 42
let y = -10
let z = 0
```

**Note:** String literals are supported in `print()` statements but cannot be assigned to variables.

## Variables

### Declaration

Variables are declared using the `let` keyword:

```gxc
let name = value
```

### Assignment

Variables can be reassigned using the assignment operator:

```gxc
name = new_value
```

### Variable Names

Variable names must:
- Start with a letter or underscore
- Contain only letters, digits, and underscores
- Not be a reserved keyword

Valid: `x`, `_count`, `value1`, `myVar`
Invalid: `1var`, `let`, `func`

## Operators

### Arithmetic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+`      | Addition    | `a + b` |
| `-`      | Subtraction | `a - b` |
| `*`      | Multiplication | `a * b` |
| `/`      | Division    | `a / b` |
| `%`      | Modulo      | `a % b` |

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `==`     | Equal to    | `a == b` |
| `!=`     | Not equal to | `a != b` |
| `<`      | Less than   | `a < b` |
| `>`      | Greater than | `a > b` |
| `<=`     | Less than or equal | `a <= b` |
| `>=`     | Greater than or equal | `a >= b` |

### Assignment Operator

| Operator | Description | Example |
|----------|-------------|---------|
| `=`      | Assignment  | `x = 5` |

## Operator Precedence

Operators are evaluated in the following order (highest to lowest):

1. Parentheses `()`
2. Function calls `()`
3. Array indexing `[]`
4. Multiplication `*`, Division `/`, Modulo `%`
5. Addition `+`, Subtraction `-`
6. Comparison operators `==`, `!=`, `<`, `>`, `<=`, `>=`

## Keywords

| Keyword | Description |
|---------|-------------|
| `func`  | Function declaration |
| `let`   | Variable declaration |
| `return`| Return from function |
| `if`    | Conditional statement |
| `elif`  | Else-if conditional |
| `else`  | Else conditional |
| `for`   | Loop statement |
| `print` | Output function |

## Functions

### Function Declaration

```gxc
func function_name(param1, param2) {
    // function body
}
```

### Function Call

```gxc
function_name(arg1, arg2)
```

### Return Statement

```gxc
return expression
```

## Control Flow

### If Statement

```gxc
if condition {
    // code
}
```

### If-Elif-Else Statement

```gxc
if condition1 {
    // code
} elif condition2 {
    // code
} else {
    // code
}
```

### For Loop

```gxc
for init; condition; post {
    // code
}
```

- `init`: Variable declaration or assignment (e.g., `let i = 0` or `i = 0`)
- `condition`: Expression evaluated before each iteration
- `post`: Assignment executed after each iteration (e.g., `i = i + 1`)

**Note**: The `post` clause cannot be a variable declaration.

## Expressions

### Literals

```gxc
42           // integer
"hello"      // string
```

### Identifiers

```gxc
variable_name
```

### Binary Operations

```gxc
a + b
a * (c - d)
x == y
```

### Parenthesized Expressions

```gxc
(a + b) * c
```

### Function Calls

```gxc
my_function(arg1, arg2)
```

### Array Indexing

```gxc
array[index]
```

## Statements

### Let Statement

Declares a new variable:

```gxc
let x = 10
```

### Assign Statement

Assigns a value to an existing variable:

```gxc
x = 20
```

### Print Statement

Outputs a value:

```gxc
print(x)
print(42)
print("Hello")
```

### Return Statement

Returns a value from a function:

```gxc
return x + y
```

### Function Declaration

Declares a function:

```gxc
func add(a, b) {
    return a + b
}
```

## Syntax Rules

### Block Delimiters

Blocks are delimited by curly braces `{}`:

```gxc
func main() {
    let x = 10
    if x > 5 {
        print(x)
    }
}
```

### Statement Termination

Statements are terminated by newlines, not semicolons (except in for loop headers).

### Whitespace

Spaces and tabs are ignored except in string literals and for separating tokens.

### Comments

GXC does not support comments.

## Error Conditions

### Parse Errors

- Missing `func main()` entry point
- Top-level statements outside functions
- Missing braces in blocks
- Missing semicolons in for loop headers
- Invalid token sequences
- Unterminated blocks

### Lex Errors

- Unknown characters in source code
- Invalid string literals

### Code Generation Errors

- Multiple `main` functions
- Variable scope errors
- Invalid for loop clauses

## Example Program Structure

```gxc
func helper_function(x) {
    return x * 2
}

func main() {
    let value = 10
    let result = helper_function(value)
    print(result)
}
```