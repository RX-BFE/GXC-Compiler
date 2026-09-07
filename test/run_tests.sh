#!/bin/bash

# Test runner script for GXC compiler
# Compiles and runs valid .gxc test files, then verifies invalid syntax tests fail

set -e  # Exit on error
shopt -s nullglob

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPILER_DIR="$(dirname "$SCRIPT_DIR")/Compiler"
TEST_DIR="$SCRIPT_DIR"
INVALID_TEST_DIR="$TEST_DIR/invalid"
VALID_GXC_FILES=("$TEST_DIR"/*.gxc)
INVALID_GXC_FILES=("$INVALID_TEST_DIR"/*.gxc)

echo "========================================"
echo "GXC Compiler Test Runner"
echo "========================================"
echo ""

# Clean up old binaries
cleanup_artifacts() {
    for gxc_file in "${VALID_GXC_FILES[@]}"; do
        base_name="$(basename "$gxc_file" .gxc)"
        rm -f "$TEST_DIR/$base_name"
    done

    for gxc_file in "${INVALID_GXC_FILES[@]}"; do
        base_name="$(basename "$gxc_file" .gxc)"
        rm -f "$INVALID_TEST_DIR/$base_name" "$INVALID_TEST_DIR/$base_name.c"
    done
}

trap cleanup_artifacts EXIT

echo "Cleaning up old binaries..."
cleanup_artifacts
echo "✓ Cleaned up old binaries"
echo ""

if [ ${#VALID_GXC_FILES[@]} -eq 0 ]; then
    echo "No valid .gxc files found in $TEST_DIR"
    exit 1
fi

echo "Found ${#VALID_GXC_FILES[@]} valid test files:"
for file in "${VALID_GXC_FILES[@]}"; do
    echo "  - $(basename "$file")"
done
echo ""

if [ ${#INVALID_GXC_FILES[@]} -gt 0 ]; then
    echo "Found ${#INVALID_GXC_FILES[@]} invalid syntax tests:"
    for file in "${INVALID_GXC_FILES[@]}"; do
        echo "  - invalid/$(basename "$file")"
    done
    echo ""
fi

# Track results
PASSED=0
FAILED=0
FAILED_TESTS=()

# Run valid tests
for gxc_file in "${VALID_GXC_FILES[@]}"; do
    BASENAME=$(basename "$gxc_file" .gxc)
    C_FILE="$TEST_DIR/$BASENAME.c"
    BINARY="$TEST_DIR/$BASENAME"
    LOG_FILE="$(mktemp)"
    
    echo "----------------------------------------"
    echo "Testing: $BASENAME"
    echo "----------------------------------------"
    
    # Compile .gxc to .c
    echo "  → Compiling $BASENAME.gxc to $BASENAME.c..."
    if python3 "$COMPILER_DIR/main.py" "$gxc_file" > "$LOG_FILE" 2>&1; then
        echo "  ✓ Compilation to C successful"
    else
        echo "  ✗ Compilation to C failed"
        cat "$LOG_FILE"
        FAILED=$((FAILED + 1))
        FAILED_TESTS+=("$BASENAME (gxc→c)")
        rm -f "$LOG_FILE"
        continue
    fi
    
    # Compile .c to binary
    echo "  → Compiling $BASENAME.c to executable..."
    if gcc "$C_FILE" -o "$BINARY" > "$LOG_FILE" 2>&1; then
        echo "  ✓ C compilation successful"
    else
        echo "  ✗ C compilation failed"
        cat "$LOG_FILE"
        FAILED=$((FAILED + 1))
        FAILED_TESTS+=("$BASENAME (c→binary)")
        rm -f "$LOG_FILE"
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
    
    rm -f "$LOG_FILE"
    echo ""
done

# Run invalid syntax tests
for gxc_file in "${INVALID_GXC_FILES[@]}"; do
    BASENAME=$(basename "$gxc_file" .gxc)
    C_FILE="$INVALID_TEST_DIR/$BASENAME.c"
    LOG_FILE="$(mktemp)"

    echo "----------------------------------------"
    echo "Testing invalid syntax: invalid/$BASENAME"
    echo "----------------------------------------"

    echo "  → Expecting compilation failure..."
    if python3 "$COMPILER_DIR/main.py" "$gxc_file" > "$LOG_FILE" 2>&1; then
        echo "  ✗ Invalid syntax was accepted"
        cat "$LOG_FILE"
        FAILED=$((FAILED + 1))
        FAILED_TESTS+=("invalid/$BASENAME (should fail)")
    else
        if [ -f "$C_FILE" ]; then
            echo "  ✗ Compiler failed but still emitted $C_FILE"
            FAILED=$((FAILED + 1))
            FAILED_TESTS+=("invalid/$BASENAME (unexpected C output)")
        else
            echo "  ✓ Invalid syntax rejected"
            PASSED=$((PASSED + 1))
        fi
    fi

    rm -f "$LOG_FILE"
    echo ""
done

# Clean up binaries
echo "Cleaning up test binaries..."
cleanup_artifacts
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
