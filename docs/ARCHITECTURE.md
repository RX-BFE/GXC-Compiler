# GRC Compiler Architecture

## Project Structure
```
grc-compiler/
├── Compiler/
│   ├── lex.py      # Lexer - tokenizes source code
│   ├── parser.py   # Parser - builds AST from tokens
│   ├── nodes.py    # AST node definitions
│   ├── c99.py      # Code generator - AST to C99
│   └── main.py     # Entry point
├── docs/
│   └── ARCHITECTURE.md
└── test/
    ├── *.gcx       # Test source files
    └── run_tests.sh # Automated test runner script
```

## Compilation Pipeline

### 1. Lexical Analysis (`lex.py`)
- Input: Raw source code string
- Output: Stream of tokens
- Uses regex patterns to identify keywords, identifiers, numbers, and operators

### 2. Parsing (`parser.py`)
- Input: Token stream from lexer
- Output: Abstract Syntax Tree (AST)
- Implements recursive descent parsing

### 3. AST Representation (`nodes.py`)
- Dataclass-based node definitions
- Expression nodes: `Number`, `Identifier`, `BinaryOp`
- Statement nodes: `Let`, `Assign`, `Print`, `If`, `Elif`, `Else`
- Root node: `Program`

### 4. Code Generation (`c99.py`)
- Input: AST from parser
- Output: C99 source code
- Generates complete C program with `main()` function

## Testing

### Automated Test Runner
The project includes an automated test runner script (`test/run_tests.sh`) that:
- Compiles all `.gxc` test files to C code
- Compiles C code to executables
- Runs all tests and reports results
- Automatically cleans up binaries after testing

### Running Tests
```bash
cd test
./run_tests.sh
```

### Manual Testing
To manually compile and run a single test:
```bash
cd Compiler
python main.py ../test/filename.gxc
cd ../test
gcc filename.c -o filename
./filename
```