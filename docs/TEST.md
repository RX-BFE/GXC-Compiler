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

## Automated Test Runner

The project includes an automated test runner script (`test/run_tests.sh`) that:

1. **Cleans up old binaries** - Removes previously compiled executables
2. **Finds all test files** - Scans for `.gxc` files in the test directory
3. **Compiles GXC to C** - Uses the compiler to convert `.gxc` files to `.c` files
4. **Compiles C to binary** - Uses GCC to compile `.c` files to executables
5. **Runs tests** - Executes each compiled binary
6. **Reports results** - Displays pass/fail status for each test
7. **Cleans up** - Removes binary files after testing

### Running All Tests

```bash
cd test
./run_tests.sh
```

### Example Output

```
========================================
GXC Compiler Test Runner
========================================

Cleaning up old binaries...
✓ Cleaned up old binaries

Found 6 test files:
  - cmd.gxc
  - comparison.gxc
  - function.gxc
  - hello.gxc
  - if_elif_else.gxc
  - operators.gxc

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
Total tests: 6
Passed:      6
Failed:      0

All tests passed! ✓
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
3. Run the automated test runner to verify:
   ```bash
   cd test
   ./run_tests.sh
   ```
4. The new test will be automatically picked up and executed

## Test Coverage

Current test coverage includes:

- **Basic I/O**: `print` statements
- **Variables**: `let` declarations and assignments
- **Arithmetic Operators**: `+`, `-`, `*`, `/`, `%`
- **Comparison Operators**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Functions**: Function declarations and calls
- **Command Line Arguments**: `argc`, `argv` handling
- **Conditional Statements**: `if`, `elif`, `else`

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

The test runner script is designed to be easily integrated into CI/CD pipelines:

```bash
# In CI pipeline
cd test
./run_tests.sh
# Exit code 0 = all tests passed
# Exit code 1 = some tests failed
```

The script uses `set -e` to exit immediately on any error, making it suitable for automated testing environments.
