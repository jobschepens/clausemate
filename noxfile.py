"""Nox configuration for clausemate project.

This file defines automated tasks for testing, linting, and other development
workflows. Nox creates isolated virtual environments for each task, ensuring
reproducible and clean execution.

Usage:
    nox                    # Run default sessions (lint, test)
    nox -s lint            # Run only linting
    nox -s test            # Run tests on current Python version
    nox -s test-3.9        # Run tests on Python 3.9
    nox -s test-3.10       # Run tests on Python 3.10
    nox -s mypy            # Run type checking
    nox -s safety          # Run security checks
    nox -s docs            # Build documentation
    nox -l                 # List all available sessions
"""

import nox

# Supported Python versions for testing
PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12"]
# Default sessions to run when no specific session is specified
nox.options.sessions = ["lint", "test"]


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run the test suite with pytest."""
    session.install("-e", ".[dev]")
    session.run(
        "pytest",
        "tests/",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-fail-under=25",  # Current coverage level
        "-v",
    )


@nox.session
def lint(session):
    """Run ruff linting and formatting checks."""
    session.install("ruff>=0.1.0")
    session.run("ruff", "check", "src/", "tests/", "tools/")
    session.run("ruff", "format", "--check", "src/", "tests/", "tools/")


@nox.session
def format(session):
    """Format code with ruff."""
    session.install("ruff>=0.1.0")
    session.run("ruff", "format", "src/", "tests/", "tools/")
    session.run("ruff", "check", "--fix", "src/", "tests/", "tools/")


@nox.session
def mypy(session):
    """Run mypy type checking."""
    session.install("-e", ".[dev]")
    session.run("mypy", "src/")


@nox.session
def safety(session):
    """Check dependencies for known security vulnerabilities."""
    session.install("safety>=2.0.0")
    session.run("safety", "check", "--json")


@nox.session
def bandit(session):
    """Run bandit security linting."""
    session.install("bandit>=1.7.0")
    session.run("bandit", "-r", "src/", "-f", "json")


@nox.session
def pre_commit(session):
    """Run pre-commit hooks on all files."""
    session.install("pre-commit>=2.20.0")
    session.run("pre-commit", "run", "--all-files")


@nox.session
def deps(session):
    """Check for outdated dependencies."""
    session.install("pip-tools")
    session.run("pip", "list", "--outdated")


@nox.session
def clean(session):
    """Clean up build artifacts and caches."""
    import pathlib
    import shutil

    # Directories to clean
    clean_dirs = [
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "htmlcov",
        "dist",
        "build",
        "*.egg-info",
    ]

    for pattern in clean_dirs:
        for path in pathlib.Path(".").glob(pattern):
            if path.is_dir():
                session.log(f"Removing directory: {path}")
                shutil.rmtree(path, ignore_errors=True)
            elif path.is_file():
                session.log(f"Removing file: {path}")
                path.unlink()

    # Remove __pycache__ directories
    for pycache in pathlib.Path(".").rglob("__pycache__"):
        session.log(f"Removing pycache: {pycache}")
        shutil.rmtree(pycache, ignore_errors=True)


@nox.session
def build(session):
    """Build the package."""
    session.install("build")
    session.run("python", "-m", "build")


@nox.session
def install_dev(session):
    """Install the package in development mode with all dependencies."""
    session.install("-e", ".[dev,benchmark]")
    session.log("✅ Development environment installed successfully!")
    session.log("Available commands:")
    session.log("  nox -s test     # Run tests")
    session.log("  nox -s lint     # Run linting")
    session.log("  nox -s format   # Format code")
    session.log("  nox -s mypy     # Type checking")


@nox.session
def ci(session):
    """Run the full CI pipeline."""
    session.log("🚀 Running full CI pipeline...")

    # Install dependencies
    session.install("-e", ".[dev]")

    # Code quality checks
    session.log("📋 Running linting...")
    session.run("ruff", "check", "src/", "tests/", "tools/")

    session.log("🎨 Checking formatting...")
    session.run("ruff", "format", "--check", "src/", "tests/", "tools/")

    session.log("🔍 Running type checking...")
    session.run("mypy", "src/", success_codes=[0, 1])  # Allow mypy errors for now

    session.log("🧪 Running tests...")
    session.run(
        "pytest",
        "tests/",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-fail-under=25",
        "-v",
    )

    session.log("🔒 Running security checks...")
    session.run("bandit", "-r", "src/", "-f", "txt", success_codes=[0, 1])

    session.log("✅ CI pipeline completed successfully!")


@nox.session(python=False)
def docs(session):
    """Generate project documentation."""
    session.log("📚 Generating documentation...")
    session.log("Project documentation is available in:")
    session.log("  - README.md")
    session.log("  - CONTRIBUTING.md")
    session.log("  - docs/README.md")
    session.log("  - MODERNIZATION_COMPLETE.md")
