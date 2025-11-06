# Development Guide

This guide provides detailed information for developers who want to contribute to Image Tool Pro or understand its internal architecture.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [Development Workflow](#development-workflow)
- [Building Executables](#building-executables)
- [Testing](#testing)
- [Debugging](#debugging)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)

---

## Architecture Overview

Image Tool Pro follows the **MVC (Model-View-Controller)** architecture pattern:

```
┌─────────────────────────────────────────┐
│            View (app.py)                │
│  - Main window UI                       │
│  - User interactions                    │
│  - Visual feedback                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     Controller (ui_components.py)       │
│  - UI component widgets                 │
│  - Event handling                       │
│  - User input validation                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Model (image_processor.py)           │
│  - Image processing algorithms          │
│  - Business logic                       │
│  - Data transformations                 │
└─────────────────────────────────────────┘
```

### Key Design Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Coordinate Transformation**: Canvas coordinates ↔ original image coordinates
3. **Event-Driven**: User interactions trigger processing workflows
4. **Stateful UI**: Application maintains image state and processing history

---

## Development Setup

### Prerequisites

- **Python 3.7 - 3.11** (3.11 recommended for performance)
- **Git** for version control
- **pip** package manager
- **Virtual environment** (recommended)

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/image-tool-pro.git
cd image-tool-pro

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pyinstaller pytest flake8

# Verify installation
python main.py
```

### IDE Configuration

#### VS Code

Create `.vscode/settings.json`:

```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "autopep8",
    "python.linting.flake8Args": ["--max-line-length=100"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

#### PyCharm

- Set Python interpreter to virtual environment
- Enable PEP 8 code style inspections
- Configure file watchers for auto-formatting

---

## Project Structure

```
image-tool-pro/
│
├── main.py                    # Application entry point
│
├── src/                       # Source code directory
│   ├── app.py                # Main application window (MVC: View)
│   ├── image_processor.py    # Image processing logic (MVC: Model)
│   ├── crop_tool.py          # Interactive cropping tool
│   ├── ui_components.py      # Reusable UI widgets (MVC: Controller)
│   └── language.py           # Multi-language support system
│
├── assets/                    # Application assets
│   ├── icon.ico              # Windows application icon
│   ├── icon.png              # High-res icon version
│   └── screenshots/          # README screenshots
│
├── docs/                      # Documentation
│   ├── DEVELOPMENT.md        # This file
│   ├── FAQ.md                # Frequently asked questions
│   └── USER_GUIDE.md         # End-user documentation
│
├── .github/                   # GitHub configuration
│   ├── ISSUE_TEMPLATE/       # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
│
├── build_exe.py              # Build script for executables
├── build_simple.bat          # Windows batch build script
├── create_icon.py            # Icon generation script
│
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
├── README.md                # Main documentation (English)
├── README-zh.md             # Chinese documentation
├── CHANGELOG.md             # Version history
└── CONTRIBUTING.md          # Contribution guidelines
```

---

## Core Components

### 1. main.py

**Purpose**: Application entry point

```python
import tkinter as tk
from src.app import ImageProcessorApp

def main():
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
```

**Responsibilities**:
- Initialize Tkinter root window
- Create main application instance
- Start event loop

---

### 2. src/app.py (View Layer)

**Purpose**: Main application window and UI management

**Key Features**:
- Menu bar (File, Edit, Language, Help)
- Canvas for image display
- Control panels (crop, compress, actions)
- Status bar for feedback
- Event handling and coordination

**Important Methods**:

```python
def load_image(self)
    """Load image from file and display on canvas."""

def save_image(self)
    """Save processed image to file."""

def execute_crop(self)
    """Execute crop operation using current crop box."""

def execute_center_crop(self)
    """Execute center-point crop with specified dimensions."""

def compress_image(self)
    """Compress image to target file size."""

def change_language(self, lang_code)
    """Switch interface language (requires restart)."""
```

**Coordinate System**:
- Maintains scale ratio between canvas and original image
- Converts canvas coordinates to image coordinates for processing

---

### 3. src/image_processor.py (Model Layer)

**Purpose**: Core image processing algorithms

**Key Functions**:

```python
def fit_image_to_canvas(image, canvas_width, canvas_height)
    """
    Resize image to fit canvas while maintaining aspect ratio.

    Returns:
        - resized PIL.Image
        - scale ratio
        - display width
        - display height
    """

def center_crop(image, width, height, center_x=None, center_y=None)
    """
    Crop image from center point with boundary handling.

    Algorithm:
    1. Calculate crop box boundaries
    2. Compute intersection with image bounds
    3. Crop valid region
    4. Return cropped image
    """

def compress_to_size(image, target_size_kb, output_format='JPEG')
    """
    Compress image to target file size using binary search.

    Algorithm:
    1. Binary search quality settings (1-95)
    2. Save to BytesIO and check size
    3. If target unreachable, reduce resolution
    4. Return compressed image
    """

def canvas_to_image_coords(canvas_x, canvas_y, scale, offset_x, offset_y)
    """Convert canvas coordinates to original image coordinates."""

def image_to_canvas_coords(img_x, img_y, scale, offset_x, offset_y)
    """Convert original image coordinates to canvas coordinates."""
```

**Algorithms**:

1. **Binary Search Compression**:
   - Time Complexity: O(log n) where n = quality range
   - Space Complexity: O(1)
   - Guarantees optimal quality for target size

2. **Boundary Intersection**:
   - Handles crops extending beyond image edges
   - Always returns valid crop region
   - No errors for out-of-bounds input

---

### 4. src/crop_tool.py

**Purpose**: Interactive cropping with mouse events

**State Machine**:

```
┌─────────────┐
│    IDLE     │ ◄──────────┐
└──────┬──────┘            │
       │ Mouse Down        │
       ▼                   │
┌─────────────┐            │
│  DRAGGING   │            │
│  (New Box)  │            │
└──────┬──────┘            │
       │ Mouse Up          │
       ▼                   │
┌─────────────┐            │
│  BOX EXISTS │ ───────────┘
│             │
│  • Move box │
│  • Resize   │
└─────────────┘
```

**Drag Modes**:
- `'new'` - Creating new crop box
- `'move'` - Moving existing box
- `'nw'`, `'ne'`, `'sw'`, `'se'` - Resizing from corners

**Corner Detection**:
- 10-pixel tolerance around corner handles
- Visual feedback with red rectangles

---

### 5. src/ui_components.py (Controller Layer)

**Purpose**: Reusable UI component widgets

**Components**:

1. **PixelInfoPanel**: Real-time dimension display
2. **CenterCropPanel**: Center point input controls
3. **CompressPanel**: Compression settings
4. **ActionPanel**: Save and preview buttons

**Design Pattern**: Composite Pattern
- Each component is self-contained
- Can be easily added/removed/reordered
- Maintains separation from main window logic

---

### 6. src/language.py

**Purpose**: Multi-language support system

**Architecture**:

```python
LANGUAGES = {
    'en': { 'key1': 'value1', 'key2': 'value2', ... },
    'zh': { 'key1': '值1', 'key2': '值2', ... }
}

class LanguageManager:
    def __init__(self):
        self.current_language = self.load_config()

    def get(self, key, **kwargs):
        """Get translated string with format substitution."""

    def set_language(self, lang_code):
        """Change language and persist to config."""
```

**Adding Translations**:
1. Add new language dict to `LANGUAGES`
2. Translate all 80+ strings
3. Update UI to add language menu option

---

## Development Workflow

### Adding a New Feature

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement Feature**:
   - Identify which layer (Model/View/Controller) to modify
   - Write clean, documented code
   - Follow coding standards

3. **Test Thoroughly**:
   - Manual testing with various images
   - Edge cases (large images, small images, different formats)
   - Performance testing

4. **Update Documentation**:
   - Update relevant docstrings
   - Add usage examples
   - Update CHANGELOG.md

5. **Commit and Push**:
   ```bash
   git add .
   git commit -m "feat: Description of feature"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**:
   - Use PR template
   - Provide screenshots/demos
   - Link related issues

---

## Building Executables

### Using build_exe.py

```bash
python build_exe.py
```

**Process**:
1. Cleans previous build artifacts
2. Runs PyInstaller with proper configuration
3. Copies assets and documentation
4. Creates release folder with all files

### Using build_simple.bat (Windows)

```cmd
build_simple.bat
```

**Output**:
- `ImageProcessor_Release/` folder
- `ImageProcessor.exe` (standalone executable)
- User guides and documentation

### PyInstaller Configuration

Key parameters in `build_exe.py`:

```python
cmd = [
    'pyinstaller',
    '--name=ImageProcessor',           # Executable name
    '--onefile',                        # Single file bundle
    '--windowed',                       # No console window
    '--icon=assets/icon.ico',          # Application icon
    '--add-data=assets;assets',        # Include assets folder
    '--noconsole',                     # GUI application
    'main.py'                          # Entry point
]
```

### Troubleshooting Build Issues

**Problem**: Missing assets in executable
- **Solution**: Verify `--add-data` parameter includes all asset folders

**Problem**: Executable won't start
- **Solution**: Check for missing DLL dependencies with Dependency Walker

**Problem**: Large executable size
- **Solution**: Use `--exclude-module` to remove unused libraries

---

## Testing

### Manual Testing Checklist

- [ ] Open various image formats (JPG, PNG, BMP, GIF)
- [ ] Test crop tool on different image sizes
- [ ] Verify center-point crop with boundary cases
- [ ] Test compression with various target sizes
- [ ] Switch languages and verify translations
- [ ] Test keyboard shortcuts (Ctrl+O, Ctrl+S)
- [ ] Check preview window functionality
- [ ] Save processed images and verify output

### Automated Testing

```bash
# Run core functionality tests
python test_core.py
```

**Test Coverage**:
- Image loading and saving
- Coordinate transformations
- Crop algorithms
- Compression quality

### Performance Testing

```python
import time

start = time.time()
compressed = image_processor.compress_to_size(large_image, 500, 'JPEG')
elapsed = time.time() - start
print(f"Compression took {elapsed:.2f} seconds")
```

**Performance Benchmarks**:
- 4000x3000 image crop: < 0.5 seconds
- Compression to 500KB: < 3 seconds
- Language switch: < 0.1 seconds

---

## Debugging

### Common Issues

**Issue**: "Too early to create image" error
- **Cause**: Creating PhotoImage before Tkinter root exists
- **Solution**: Create PhotoImage in `app.py`, not `image_processor.py`

**Issue**: Coordinate mismatch in crops
- **Cause**: Forgetting to apply scale/offset transformation
- **Solution**: Always use `canvas_to_image_coords()` before processing

**Issue**: Memory leak with large images
- **Cause**: Not releasing image references
- **Solution**: Use `del` on PIL images after processing

### Debug Mode

Add debug logging to `image_processor.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

def center_crop(image, width, height, center_x, center_y):
    logging.debug(f"Crop params: w={width}, h={height}, cx={center_x}, cy={center_y}")
    # ... processing ...
    logging.debug(f"Crop result: {cropped.size}")
    return cropped
```

---

## Performance Optimization

### Image Processing Optimization

1. **Use Efficient Resampling**:
   ```python
   # Fast but lower quality
   image.resize((width, height), Image.BILINEAR)

   # Slow but high quality (current)
   image.resize((width, height), Image.LANCZOS)
   ```

2. **Lazy Loading**:
   - Only load images when needed
   - Release memory after processing

3. **Caching**:
   - Cache scaled display images
   - Avoid redundant processing

### UI Responsiveness

1. **Threading for Long Operations**:
   ```python
   import threading

   def compress_in_thread():
       thread = threading.Thread(target=compress_image)
       thread.start()
   ```

2. **Progress Indicators**:
   - Show progress bar for long operations
   - Update status bar during processing

---

## Troubleshooting

### Development Issues

**Q**: Virtual environment not activating
**A**: Check path separators (Windows uses `\`, Unix uses `/`)

**Q**: Import errors after installation
**A**: Verify virtual environment is activated and dependencies installed

**Q**: GUI not displaying properly
**A**: Update Tkinter or test with different Python version

### Build Issues

**Q**: PyInstaller fails with "module not found"
**A**: Add module explicitly with `--hidden-import=module_name`

**Q**: Icon not showing in executable
**A**: Verify icon.ico is in assets folder and path is correct

### Runtime Issues

**Q**: Application crashes on large images
**A**: Implement image size limits or progressive loading

**Q**: Compression takes too long
**A**: Reduce quality search range or use faster compression algorithm

---

## Additional Resources

- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [PyInstaller Manual](https://pyinstaller.readthedocs.io/)
- [PEP 8 Style Guide](https://pep8.org/)

---

## Questions?

If you have questions not covered in this guide:
- Check the [FAQ](FAQ.md)
- Search [existing issues](https://github.com/yourusername/image-tool-pro/issues)
- Ask in [discussions](https://github.com/yourusername/image-tool-pro/discussions)

Happy coding! 🚀
