#!/bin/bash

# Test runner script for GXC compiler
# Compiles and runs all .gxc test files

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPILER_DIR="$(dirname "$SCRIPT_DIR")/Compiler"
TEST_DIR="$SCRIPT_DIR"

echo "========================================"
echo "GXC Compiler Test Runner"
echo "========================================"
echo ""

# Clean up old binaries
echo "Cleaning up old binaries..."
cd "$TEST_DIR"
rm -f cmd function hello hello_test operators operators_test if_elif_else
echo "✓ Cleaned up old binaries"
echo ""

# Find all .gxc files
GXC_FILES=("$TEST_DIR"/*.gxc)

if [ ${#GXC_FILES[@]} -eq 0 ]; then
    echo "No .gxc files found in $TEST_DIR"
    exit 1
fi

echo "Found ${#GXC_FILES[@]} test files:"
for file in "${GXC_FILES[@]}"; do
    echo "  - $(basename "$file")"
done
echo ""

# Track results
PASSED=0
FAILED=0
FAILED_TESTS=()

# Run tests
for gxc_file in "${GXC_FILES[@]}"; do
    BASENAME=$(basename "$gxc_file" .gxc)
    C_FILE="$TEST_DIR/$BASENAME.c"
    BINARY="$TEST_DIR/$BASENAME"
    
    echo "----------------------------------------"
    echo "Testing: $BASENAME"
    echo "----------------------------------------"
    
    # Compile .gxc to .c
    echo "  → Compiling $BASENAME.gxc to $BASENAME.c..."
    if python3 "$COMPILER_DIR/main.py" "$gxc_file" > /dev/null 2>&1; then
        echo "  ✓ Compilation to C successful"
    else
        echo "  ✗ Compilation to C failed"
        FAILED=$((FAILED + 1))
        FAILED_TESTS+=("$BASENAME (gxc→c)")
        continue
    fi
    
    # Compile .c to binary
    echo "  → Compiling $BASENAME.c to executable..."
    if gcc "$C_FILE" -o "$BINARY" 2>/dev/null; then
        echo "  ✓ C compilation successful"
    else
        echo "  ✗ C compilation failed"
        FAILED=$((FAILED + 1))
        FAILED_TESTS+=("$BASENAME (c→binary)")
        continue
    fi
    
    # Run the binary
    echo "  → Running $BASENAME..."
    if "$BINARY" > /dev/null 2>&1; then
        echo "  ✓ Execution successful"
        PASSED=$((PASSED + 1))
    else
        echo "  ✗ Execution failed"
        FAILED=$((FAILED + 1))
        FAILED_TESTS+=("$BASENAME (execution)")
    fi
    
    echo ""
done

# Clean up binaries
echo "Cleaning up test binaries..."
cd "$TEST_DIR"
rm -f cmd function hello hello_test operators operators_test if_elif_else
echo "✓ Cleaned up"
echo ""

# Summary
echo "========================================"
echo "Test Summary"
echo "========================================"
echo "Total tests: $((PASSED + FAILED))"
echo "Passed:      $PASSED"
echo "Failed:      $FAILED"
echo ""

if [ $FAILED -gt 0 ]; then
    echo "Failed tests:"
    for test in "${FAILED_TESTS[@]}"; do
        echo "  ✗ $test"
    done
    echo ""
    exit 1
else
    echo "All tests passed! ✓"
    echo ""
    exit 0
fi
