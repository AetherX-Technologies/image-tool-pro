# Image Tool Pro

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Release](https://img.shields.io/badge/version-1.0.0-blue.svg)

**A powerful desktop image processing tool with interactive cropping, smart compression, and multi-language support**

[English](README.md) | [简体中文](README-zh.md)

[Download](https://github.com/yourusername/image-tool-pro/releases) | [Documentation](docs/USER_GUIDE.md) | [Report Bug](https://github.com/yourusername/image-tool-pro/issues)

</div>

---

## 📖 Overview

**Image Tool Pro** is a user-friendly desktop application designed for **quick and efficient image processing**. Whether you're a photographer needing to **crop photos**, a designer optimizing **images for web**, or a content creator preparing social media assets, this tool streamlines your workflow.

Built with Python and Tkinter, packaged as a **portable Windows executable** - no Python installation required!

### Why Image Tool Pro?

- 🎯 **Pixel-Perfect Control** - Precise cropping with real-time dimension display
- 🗜️ **Smart Compression** - Compress images to exact file sizes while maintaining quality
- 🌍 **Multi-Language** - Available in English and Chinese
- 💼 **Professional Yet Simple** - Powerful features in an intuitive interface
- 📦 **Zero Installation** - Standalone executable, works out of the box

---

## ✨ Features

### 🎨 Interactive Image Cropping

Intuitive drag-and-drop interface for effortless image cropping:

- Draw crop areas with mouse drag
- Adjust crop boundaries with corner handles
- Real-time pixel dimension display
- Move entire crop area by dragging
- Visual feedback with red crop box and control points

### 🎯 Center-Point Cutting

Precision cropping based on custom center points:

- Right-click to set custom center point (blue crosshair marker)
- Input precise width and height in pixels
- Automatic boundary handling for out-of-bounds crops
- Default to image center if not specified
- Perfect for creating thumbnails and profile pictures

### 🗜️ Smart Image Compression

Compress images to exact file sizes with intelligent optimization:

- Target specific file sizes (KB or MB)
- Support for JPEG and PNG formats
- Binary search algorithm for optimal quality
- Automatic resolution scaling when needed
- Maintains visual quality while reducing file size

### 🌍 Multi-Language Support

Seamless language switching:

- English and Chinese (Simplified) interfaces
- Easy language switching via menu
- Persistent language preferences
- Localized help documentation

### 🖥️ Desktop-Friendly

Native Windows application experience:

- Keyboard shortcuts (Ctrl+O, Ctrl+S)
- Intuitive menu system
- Status bar with real-time feedback
- Professional window design with custom icon
- Responsive UI for smooth interactions

### 📦 Ready to Use

No hassle, no configuration:

- Portable executable (~11MB)
- No Python environment required
- No installation needed
- Run from any location (USB drive, desktop, etc.)
- All dependencies included

---

## 🖼️ Screenshots

### Main Interface
![image-20251106201204500](assets/screenshots/main-interface.png)

### Interactive Cropping in Action
![image-20251106201319105](assets/screenshots/crop-demo.png)

### Center-Point Cutting Feature
![image-20251106201554946](assets/screenshots/center-cut1.png)

![image-20251106201711965](assets/screenshots/center-cut2.png)

### Smart Compression Results
![Compression](assets/screenshots/compression.png)

### Multi-Language Interface
![Language Support](assets/screenshots/language.png)

### Preview Comparison
![Preview Comparison](assets/screenshots/preview.png)

---

## 📥 Download

### Latest Release: v1.0.0

**[⬇️ Download Image Tool Pro for Windows](https://github.com/yourusername/image-tool-pro/releases/latest)**

**System Requirements:**
- Windows 7 or later (64-bit)
- 512 MB RAM minimum (1 GB recommended)
- 50 MB free disk space
- 1024x768 display resolution minimum

### Installation

No installation required! Simply:

1. Download the ZIP file from [Releases](https://github.com/yourusername/image-tool-pro/releases)
2. Extract to your desired location
3. Run `ImageProcessor.exe`
4. Start processing images!

---

## 🚀 Quick Start

### For End Users

1. **Open an Image**
   - Click `File → Open Image` (or press `Ctrl+O`)
   - Select a JPG, PNG, BMP, or GIF file

2. **Process Your Image**
   - **Crop**: Left-click and drag to create a crop box
   - **Center Cut**: Right-click to set center, enter dimensions, click "Execute Crop"
   - **Compress**: Enter target size, choose format, click "Start Compression"

3. **Save Your Work**
   - Click `Save Image` button (or press `Ctrl+S`)
   - Choose save location and filename

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open Image |
| `Ctrl+S` | Save Image |
| `Left-Drag` | Create/Adjust Crop Box |
| `Right-Click` | Set Center Point |

---

## 🛠️ Tech Stack

- **Language**: Python 3.7+
- **GUI Framework**: Tkinter (built-in)
- **Image Processing**: Pillow 9.5.0
- **Packaging**: PyInstaller 5.13.2
- **Architecture**: MVC pattern with modular design

### Key Dependencies

```
pillow>=10.0.0    # Image processing library
```

That's it! Tkinter is included with Python, so minimal dependencies.

---

## 💻 Development

### For Developers

Want to contribute or build from source? Here's how:

#### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git

#### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/image-tool-pro.git
cd image-tool-pro

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

#### Building the Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build using the provided script
python build_exe.py

# Or use the batch file (Windows)
build_simple.bat

# Executable will be in dist/ImageProcessor.exe
```

#### Project Structure

```
image-tool-pro/
├── main.py                # Application entry point
├── src/
│   ├── app.py            # Main application window
│   ├── image_processor.py # Image processing logic
│   ├── crop_tool.py      # Interactive cropping tool
│   ├── ui_components.py  # UI component widgets
│   └── language.py       # Multi-language support
├── assets/
│   ├── icon.ico          # Application icon
│   └── screenshots/      # Screenshots for README
├── requirements.txt      # Python dependencies
└── build_exe.py         # PyInstaller build script
```

### Running Tests

```bash
# Run core functionality tests
python test_core.py
```

---

## 🤝 Contributing

Contributions are welcome! Whether it's bug reports, feature requests, or code contributions, we appreciate your help.

Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

### Ways to Contribute

- 🐛 Report bugs via [Issues](https://github.com/yourusername/image-tool-pro/issues)
- 💡 Suggest features or improvements
- 📖 Improve documentation
- 🌍 Add translations for new languages
- 💻 Submit pull requests

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
Copyright (c) 2025 Image Tool Pro Contributors

Permission is hereby granted, free of charge, to use, modify, and distribute
this software for any purpose, including commercial applications.
```

---

## 🙏 Acknowledgments

- **[Pillow Team](https://python-pillow.org/)** - Excellent imaging library
- **[PyInstaller Team](https://pyinstaller.org/)** - Standalone executable packaging
- **Python Community** - Amazing ecosystem and support
- **All Contributors** - Thank you for making this project better!

---

## 📞 Support

### Getting Help

- 📚 Read the [User Guide](docs/USER_GUIDE.md)
- ❓ Check the [FAQ](docs/FAQ.md)
- 🐛 Report issues on [GitHub Issues](https://github.com/yourusername/image-tool-pro/issues)

### Stay Updated

- ⭐ Star this repository to show your support
- 👀 Watch for updates and new releases
- 🔔 Enable notifications for important announcements

---

## 🗺️ Roadmap

### Version 1.1 (Coming Soon)
- [ ] Batch processing support
- [ ] Undo/Redo functionality
- [ ] Processing history
- [ ] More keyboard shortcuts

### Version 1.2 (Planned)
- [ ] Image rotation and flip tools
- [ ] Basic filters (blur, sharpen, brightness)
- [ ] More output formats (WEBP, TIFF)
- [ ] Command-line interface

### Version 2.0 (Future)
- [ ] Advanced filters and effects
- [ ] Watermarking capabilities
- [ ] Batch automation scripts
- [ ] macOS and Linux support

---

## 📊 Project Stats

- **Lines of Code**: ~1,600
- **Languages Supported**: 2 (English, Chinese)
- **Translation Strings**: 80+
- **Build Size**: ~11 MB
- **Supported Image Formats**: JPG, PNG, BMP, GIF

---

<div align="center">

**Made with ❤️ by the Image Tool Pro Team**

[⬆ Back to Top](#image-tool-pro)

</div>
