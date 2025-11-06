# Contributing to Image Tool Pro

Thank you for your interest in contributing to Image Tool Pro! We welcome contributions from the community and are grateful for your support.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Translation Contributions](#translation-contributions)

---

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

**In short:**
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Keep discussions professional

---

## How Can I Contribute?

There are many ways to contribute to Image Tool Pro:

### 🐛 Report Bugs
Found a bug? [Open an issue](https://github.com/yourusername/image-tool-pro/issues/new?template=bug_report.md) with details.

### 💡 Suggest Features
Have an idea? [Request a feature](https://github.com/yourusername/image-tool-pro/issues/new?template=feature_request.md).

### 📖 Improve Documentation
Help us make the docs better! Fix typos, clarify instructions, or add examples.

### 🌍 Add Translations
Add support for new languages or improve existing translations.

### 💻 Write Code
Fix bugs, implement features, or improve performance.

### 🧪 Test & Review
Test pull requests and provide feedback on proposed changes.

---

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Python 3.7+** installed
- **Git** for version control
- **pip** package manager
- A **GitHub account**

### Fork and Clone

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/image-tool-pro.git
cd image-tool-pro
```

3. **Add upstream remote**:

```bash
git remote add upstream https://github.com/yourusername/image-tool-pro.git
```

### Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pyinstaller  # For building executables
```

### Run the Application

```bash
python main.py
```

---

## Development Workflow

### 1. Create a Branch

Always create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications

### 2. Make Changes

- Write clean, readable code
- Follow the [coding standards](#coding-standards)
- Test your changes thoroughly
- Update documentation if needed

### 3. Commit Changes

```bash
git add .
git commit -m "Brief description of changes"
```

See [commit guidelines](#commit-guidelines) for details.

### 4. Keep Your Branch Updated

```bash
git fetch upstream
git rebase upstream/main
```

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Open a Pull Request

Go to GitHub and [create a pull request](https://github.com/yourusername/image-tool-pro/compare) from your branch.

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) style guidelines:

- **Indentation**: 4 spaces (no tabs)
- **Line length**: Maximum 100 characters
- **Naming**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### Code Quality

```python
# Good: Clear, descriptive names
def calculate_crop_dimensions(width, height, center_x, center_y):
    """Calculate crop box dimensions based on center point."""
    pass

# Bad: Unclear, abbreviated names
def calc_dim(w, h, cx, cy):
    pass
```

### Documentation

- Add docstrings to all functions and classes
- Include parameter types and return values
- Provide usage examples for complex functions

```python
def center_crop(image, width, height, center_x=None, center_y=None):
    """
    Crop image from a center point with specified dimensions.

    Args:
        image (PIL.Image): Source image to crop
        width (int): Desired crop width in pixels
        height (int): Desired crop height in pixels
        center_x (int, optional): X coordinate of center point. Defaults to image center.
        center_y (int, optional): Y coordinate of center point. Defaults to image center.

    Returns:
        PIL.Image: Cropped image

    Example:
        >>> img = Image.open('photo.jpg')
        >>> cropped = center_crop(img, 800, 600, 400, 300)
    """
    pass
```

### Comments

- Explain **why**, not **what**
- Use comments for complex logic
- Keep comments up-to-date

```python
# Good: Explains reasoning
# Use binary search to find optimal quality setting
# This is faster than linear search for large images
quality = binary_search_quality(min_q=10, max_q=95)

# Bad: States the obvious
# Set quality to result of function
quality = binary_search_quality(min_q=10, max_q=95)
```

---

## Commit Guidelines

### Commit Message Format

```
<type>: <subject>

<body> (optional)

<footer> (optional)
```

### Types

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code formatting (no logic changes)
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Build tasks, dependencies

### Examples

```bash
# Good commits
feat: Add batch processing support for multiple images
fix: Correct boundary calculation in center crop
docs: Update installation instructions for Windows
refactor: Extract compression logic into separate module

# Bad commits
fixed stuff
update
changes
asdfgh
```

### Best Practices

- Use present tense: "Add feature" not "Added feature"
- Keep subject line under 50 characters
- Provide detailed body for complex changes
- Reference issues: "Fixes #123" or "Related to #456"

---

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up-to-date with main

### PR Title

Use the same format as commit messages:

```
feat: Add support for WEBP format
fix: Resolve crash when opening large PNG files
```

### PR Description

Use the [pull request template](.github/PULL_REQUEST_TEMPLATE.md):

1. **Summary**: What does this PR do?
2. **Changes**: List of modifications
3. **Testing**: How did you test?
4. **Screenshots**: Visual changes (if applicable)
5. **Related Issues**: Link to issues

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged
4. Your contribution will be acknowledged in the changelog

### After Merging

- Delete your feature branch
- Update your fork:

```bash
git checkout main
git pull upstream main
git push origin main
```

---

## Reporting Bugs

### Before Reporting

- Check if the bug has already been reported
- Verify it's reproducible in the latest version
- Gather relevant information

### Bug Report Template

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) including:

1. **Description**: What happened?
2. **Steps to Reproduce**: How to trigger the bug?
3. **Expected Behavior**: What should happen?
4. **Actual Behavior**: What actually happened?
5. **Environment**:
   - OS version
   - Python version
   - Application version
6. **Screenshots**: Visual evidence (if applicable)
7. **Error Messages**: Full traceback or error text

---

## Suggesting Features

### Feature Request Template

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) including:

1. **Problem**: What problem does this solve?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Other approaches considered?
4. **Use Cases**: Who would benefit?
5. **Additional Context**: Mockups, examples, etc.

### Feature Discussion

- Features may be discussed before implementation
- Maintainers will label and prioritize requests
- Some features may be rejected if out of scope

---

## Translation Contributions

### Adding a New Language

1. Open `src/language.py`
2. Add new language code to `LANGUAGES` dict:

```python
LANGUAGES = {
    'en': { ... },
    'zh': { ... },
    'es': {  # Spanish
        'app_title': 'Herramienta de Procesamiento de Imágenes',
        'menu_file': 'Archivo',
        # ... 80+ strings
    }
}
```

3. Translate all 80+ strings
4. Update `src/app.py` to add menu option:

```python
language_menu.add_command(
    label='Español',
    command=lambda: self.change_language('es')
)
```

5. Test thoroughly in the new language

### Translation Guidelines

- Maintain consistent terminology
- Keep text length similar to English (for UI layout)
- Use formal tone for professional contexts
- Test all UI elements after translation

---

## Questions?

- **Documentation**: Check [docs/](docs/) folder
- **Issues**: Browse [existing issues](https://github.com/yourusername/image-tool-pro/issues)
- **Discussions**: Start a [discussion](https://github.com/yourusername/image-tool-pro/discussions)

---

## Recognition

Contributors will be:
- Listed in the [CHANGELOG.md](CHANGELOG.md)
- Acknowledged in release notes
- Featured in the project README (for significant contributions)

Thank you for making Image Tool Pro better! 🎉
