# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v1.1
- Batch processing support for multiple images
- Undo/Redo functionality
- Processing history tracking
- Additional keyboard shortcuts
- Performance optimizations for large images

### Planned for v1.2
- Image rotation and flip tools
- Basic filters (blur, sharpen, brightness adjustment)
- Contrast and saturation controls
- Support for additional formats (WEBP, TIFF)
- Command-line interface (CLI) mode

## [1.0.0] - 2025-11-06

### Added
- **Interactive Image Cropping**
  - Drag-and-drop interface to create crop boxes
  - Adjustable corner handles for precise sizing
  - Real-time pixel dimension display
  - Move crop box by dragging inside the selection area
  - Visual feedback with red crop box and control points

- **Center-Point Cropping**
  - Right-click to set custom center point with blue crosshair marker
  - Input precise width and height in pixels
  - Automatic boundary handling for crops extending beyond image edges
  - Default to image center if not specified
  - Smart intersection calculation for out-of-bounds crops

- **Smart Image Compression**
  - Target specific file sizes (KB or MB units)
  - Support for JPEG and PNG output formats
  - Binary search algorithm for optimal quality settings
  - Automatic resolution scaling when needed to reach target size
  - Quality preservation while reducing file size

- **Preview & Comparison**
  - Side-by-side view of original and processed images
  - Dimension information display
  - Visual quality comparison before saving

- **Multi-Language Support**
  - English interface (default)
  - Chinese (Simplified) interface
  - Easy language switching via menu
  - Persistent language preferences saved to configuration file
  - 80+ localized translation strings

- **Desktop Application Features**
  - Native Windows application with Tkinter GUI
  - Custom application icon (gradient design with crop elements)
  - Keyboard shortcuts (Ctrl+O for Open, Ctrl+S for Save)
  - Intuitive menu system (File, Edit, Language, Help)
  - Status bar with real-time feedback
  - Professional window design

- **Standalone Executable**
  - Portable EXE file (~11 MB)
  - No Python installation required
  - No external dependencies to install
  - Run from any location (USB drive, desktop, etc.)
  - All dependencies bundled with PyInstaller

- **Documentation**
  - Comprehensive user guides (English and Chinese)
  - Quick start guide
  - Release notes
  - Technical documentation
  - Build instructions for developers

### Technical Details
- Python 3.7.6 runtime
- Tkinter for GUI framework
- Pillow 9.5.0 for image processing
- PyInstaller 5.13.2 for executable packaging
- MVC architecture pattern
- LANCZOS resampling for high-quality scaling
- Modular code structure with separate components

### Supported Formats
- **Input**: JPG, JPEG, PNG, BMP, GIF
- **Output**: JPEG, PNG (user selectable)

### System Requirements
- Windows 7 (64-bit) or newer
- 512 MB RAM minimum (1 GB recommended)
- 50 MB free disk space
- 1024x768 display resolution minimum

### Known Limitations
- Language changes require application restart
- Compression target size is approximate (±5-10%)
- Large images (>8000x6000) may take several seconds to load
- No batch processing in this version
- No undo/redo functionality yet

### Security & Privacy
- All processing done locally
- No internet connection required
- No data collection or telemetry
- No external server communication
- Images never leave your computer

---

## Version History Summary

- **v1.0.0** (2025-11-06) - Initial public release with core features
- **Future versions** - See [Roadmap](README.md#-roadmap) in README

---

[Unreleased]: https://github.com/yourusername/image-tool-pro/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/image-tool-pro/releases/tag/v1.0.0
