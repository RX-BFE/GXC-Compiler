SHELL := /bin/sh

PYTHON ?= python3
GCC ?= gcc
COMPILER := Compiler/main.py
TEST_DIR := test
INVALID_TEST_DIR := $(TEST_DIR)/invalid

VALID_GXC := $(wildcard $(TEST_DIR)/*.gxc)
INVALID_GXC := $(wildcard $(INVALID_TEST_DIR)/*.gxc)

VALID_BINARIES := $(patsubst $(TEST_DIR)/%.gxc,$(TEST_DIR)/%,$(VALID_GXC))
INVALID_BINARIES := $(patsubst $(INVALID_TEST_DIR)/%.gxc,$(INVALID_TEST_DIR)/%,$(INVALID_GXC))
INVALID_C_FILES := $(patsubst $(INVALID_TEST_DIR)/%.gxc,$(INVALID_TEST_DIR)/%.c,$(INVALID_GXC))

.DEFAULT_GOAL := test

.PHONY: test test-valid test-invalid clean clean-artifacts list-tests

test:
	@set -eu; \
	trap '$(MAKE) --no-print-directory clean-artifacts >/dev/null' EXIT; \
	$(MAKE) --no-print-directory clean-artifacts >/dev/null; \
	$(MAKE) --no-print-directory test-valid; \
	$(MAKE) --no-print-directory test-invalid; \
	echo "========================================"; \
	echo "Test Summary"; \
	echo "========================================"; \
	echo "Valid tests:   $(words $(VALID_GXC))"; \
	echo "Invalid tests: $(words $(INVALID_GXC))"; \
	echo "All tests passed! ✓"

test-valid:
	@set -eu; \
	if [ -z "$(strip $(VALID_GXC))" ]; then \
		echo "No valid .gxc files found in $(TEST_DIR)"; \
		exit 1; \
	fi; \
	echo "========================================"; \
	echo "GXC Compiler Test Runner"; \
	echo "========================================"; \
	echo ""; \
	echo "Found $(words $(VALID_GXC)) valid test files:"; \
	for file in $(VALID_GXC); do \
		echo "  - $$(basename "$$file")"; \
	done; \
	echo ""; \
	if [ -n "$(strip $(INVALID_GXC))" ]; then \
		echo "Found $(words $(INVALID_GXC)) invalid syntax tests:"; \
		for file in $(INVALID_GXC); do \
			echo "  - invalid/$$(basename "$$file")"; \
		done; \
		echo ""; \
	fi; \
	passed=0; \
	failed=0; \
	failed_tests=""; \
	for gxc_file in $(VALID_GXC); do \
		base_name=$$(basename "$$gxc_file" .gxc); \
		c_file="$(TEST_DIR)/$$base_name.c"; \
		binary="$(TEST_DIR)/$$base_name"; \
		log_file=$$(mktemp); \
		echo "----------------------------------------"; \
		echo "Testing: $$base_name"; \
		echo "----------------------------------------"; \
		echo "  → Compiling $$base_name.gxc to $$base_name.c..."; \
		if $(PYTHON) "$(COMPILER)" "$$gxc_file" > "$$log_file" 2>&1; then \
			echo "  ✓ Compilation to C successful"; \
		else \
			echo "  ✗ Compilation to C failed"; \
			cat "$$log_file"; \
			failed=$$((failed + 1)); \
			failed_tests="$$failed_tests $$base_name (gxc→c)"; \
			rm -f "$$log_file"; \
			continue; \
		fi; \
		echo "  → Compiling $$base_name.c to executable..."; \
		if $(GCC) "$$c_file" -o "$$binary" > "$$log_file" 2>&1; then \
			echo "  ✓ C compilation successful"; \
		else \
			echo "  ✗ C compilation failed"; \
			cat "$$log_file"; \
			failed=$$((failed + 1)); \
			failed_tests="$$failed_tests $$base_name (c→binary)"; \
			rm -f "$$log_file"; \
			continue; \
		fi; \
		echo "  → Running $$base_name..."; \
		if "$$binary" > /dev/null 2>&1; then \
			echo "  ✓ Execution successful"; \
			passed=$$((passed + 1)); \
		else \
			echo "  ✗ Execution failed"; \
			failed=$$((failed + 1)); \
			failed_tests="$$failed_tests $$base_name (execution)"; \
		fi; \
		rm -f "$$log_file"; \
		echo ""; \
	done; \
	if [ $$failed -gt 0 ]; then \
		echo "Failed tests:"; \
		for test in $$failed_tests; do \
			echo "  ✗ $$test"; \
		done; \
		echo ""; \
		exit 1; \
	fi

test-invalid:
	@set -eu; \
	if [ -z "$(strip $(INVALID_GXC))" ]; then \
		exit 0; \
	fi; \
	passed=0; \
	failed=0; \
	failed_tests=""; \
	for gxc_file in $(INVALID_GXC); do \
		base_name=$$(basename "$$gxc_file" .gxc); \
		c_file="$(INVALID_TEST_DIR)/$$base_name.c"; \
		log_file=$$(mktemp); \
		echo "----------------------------------------"; \
		echo "Testing invalid syntax: invalid/$$base_name"; \
		echo "----------------------------------------"; \
		echo "  → Expecting compilation failure..."; \
		if $(PYTHON) "$(COMPILER)" "$$gxc_file" > "$$log_file" 2>&1; then \
			echo "  ✗ Invalid syntax was accepted"; \
			cat "$$log_file"; \
			failed=$$((failed + 1)); \
			failed_tests="$$failed_tests invalid/$$base_name (should fail)"; \
		else \
			if [ -f "$$c_file" ]; then \
				echo "  ✗ Compiler failed but still emitted $$c_file"; \
				failed=$$((failed + 1)); \
				failed_tests="$$failed_tests invalid/$$base_name (unexpected C output)"; \
			else \
				echo "  ✓ Invalid syntax rejected"; \
				passed=$$((passed + 1)); \
			fi; \
		fi; \
		rm -f "$$log_file"; \
		echo ""; \
	done; \
	if [ $$failed -gt 0 ]; then \
		echo "Failed tests:"; \
		for test in $$failed_tests; do \
			echo "  ✗ $$test"; \
		done; \
		echo ""; \
		exit 1; \
	fi

clean-artifacts:
	@rm -f $(VALID_BINARIES) $(INVALID_BINARIES) $(INVALID_C_FILES)

clean: clean-artifacts

list-tests:
	@echo "Valid tests:"; \
	for file in $(VALID_GXC); do \
		echo "  - $$(basename "$$file")"; \
	done; \
	if [ -n "$(strip $(INVALID_GXC))" ]; then \
		echo "Invalid tests:"; \
		for file in $(INVALID_GXC); do \
			echo "  - invalid/$$(basename "$$file")"; \
		done; \
	fi
