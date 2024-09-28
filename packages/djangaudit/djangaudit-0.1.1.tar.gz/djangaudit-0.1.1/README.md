# Djangaudit

Djangaudit is a tool to help you audit your Django project. It will help you to find common security issues in your project.

## Installation

```bash
pip install djangaudit
```

Then, add it to your installed apps:

```python
INSTALLED_APPS = [
    ...
    'djangaudit',
    ...
]
```

## Usage

```bash
python manage.py audit_project
```

## What does it check?

1. Checking for large Python files (based on the AUDIT_MAX_LINES_PER_FILE setting): This is to help you identify files that are too large and may be difficult to maintain.
2. Checking for __init__.py files with code: This is to help you identify if you take advantage of the __init__.py files to execute code.
3. Checking the line length of Python files. The checker indicates the number of lines by groups (less than 80 characters wide, between 80 and 100, between 100 and 120, more than 120).
4. Check the versions of the libraries used in the project. The checker indicates if there are newer versions of the libraries used in the project.

## Contribute

This package is a very humble django application that I created to help me audit my projects. If you have any suggestions, please feel free to open an issue or a pull request.

## License

MIT
