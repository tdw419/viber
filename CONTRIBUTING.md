# Contributing to Viber

We welcome contributions to the Viber development environment! Whether you're fixing a bug, adding a new feature, or improving the documentation, your help is appreciated.

## Getting Started

1.  **Fork the repository**: Click the "Fork" button at the top right of the repository page.
2.  **Clone your fork**: `git clone https://github.com/YOUR_USERNAME/viber.git`
3.  **Create a branch**: `git checkout -b your-feature-branch`
4.  **Make your changes**: Make your desired changes to the codebase.
5.  **Commit your changes**: `git commit -m "Add some feature"`
6.  **Push to your fork**: `git push origin your-feature-branch`
7.  **Create a pull request**: Open a pull request from your fork to the main repository.

## Development Environment

Before you start, make sure you have the following installed:

*   Python 3.11+
*   `venv`

To set up the development environment, run the following commands from the root of the repository:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Code Style

We use the `black` code formatter to maintain a consistent code style. Before submitting a pull request, please make sure your code is formatted by running:

```bash
pip install black
black .
```

## Reporting Bugs

If you find a bug, please open an issue and provide the following information:

*   A clear and concise description of the bug.
*   Steps to reproduce the bug.
*   The expected behavior.
*   The actual behavior.
*   Your operating system and Python version.

## Suggesting Enhancements

If you have an idea for a new feature or an improvement to an existing one, please open an issue and describe your suggestion in detail.

Thank you for contributing to Viber!
