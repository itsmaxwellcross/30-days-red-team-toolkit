# Contributing to 30 Days of Red Team Toolkit

Thank you for your interest in contributing to the 30 Days of Red Team Toolkit! This project aims to provide educational, well-documented tools for authorized security testing and red team operations.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Guidelines](#development-guidelines)
- [Coding Standards](#coding-standards)
- [Submitting Contributions](#submitting-contributions)
- [Security and Ethics](#security-and-ethics)
- [Tool Documentation Standards](#tool-documentation-standards)
- [Testing Requirements](#testing-requirements)
- [Community](#community)

---

## Code of Conduct

### Our Commitment

This project is dedicated to providing educational resources for **authorized security testing only**. All contributors must:

- ✅ Promote ethical hacking and responsible disclosure
- ✅ Emphasize the importance of authorization and legal compliance
- ✅ Include appropriate warnings and disclaimers
- ✅ Respect privacy and confidentiality
- ✅ Foster an inclusive and welcoming community

### Unacceptable Behavior

- ❌ Promoting illegal activities or unauthorized access
- ❌ Sharing tools intended for malicious purposes
- ❌ Removing or weakening safety disclaimers
- ❌ Harassment or discrimination of any kind
- ❌ Sharing credentials, exploits, or attack details from real systems without authorization

**Violations may result in removal from the project.**

---

## How Can I Contribute?

### 1. Reporting Bugs

Found a bug? Help us fix it!

**Before submitting:**
- Check existing [Issues](https://github.com/yourusername/30-days-red-team-toolkit/issues)
- Verify the bug is reproducible
- Test on the recommended Python version (3.8+)

**Bug Report Template:**
```markdown
**Description:**
Clear description of the bug

**To Reproduce:**
Steps to reproduce the behavior:
1. Run command '...'
2. With parameters '...'
3. See error

**Expected Behavior:**
What should happen

**Environment:**
- OS: [e.g., Ubuntu 22.04, Windows 11]
- Python Version: [e.g., 3.10.5]
- Tool: [e.g., nmap_scanner.py from Day 3]

**Error Output:**
```
Paste error messages here
```

**Additional Context:**
Any other relevant information
```

### 2. Suggesting Enhancements

Have an idea for improvement?

**Enhancement Request Template:**
```markdown
**Feature Description:**
Clear description of the enhancement

**Use Case:**
How would this benefit users?

**Proposed Solution:**
Your suggested implementation

**Alternatives Considered:**
Other approaches you've thought about

**Additional Context:**
Relevant examples or references
```

### 3. Contributing Code

We welcome:
- ✅ Bug fixes
- ✅ New tools that fit the curriculum
- ✅ Performance improvements
- ✅ Documentation improvements
- ✅ Test coverage improvements
- ✅ Additional features for existing tools

### 4. Improving Documentation

Documentation contributions are highly valued:
- Fix typos or unclear explanations
- Add usage examples
- Create tutorials or guides
- Translate documentation
- Improve code comments

---

## Getting Started

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/30-days-red-team-toolkit.git
   cd 30-days-red-team-toolkit
   ```

3. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/30-days-red-team-toolkit.git
   ```

### Set Up Development Environment

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate  # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

### Create a Branch

```bash
git checkout -b feature/your-feature-name
# OR
git checkout -b fix/your-bug-fix
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications

---

## Development Guidelines

### Project Structure

```
30-days-red-team-toolkit/
├── 01-reconnaissance/          # Day 1 tools
│   ├── subdomain_enum.py
│   ├── port_scanner.py
│   └── README.md
├── 02-scanning/                # Day 2 tools
│   ├── nmap_scanner.py
│   └── README.md
├── ...
├── docs/                       # Additional documentation
│   ├── setup-guide.md
│   └── troubleshooting.md
├── tests/                      # Test files
│   ├── test_reconnaissance.py
│   └── test_scanning.py
├── utils/                      # Shared utilities
│   ├── network_utils.py
│   └── output_utils.py
├── .github/                    # GitHub-specific files
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── CONTRIBUTING.md             # This file
├── LICENSE
└── README.md
```

### File Organization

Each day's directory should contain:
- **Tool scripts** (`.py` files)
- **README.md** - Documentation for that day's tools
- **examples/** (optional) - Example outputs or usage scenarios
- **payloads/** (optional) - Sample payloads or templates

---

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some specific conventions:

#### 1. Code Formatting

- **Line length:** 88 characters (Black formatter default)
- **Indentation:** 4 spaces (no tabs)
- **String quotes:** Double quotes for strings, single quotes for dict keys
- **Imports:** Organized and grouped (stdlib, third-party, local)

```python
# Standard library
import os
import sys
from datetime import datetime

# Third-party
import requests
from colorama import Fore, Style

# Local
from utils.network_utils import validate_ip
```

#### 2. Naming Conventions

```python
# Classes: PascalCase
class PortScanner:
    pass

# Functions and methods: snake_case
def scan_target(host, port):
    pass

# Constants: UPPER_CASE
MAX_THREADS = 100
DEFAULT_TIMEOUT = 30

# Private methods: _leading_underscore
def _internal_helper(self):
    pass

# Variables: snake_case
target_host = "192.168.1.1"
port_list = [80, 443, 8080]
```

#### 3. Documentation

**Every tool must include:**

```python
#!/usr/bin/env python3
"""
Tool Name - Brief Description

Detailed description of what the tool does, its purpose,
and how it fits into the red team toolkit.

Usage:
    python3 tool_name.py --target 192.168.1.1 --ports 80,443

Author: Your Name
Date: YYYY-MM-DD
Day: X of 30 Days of Red Team
"""

import sys
import argparse


class ToolClass:
    """
    Main class description.
    
    Attributes:
        attribute1 (type): Description
        attribute2 (type): Description
    """
    
    def __init__(self, config):
        """
        Initialize the tool.
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config
    
    def main_method(self, param1, param2):
        """
        Method description.
        
        Args:
            param1 (str): Description of param1
            param2 (int): Description of param2
        
        Returns:
            dict: Dictionary containing results with keys:
                - 'success' (bool): Operation success status
                - 'data' (list): Result data
                - 'error' (str): Error message if failed
        
        Raises:
            ValueError: If param1 is invalid
            ConnectionError: If connection fails
        """
        pass


def main():
    """Main entry point for the tool."""
    parser = argparse.ArgumentParser(
        description='Tool description',
        epilog='Example: python3 tool.py --target 192.168.1.1'
    )
    
    # Add arguments
    parser.add_argument('--target', required=True,
                       help='Target IP address or hostname')
    
    args = parser.parse_args()
    
    # Tool logic
    print("[*] Starting tool...")


if __name__ == "__main__":
    main()
```

#### 4. Error Handling

Always include proper error handling:

```python
def scan_port(host, port, timeout=5):
    """
    Scan a single port on target host.
    
    Args:
        host (str): Target hostname or IP
        port (int): Port number to scan
        timeout (int): Connection timeout in seconds
    
    Returns:
        dict: Scan result
    """
    try:
        # Validate inputs
        if not isinstance(port, int) or not (1 <= port <= 65535):
            raise ValueError(f"Invalid port number: {port}")
        
        # Perform operation
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        return {
            'success': True,
            'host': host,
            'port': port,
            'state': 'open' if result == 0 else 'closed'
        }
    
    except ValueError as e:
        return {
            'success': False,
            'error': f"Validation error: {e}"
        }
    except socket.timeout:
        return {
            'success': False,
            'error': f"Connection timeout after {timeout}s"
        }
    except socket.error as e:
        return {
            'success': False,
            'error': f"Socket error: {e}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Unexpected error: {e}"
        }
```

#### 5. Output and Logging

Use consistent output formatting:

```python
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Standard output format
print(f"{Fore.BLUE}[*]{Style.RESET_ALL} Information message")
print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Success message")
print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} Warning message")
print(f"{Fore.RED}[-]{Style.RESET_ALL} Error message")

# Progress indicators
print(f"{Fore.CYAN}[~]{Style.RESET_ALL} Processing...")
```

---

## Tool Requirements

### Every Tool Must Include:

#### 1. **Ethical Disclaimer**

```python
"""
ETHICAL USE ONLY
================
This tool is for authorized security testing only.
Unauthorized access to computer systems is illegal.

Always:
- Get written permission before testing
- Respect scope limitations
- Follow responsible disclosure
- Comply with applicable laws
"""
```

#### 2. **Argument Parsing**

Use `argparse` for command-line arguments:

```python
parser = argparse.ArgumentParser(
    description='Tool description',
    epilog='Example: python3 tool.py --help'
)

# Required arguments
parser.add_argument('--target', required=True,
                   help='Target system')

# Optional arguments with defaults
parser.add_argument('--timeout', type=int, default=30,
                   help='Timeout in seconds (default: 30)')

# Boolean flags
parser.add_argument('--verbose', action='store_true',
                   help='Enable verbose output')

args = parser.parse_args()
```

#### 3. **Input Validation**

```python
def validate_ip(ip_address):
    """
    Validate IP address format.
    
    Args:
        ip_address (str): IP address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        parts = ip_address.split('.')
        if len(parts) != 4:
            return False
        return all(0 <= int(part) <= 255 for part in parts)
    except (ValueError, AttributeError):
        return False


def validate_port(port):
    """Validate port number (1-65535)."""
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except (ValueError, TypeError):
        return False
```

#### 4. **Output Options**

Support multiple output formats:

```python
def save_results(results, output_file, format='json'):
    """
    Save results to file.
    
    Args:
        results (dict): Results to save
        output_file (str): Output file path
        format (str): Output format ('json', 'csv', 'txt')
    """
    if format == 'json':
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
    
    elif format == 'csv':
        # CSV implementation
        pass
    
    elif format == 'txt':
        # Plain text implementation
        pass
```

#### 5. **Progress Indication**

For long-running operations:

```python
from tqdm import tqdm

# Progress bar
for item in tqdm(items, desc="Scanning"):
    process(item)

# Manual progress
total = len(items)
for i, item in enumerate(items, 1):
    process(item)
    print(f"\rProgress: {i}/{total} ({i*100//total}%)", end='')
print()  # New line after completion
```

---

## Testing Requirements

### Unit Tests

Write tests for all new functionality:

```python
# tests/test_reconnaissance.py
import unittest
from reconnaissance.subdomain_enum import SubdomainEnumerator


class TestSubdomainEnumerator(unittest.TestCase):
    """Test cases for SubdomainEnumerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.enum = SubdomainEnumerator('example.com')
    
    def test_domain_validation(self):
        """Test domain validation."""
        self.assertTrue(self.enum.validate_domain('example.com'))
        self.assertFalse(self.enum.validate_domain('invalid domain'))
    
    def test_subdomain_discovery(self):
        """Test subdomain discovery."""
        result = self.enum.enumerate()
        self.assertIsInstance(result, dict)
        self.assertIn('subdomains', result)
    
    def tearDown(self):
        """Clean up after tests."""
        pass


if __name__ == '__main__':
    unittest.main()
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_reconnaissance.py

# Run with coverage
python -m pytest --cov=. --cov-report=html

# Run specific test
python -m pytest tests/test_reconnaissance.py::TestSubdomainEnumerator::test_domain_validation
```

### Test Coverage Goals

- Aim for **>80% code coverage** for new code
- Test edge cases and error conditions
- Include integration tests where appropriate

---

## Submitting Contributions

### Pull Request Process

1. **Update your fork:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Make your changes:**
   - Write clean, documented code
   - Follow coding standards
   - Add tests
   - Update documentation

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add subdomain enumeration tool"
   ```
   
   **Commit message format:**
   ```
   <type>: <short description>
   
   <detailed description>
   
   <footer>
   ```
   
   **Types:**
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation only
   - `style`: Code style changes (formatting)
   - `refactor`: Code refactoring
   - `test`: Adding tests
   - `chore`: Maintenance tasks

4. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request:**
   - Go to GitHub and create a PR
   - Use the PR template
   - Link related issues
   - Request review

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Related Issue
Fixes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe testing performed:
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Ethical disclaimer included (if applicable)
- [ ] No credentials or sensitive data committed

## Screenshots (if applicable)
Add screenshots or examples

## Additional Notes
Any additional context
```

### Code Review Process

1. **Automated checks** must pass:
   - Linting (flake8, pylint)
   - Type checking (mypy)
   - Tests (pytest)
   - Security scan (bandit)

2. **Manual review** by maintainers:
   - Code quality
   - Security considerations
   - Documentation completeness
   - Ethical compliance

3. **Feedback and revisions:**
   - Address reviewer comments
   - Push additional commits
   - Request re-review

4. **Merge:**
   - Once approved, maintainers will merge
   - Squash commits if necessary
   - Delete feature branch

---

## Security and Ethics

### Security Guidelines

1. **Never commit sensitive data:**
   - No API keys, tokens, or credentials
   - No real target information
   - No personally identifiable information (PII)

2. **Use safe examples:**
   ```python
   # Good - Use safe examples
   target = "example.com"
   api_key = "YOUR_API_KEY_HERE"
   
   # Bad - Don't commit real data
   target = "victim-company.com"
   api_key = "sk_live_abc123xyz789"
   ```

3. **Sanitize outputs:**
   - Remove sensitive information from error messages
   - Don't expose system paths in production
   - Redact credentials in logs

4. **Report vulnerabilities:**
   - Found a security issue? Email: security@project.com
   - **Do NOT** open public issues for security vulnerabilities
   - Follow responsible disclosure

### Ethical Guidelines

Every contribution must:

1. **Promote authorized testing:**
   - Include ethical use disclaimers
   - Emphasize the need for permission
   - Warn about legal consequences

2. **Educational focus:**
   - Teach defensive security
   - Explain detection methods
   - Include blue team perspective

3. **No weaponization:**
   - Don't create tools solely for attack
   - Include defensive capabilities
   - Provide removal/cleanup functions

4. **Responsible disclosure:**
   - Don't share 0-day exploits
   - Don't include real vulnerability details without coordination
   - Follow coordinated disclosure practices

---

## Documentation Standards

### Tool README Structure

Each day's `README.md` should include:

```markdown
# Day X - Topic Name

## Overview
Brief description of the day's focus

## Learning Objectives
- Objective 1
- Objective 2
- Objective 3

## Tools Included

### Tool 1: Name
**Purpose:** What it does
**Usage:**
```bash
python3 tool1.py --target example.com
```
**Features:**
- Feature 1
- Feature 2

### Tool 2: Name
...

## Prerequisites
- Requirement 1
- Requirement 2

## Installation
```bash
pip install -r requirements.txt
```

## Usage Examples

### Example 1: Basic Usage
```bash
python3 tool.py --target example.com
```

### Example 2: Advanced Usage
```bash
python3 tool.py --target example.com --advanced --output results.json
```

## Common Issues

### Issue 1
**Problem:** Description
**Solution:** Fix

## Further Reading
- Resource 1
- Resource 2

## Legal Notice
These tools are for authorized testing only...
```

### Code Comments

```python
# Good comments explain WHY, not WHAT
# Bad: Loop through ports
for port in ports:
    scan(port)

# Good: Scanning common ports first for faster results
for port in common_ports:
    scan(port)
```

---

## Community

### Communication Channels

- **GitHub Issues:** Bug reports, feature requests
- **GitHub Discussions:** General questions, ideas
- **Discord:** Real-time chat (link in README)
- **Twitter:** Updates and announcements (@project)

### Getting Help

**Before asking for help:**
1. Check existing documentation
2. Search closed issues
3. Review troubleshooting guide

**When asking questions:**
- Provide environment details (OS, Python version)
- Include error messages
- Share relevant code snippets
- Describe what you've tried

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Mentioned in project updates

### Becoming a Maintainer

Active contributors may be invited to become maintainers based on:
- Quality contributions
- Community involvement
- Ethical conduct
- Technical expertise

---

## Development Setup

### Recommended Tools

```bash
# Code formatting
pip install black isort

# Linting
pip install flake8 pylint

# Type checking
pip install mypy

# Testing
pip install pytest pytest-cov

# Pre-commit hooks
pip install pre-commit
```

### Pre-commit Configuration

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88']

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ['--profile=black']
```

Install hooks:
```bash
pre-commit install
```

### Code Quality Checks

Before submitting PR:

```bash
# Format code
black .
isort .

# Lint
flake8 .
pylint **/*.py

# Type check
mypy .

# Run tests
pytest --cov

# Security scan
bandit -r . -ll
```

---

## Questions?

Still have questions? We're here to help!

1. **Check the [FAQ](docs/FAQ.md)**
2. **Browse [GitHub Discussions](https://github.com/username/30-days-red-team-toolkit/discussions)**
3. **Open an [Issue](https://github.com/username/30-days-red-team-toolkit/issues)**
4. **Join our [Discord](link)**

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

## Thank You!

Thank you for contributing to 30 Days of Red Team Toolkit! Your efforts help make security education accessible to everyone.

**Remember:** With great power comes great responsibility. Use these tools ethically and legally.

Happy hacking (the legal kind)! 🛡️

---

**Last Updated:** 2024-11-21  
**Version:** 1.0.0