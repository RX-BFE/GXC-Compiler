# GXC Compiler

GXC is a small compiler that translates `.gxc` source files into C99.

## Install

```bash
uv sync
uv sync --group dev
```

## CLI

After installation, compile a file with:

```bash
uv run gxc path/to/file.gxc
```

## Test

```bash
make test
make lint
```
