# Contributing to Project Intelligence Engine

First off, thank you for considering contributing! 🎉 Every contribution helps make this project better.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behaviour to the maintainers.

## How Can I Contribute?

### 🐛 Reporting Bugs

- Check [existing issues](https://github.com/ajithnow/projectintel/issues) first to avoid duplicates.
- Use the **Bug Report** issue template.
- Include steps to reproduce, expected vs. actual behaviour, and your environment details.

### 💡 Suggesting Features

- Open a [feature request](https://github.com/ajithnow/projectintel/issues/new) issue.
- Describe the problem you're solving and your proposed solution.
- Tag the issue with `enhancement`.

### 🔧 Submitting Code

1. Fork the repository.
2. Create a feature branch from `main` (`git checkout -b feature/my-feature`).
3. Make your changes (see [Development Setup](#development-setup) below).
4. Commit with a [meaningful message](#commit-messages).
5. Push to your fork and open a Pull Request.

## Development Setup

### Prerequisites

- **Python 3.13+**
- **PostgreSQL 14+**
- **[uv](https://docs.astral.sh/uv/)** — fast Python package manager

### Getting Started

```bash
# Clone your fork
git clone https://github.com/<your-username>/projectintel.git
cd projectintel

# Create venv and install all dependencies
uv sync

# Copy env and configure
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Run database migrations
alembic upgrade head

# Start the dev server
uvicorn main:app --reload
```

### Running Tests

```bash
# Full suite
pytest

# With coverage report
pytest --cov=features --cov-report=term-missing
```

### Linting & Formatting

```bash
# Format code
ruff format .

# Lint
ruff check .
```

## Coding Standards

- **Style**: Follow [PEP 8](https://peps.python.org/pep-0008/). We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.
- **Type hints**: All public functions must have type annotations.
- **Docstrings**: Use Google‑style docstrings for modules, classes, and public functions.
- **Feature modules**: New functionality should live inside `features/<feature_name>/` with its own `router.py`, `schema.py`, `models.py`, and `service.py` as needed.
- **Tests**: Every new feature or bug fix should include tests.

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <short summary>

<optional body>
```

### Types

| Type | Description |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, whitespace (no logic changes) |
| `refactor` | Code restructuring (no feature or fix) |
| `test` | Adding or updating tests |
| `chore` | Build, CI, tooling changes |

**Examples:**
```
feat(auth): add JWT token refresh endpoint
fix(users): handle duplicate email gracefully
docs: update contributing guidelines
```

## Pull Request Process

1. **Ensure your branch is up to date** with `main`.
2. **All tests pass** — CI will verify this automatically.
3. **Lint checks pass** — run `ruff check .` before pushing.
4. **Fill in the PR template** with a clear description of changes.
5. **Request a review** from at least one maintainer.
6. Once approved, a maintainer will merge your PR.

### PR Checklist

- [ ] My code follows the project's coding standards.
- [ ] I have added/updated tests for my changes.
- [ ] I have updated documentation if needed.
- [ ] All existing tests pass.
- [ ] My commit messages follow Conventional Commits.

---

Thank you for helping improve Project Intelligence Engine! 🚀
