# Project TODO List

This document outlines the remaining tasks to bring the project to a production-ready state.

---

## 🎯 Success Criteria

The project is considered "complete" when the following criteria are met:
- [x] CI passes on all platforms
- [x] All tests pass
- [x] Reproducibility is guaranteed and verifiable
- [x] All formatting issues are resolved
- [ ] **< 10 mypy issues remaining** (currently 36)
- [ ] **> 60% test coverage** (currently ~49%)
- [ ] **Core modules are fully documented**

---

## 🚀 High Priority

### 1. Enhance Reproducibility Guarantees
*Goal: Make the analysis fully and formally reproducible by a third party.*
- [x] **Formalize Dependency Locking:**
    - [x] Use `pip-tools` to generate `requirements.txt` and `requirements-dev.txt` lock files.
    - [ ] Update the CI and `noxfile.py` to use these lock files for all installations.
- [x] **Commit Reference Outputs:**
    - [x] Create a `data/output/reference/` directory.
    - [x] Store a "golden copy" of the output for the test data (`2.tsv`).
    - [x] Modify the CI `reproducibility` job to compare the script's output against this reference file.
- [x] **Create a `REPRODUCIBILITY.md` Guide:**
    - [x] Document the exact steps for a third party to replicate the results using the lock files and reference output.

### 2. Achieve Full Type Safety
*Goal: Reduce mypy errors to fewer than 10.*
- [ ] **Add Missing Type Annotations:**
    - [ ] Add return type annotations to all functions.
    - [ ] Fix type mismatches in `relationship_extractor.py`.
    - [ ] Add proper type annotations to `benchmark.py` functions.
- [x] **Install Missing Type Stubs:**
    - [x] Run `pip install types-psutil` to resolve missing stub errors.

### 3. Fix Critical Module Imports
*Goal: Ensure all modules can be imported reliably.*
- [x] Fix missing analyzer modules in `src/analyzers/__init__.py`.
- [ ] Verify that all module imports are properly structured and relative where appropriate.

---

## 📝 Medium Priority

### 4. Improve Code Quality & Style
*Goal: Reduce Ruff linting issues to fewer than 20.*
- [ ] **Fix Line Length Violations:**
    - [ ] Break long lines in `tools/analyze_results.py`.
    - [ ] Fix long lines in `src/` modules.
- [ ] **Improve Exception Handling:**
    - [ ] Add `from err` to exception chains where appropriate (B904).
- [ ] **Cleanup Unused Variables:**
    - [ ] Remove unused variables in `tests/` and `tools/`.

### 5. Increase Test Coverage
*Goal: Increase test coverage to over 60%.*
- [x] **Add Tests for Untested Modules:**
    - [x] `src/benchmark.py`
    - [x] `src/verify_phase2.py`
    - [x] `src/data/versioning.py`

---

## 🎯 Low Priority

### 6. Finalize Documentation
*Goal: Ensure the project is well-documented and easy to understand.*
- [ ] **Add Missing Docstrings:**
    - [ ] Add docstrings to all `__init__` methods.
    - [ ] Add docstrings to all public functions.
    - [ ] Fix remaining docstring formatting issues.
- [ ] **Create Developer Documentation:**
    - [ ] Create a developer onboarding guide.
    - [ ] Add a troubleshooting guide to the main `README.md`.

### 7. Performance & Optimization
*Goal: Profile and optimize performance where necessary.*
- [ ] Profile memory usage in large file processing.
- [ ] Optimize relationship extraction algorithms if performance becomes an issue.
- [ ] Consider caching strategies for repeated operations.
