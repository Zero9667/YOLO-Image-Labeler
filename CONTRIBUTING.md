# Contributing to YOLO Image Labeler

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, package versions)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Clear use case** for the enhancement
- **Expected behavior** and benefits
- **Possible implementation** approach (if known)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**: `git commit -m 'Add amazing feature'`
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/yolo-image-labeler.git
cd yolo-image-labeler

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise

### Code Organization

```python
def function_name(param1, param2):
    """
    Brief description of function.
    
    Args:
        param1 (type): Description
        param2 (type): Description
    
    Returns:
        type: Description
    """
    # Implementation
    pass
```

### Comments

- Use English for all comments
- Explain **why**, not **what** (code should be self-explanatory)
- Update comments when code changes

## Testing

Currently, the project doesn't have automated tests, but manual testing is essential:

- Test all modified features
- Test on different operating systems if possible
- Test with various image sizes and formats
- Test YOLO integration with different models

## Commit Messages

Write clear, concise commit messages:

```
Add feature: Brief description

More detailed explanation if needed.
Explain why this change is necessary.
```

Good examples:
- `Add zoom feature with Ctrl+MouseWheel`
- `Fix: Rectangle coordinates not scaling correctly`
- `Refactor: Improve label management code structure`

Bad examples:
- `Fixed stuff`
- `Update`
- `Changed some files`

## Feature Requests

Before implementing major features:

1. **Open an issue** to discuss the feature
2. **Wait for feedback** from maintainers
3. **Get approval** before starting work
4. **Create a draft PR** for early feedback

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and beginners
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Other unprofessional conduct

## Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- Automated testing framework
- CI/CD pipeline setup
- Performance optimizations
- Documentation improvements

### Features
- Export to other annotation formats (COCO, Pascal VOC)
- Polygon annotation support
- Segmentation mask support
- Multi-user annotation tracking

### UI/UX
- Dark mode support
- Customizable themes
- Better keyboard shortcut system
- Improved error messages

### Integration
- Cloud storage integration (S3, GCS)
- Database support for annotations
- Export to training frameworks
- Batch processing tools

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion
- Contact maintainers directly

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to YOLO Image Labeler! 🎉
