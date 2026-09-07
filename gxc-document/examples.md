# GXC Code Examples

This document provides working code examples for various GXC language features. All examples are located in the `gxc-document/examples/` directory and can be compiled and run using the instructions in [Getting Started](getting-started.md).

## Basic Programs

### Hello World

File: `hello.gxc`

```gxc
func main() {
    let a = 10
    let b = 20
    let result = a + b
    print(result)
}
```

### Simple Output

File: `simple_output.gxc`

```gxc
func main() {
    let x = 42
    print(x)
}
```

### String Literals in Print

File: `string_print.gxc`

```gxc
func main() {
    print("Hello, World!")
}
```

## Variables and Types

### Integer Variables

```gxc
func main() {
    let x = 10
    let y = 20
    let z = x + y
    print(z)
}
```

### Variable Reassignment

File: `variable_reassignment.gxc`

```gxc
func main() {
    let x = 10
    x = 20
    print(x)
}
```

## Arithmetic Operations

### Basic Arithmetic

File: `operators.gxc`

```gxc
func main() {
    let a = 10 + 5
    let b = 10 - 5
    let c = 10 * 5
    let d = 10 / 5
    let e = 10 % 3

    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
}
```

### Operator Precedence

File: `operator_precedence.gxc`

```gxc
func main() {
    let f = 10 + 5 * 2
    let g = (10 + 5) * 2

    print(f)
    print(g)
}
```

## Comparison Operations

### Basic Comparisons

File: `comparison.gxc`

```gxc
func main() {
    let x = 10
    let y = 5

    let a = x > y
    let b = x == 10
    let c = x != y
    let d = x >= y
    let e = x <= 20
    let f = x < 100

    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)
}
```

### Complex Comparisons

File: `complex_comparison.gxc`

```gxc
func main() {
    let x = 10
    let y = 5

    let g = (x + y) > 10
    let h = x * 2 == 20
    print(g)
    print(h)
}
```

## Functions

### Function Declaration and Call

File: `function.gxc`

```gxc
func add(a, b) {
    return a + b
}

func main() {
    let result = add(10, 20)
    print(result)
}
```

### Multiple Functions

File: `multiple_functions.gxc`

```gxc
func multiply(x, y) {
    return x * y
}

func divide(x, y) {
    return x / y
}

func main() {
    let a = multiply(6, 7)
    let b = divide(20, 4)
    print(a)
    print(b)
}
```

### Function with No Parameters

File: `function_no_params.gxc`

```gxc
func get_value() {
    return 42
}

func main() {
    let x = get_value()
    print(x)
}
```

## Control Flow

### If Statement

File: `if_statement.gxc`

```gxc
func main() {
    let x = 15

    if x > 10 {
        print(1)
    }
}
```

### If-Else Statement

File: `if_else.gxc`

```gxc
func main() {
    let x = 5

    if x > 10 {
        print(1)
    } else {
        print(2)
    }
}
```

### If-Elif-Else Statement

File: `if_elif_else.gxc`

```gxc
func main() {
    let x = 15

    if x > 10 {
        print(1)
    } elif x > 5 {
        print(2)
    } else {
        print(3)
    }
}
```

### Nested Conditionals

File: `nested_conditionals.gxc`

```gxc
func main() {
    let x = 15
    let y = 20

    if x > 10 {
        if y > 15 {
            print(1)
        } else {
            print(2)
        }
    } else {
        print(3)
    }
}
```

## Loops

### Basic For Loop

File: `for_loop.gxc`

```gxc
func main() {
    let sum = 0

    for let i = 0; i < 5; i = i + 1 {
        sum = sum + i
    }

    print(sum)
}
```

### For Loop with Existing Variable

File: `for_existing_var.gxc`

```gxc
func main() {
    let i = 0
    let sum = 0

    for i = 0; i < 5; i = i + 1 {
        sum = sum + i
    }

    print(sum)
}
```

### For Loop with Complex Condition

File: `for_complex.gxc`

```gxc
func main() {
    let count = 0

    for let i = 1; i <= 10; i = i + 1 {
        if i % 2 == 0 {
            count = count + 1
        }
    }

    print(count)
}
```

## Command Line Arguments

### Get Argument Count

File: `cmd_args.gxc`

```gxc
func main() {
    let arg_count = get_args()
    print(arg_count)
}
```

### Access Command Line Arguments

File: `cmd_args_access.gxc`

```gxc
func main() {
    let arg_count = get_args()
    
    if arg_count > 0 {
        let first_arg = args[0]
        print(first_arg)
    }
}
```

### Process All Arguments

File: `process_all_args.gxc`

```gxc
func main() {
    let arg_count = get_args()
    let i = 0

    for i = 0; i < arg_count; i = i + 1 {
        let arg = args[i]
        print(arg)
    }
}
```

## Combined Examples

### Calculator Function

File: `calculator.gxc`

```gxc
func calculate(op, a, b) {
    if op == 1 {
        return a + b
    } elif op == 2 {
        return a - b
    } elif op == 3 {
        return a * b
    } else {
        return a / b
    }
}

func main() {
    let result1 = calculate(1, 10, 5)
    let result2 = calculate(3, 4, 3)
    print(result1)
    print(result2)
}
```

### Sum of Array Elements

File: `sum_array.gxc`

```gxc
func main() {
    let sum = 0
    let i = 0

    for i = 0; i < 5; i = i + 1 {
        sum = sum + i
    }

    print(sum)
}
```

### Factorial Function

File: `factorial.gxc`

```gxc
func main() {
    let n = 5
    let result = 1
    let i = 1

    for i = 1; i <= n; i = i + 1 {
        result = result * i
    }

    print(result)
}
```

## Error Handling Examples

### Missing Main Function (Invalid)

```gxc
func add(a, b) {
    return a + b
}

let result = add(10, 20)
print(result)
```

This will fail because there is no `func main()` entry point.

### Top-Level Statement (Invalid)

```gxc
let x = 10

func main() {
    print(x)
}
```

This will fail because top-level statements are not allowed.

### Missing Braces (Invalid)

```gxc
func main() {
    let x = 10
    if x > 5
        print(x)
}
```

This will fail because blocks require curly braces.