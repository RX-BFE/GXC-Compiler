# Testing Guide

## Overview

This document describes the testing infrastructure for the GXC compiler project.

## Test Structure

Test files are located in the `test/` directory with the `.gxc` extension:
- `test/hello.gxc` - Basic hello world test
- `test/operators.gxc` - Arithmetic operators test
- `test/comparison.gxc` - Comparison operators test
- `test/function.gxc` - Function declaration and call test
- `test/cmd.gxc` - Command line arguments test
- `test/if_elif_else.gxc` - Conditional statements test
- `test/invalid/missing_main.gxc` - Top-level statements without `func main()`
- `test/invalid/*.gxc` - Invalid syntax tests that must fail compilation

## Automated Test Runner

The project includes a Makefile-based automated test runner that:

1. **Cleans up old binaries** - Removes previously compiled executables
2. **Finds valid and invalid tests** - Scans `test/*.gxc` and `test/invalid/*.gxc`
3. **Compiles valid GXC to C** - Uses the compiler to convert `.gxc` files to `.c` files
4. **Compiles generated C with GCC** - Ensures the emitted C99 code is valid
5. **Runs valid binaries** - Executes each compiled binary
6. **Checks invalid syntax** - Verifies rejected programs do not compile
7. **Reports results** - Displays pass/fail status for every test
8. **Cleans up** - Removes compiled binaries and any invalid-test C artifacts

### Running All Tests

```bash
make test
```

### Example Output

```
========================================
GXC Compiler Test Runner
========================================

Cleaning up old binaries...
✓ Cleaned up old binaries

Found 6 valid test files:
  - cmd.gxc
  - comparison.gxc
  - function.gxc
  - hello.gxc
  - if_elif_else.gxc
  - operators.gxc

Found 6 invalid syntax tests:
  - invalid/missing_if_brace.gxc
  - invalid/missing_func_brace.gxc
  - invalid/missing_else_brace.gxc
  - invalid/unterminated_block.gxc
  - invalid/stray_closing_brace.gxc
  - invalid/missing_main.gxc

----------------------------------------
Testing: cmd
----------------------------------------
  → Compiling cmd.gxc to cmd.c...
  ✓ Compilation to C successful
  → Compiling cmd.c to executable...
  ✓ C compilation successful
  → Running cmd...
  ✓ Execution successful

...

========================================
Test Summary
========================================
Total tests: 12
Passed:      12
Failed:      0

All tests passed! ✓
```

### Useful Targets

```bash
make test
make test-valid
make test-invalid
make clean
make list-tests
```

## Manual Testing

For manual testing of individual files:

### Compile a Single Test File

```bash
cd Compiler
python main.py ../test/filename.gxc
```

This generates `../test/filename.c`

### Compile C Code to Executable

```bash
cd ../test
gcc filename.c -o filename
```

### Run the Executable

```bash
./filename
```

### Complete Manual Test Workflow

```bash
cd Compiler
python main.py ../test/hello.gxc
cd ../test
gcc hello.c -o hello
./hello
```

## Adding New Tests

To add a new test:

1. Create a new `.gxc` file in the `test/` directory
2. The test file should be a valid GXC program
3. The program must define `func main() { ... }` as the entry point
4. Run the automated test runner to verify:
   ```bash
   make test
   ```
5. The new test will be automatically picked up and executed

To add a new invalid syntax case:

1. Create a new `.gxc` file in `test/invalid/`
2. The file should contain code that must be rejected by the parser
3. Run the automated test runner to verify the compiler returns an error

## Test Coverage

Current test coverage includes:

- **Basic I/O**: `print` statements
- **Variables**: `let` declarations and assignments
- **Arithmetic Operators**: `+`, `-`, `*`, `/`, `%`
- **Comparison Operators**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Functions**: Function declarations and calls
- **Command Line Arguments**: `argc`, `argv` handling
- **Conditional Statements**: `if`, `elif`, `else`
- **Program Entry**: `func main() { ... }` required; no top-level statements
- **Invalid Syntax**: Missing braces, unterminated blocks, stray tokens

## Troubleshooting

### Test Compilation Fails

If a test fails during GXC to C compilation:
- Check syntax in the `.gxc` file
- Verify all tokens are recognized by the lexer
- Ensure AST nodes are properly defined

### C Compilation Fails

If a test fails during C compilation:
- Check the generated `.c` file for syntax errors
- Verify code generation is producing valid C99 code
- Ensure all variables are properly declared

### Execution Fails

If a test compiles but fails during execution:
- Check for runtime errors in the generated C code
- Verify logic in the original `.gxc` file
- Check for undefined behavior in C code

## Continuous Integration

### GitHub Actions

The project uses GitHub Actions for automated testing. The CI/CD pipeline is defined in `.github/workflows/test.yml` and:

- Runs on every push to `master` and `if-else` branches
- Runs on every pull request to `master` and `if-else` branches
- Sets up Python 3.x and GCC in an Ubuntu environment
- Executes the automated test runner script
- Uploads generated C files as artifacts for debugging

### Manual CI Testing

The test runner script is designed to be easily integrated into CI/CD pipelines:

```bash
# In CI pipeline
make test
# Exit code 0 = all tests passed
# Exit code 1 = some tests failed
```

The script uses `set -e` to exit immediately on any error, making it suitable for automated testing environments.
