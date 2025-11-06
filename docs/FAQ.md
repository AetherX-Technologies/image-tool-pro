# Frequently Asked Questions (FAQ)

Common questions and answers about Image Tool Pro.

## Table of Contents

- [General Questions](#general-questions)
- [Installation & Setup](#installation--setup)
- [Features & Usage](#features--usage)
- [Troubleshooting](#troubleshooting)
- [Technical Questions](#technical-questions)
- [Contributing & Development](#contributing--development)

---

## General Questions

### What is Image Tool Pro?

Image Tool Pro is a desktop application for Windows that provides powerful image processing features including interactive cropping, center-point cutting, and smart compression. It's designed for photographers, designers, and anyone who needs to quickly process images.

### Is it free?

Yes, Image Tool Pro is completely free and open-source under the MIT License. You can use it for personal or commercial purposes without any restrictions.

### Do I need to install Python?

No! The standalone executable (`.exe` file) includes everything you need. Just download and run it. However, if you want to run from source code or contribute to development, you'll need Python 3.7+.

### Does it work offline?

Yes, absolutely. Image Tool Pro processes all images locally on your computer with no internet connection required. Your images never leave your machine.

### What platforms are supported?

Currently, only Windows (7, 8, 10, 11) is officially supported. The source code may work on macOS and Linux with Python installed, but executables are only built for Windows.

---

## Installation & Setup

### How do I install Image Tool Pro?

There's no installation required:
1. Download the ZIP file from [GitHub Releases](https://github.com/yourusername/image-tool-pro/releases)
2. Extract it to any folder
3. Double-click `ImageProcessor.exe`

### Why does Windows show a security warning?

This is normal for applications not signed with an expensive code-signing certificate. The application is safe and open-source. Click "More info" → "Run anyway" to proceed.

### Why is my antivirus flagging the executable?

Some antivirus software flags PyInstaller executables as potentially suspicious (false positive). This is a known issue with PyInstaller. The source code is available for audit, or you can build the executable yourself from source.

### Can I run it from a USB drive?

Yes! Image Tool Pro is fully portable. Copy the folder to a USB drive and run it from there. Your language preferences will be saved in the same folder.

### How much disk space does it need?

- Executable: ~11 MB
- Runtime memory: 50-200 MB depending on image size
- Recommended free disk space: 100 MB for processed images

---

## Features & Usage

### What image formats are supported?

**Input formats**: JPG, JPEG, PNG, BMP, GIF
**Output formats**: JPEG, PNG (selectable during save/compression)

### What's the maximum image size?

There's no hard limit, but practical limits are:
- **Recommended**: Up to 8000×6000 pixels (48 megapixels)
- **Maximum**: Limited by available RAM (~200 MB per large image)
- Very large images (20+ megapixels) may take longer to process

### How does interactive cropping work?

1. Load an image
2. Left-click and drag on the canvas to create a crop box
3. Drag the red corner handles to adjust the crop area
4. Drag inside the box to move it
5. View real-time pixel dimensions in the Pixel Info panel
6. Click "Execute Crop" to apply

### What's center-point cutting?

Center-point cutting crops an image from a specific center point:
1. Right-click on the image to set a center point (blue crosshair appears)
2. Enter desired width and height in pixels
3. Click "Execute Cut"
4. If the crop extends beyond image boundaries, only the valid intersection is cropped

### How does smart compression work?

Smart compression uses binary search to find the optimal quality setting:
1. Enter target file size (e.g., "500" and select "KB")
2. Choose output format (JPEG or PNG)
3. Click "Start Compress"
4. The algorithm tries different quality levels to match your target size
5. If needed, it will reduce resolution to reach the target

### Can I undo operations?

Currently, no. There's no undo/redo functionality in v1.0. This feature is planned for v1.1. Workaround: Keep your original images and reload if needed.

### How do I switch languages?

Menu bar → **Language** → Select **English** or **中文 (Chinese)**

The interface will restart with the new language. Your preference is saved automatically.

---

## Troubleshooting

### The application won't start

**Solutions**:
1. Verify you're running Windows 7 or newer (64-bit)
2. Check if antivirus is blocking it (add exception)
3. Run as administrator (right-click → "Run as administrator")
4. Re-download in case of corrupted download
5. Check Event Viewer for error details

### Images look blurry after processing

**Possible causes**:
1. **Compression quality**: Lower quality settings reduce file size but decrease image quality
2. **Resolution reduction**: If target file size is too small, resolution is automatically reduced
3. **Display scaling**: Check if you're viewing at 100% zoom

**Solutions**:
- Use higher target file sizes for compression
- Save as PNG for lossless quality
- Don't compress if quality is critical

### Cropping is not precise

**Tips**:
- Zoom your OS display scaling to 100% for pixel-perfect precision
- Use the Pixel Info panel to see exact dimensions
- Use center-point cutting for exact pixel dimensions
- Drag corner handles slowly for fine adjustments

### Center point cutting gives unexpected results

**Common issues**:
- **Boundary handling**: If your crop extends beyond the image, only the valid intersection is returned
- **Coordinate system**: Center point is relative to the original image, not the displayed canvas

**Example**: If image is 2000×1000 and you request 3000×3000 from center, you'll get a 2000×1000 crop (the entire image).

### Compression doesn't reach target size

**Reasons**:
1. **PNG format**: PNG is lossless and may not compress as much as JPEG
2. **Complex images**: High-detail images are harder to compress
3. **Already small**: If image is already smaller than target, it won't be enlarged

**Solutions**:
- Switch to JPEG format
- Reduce target dimensions first (crop before compressing)
- Set a lower target size to force more aggressive compression

### Application crashes with large images

**Causes**:
- Insufficient RAM (4GB+ recommended for large images)
- Image dimensions exceed practical limits

**Solutions**:
- Pre-resize very large images in another tool
- Close other applications to free up memory
- Process smaller image batches

### "Failed to load image" error

**Possible causes**:
1. File is corrupted or not a valid image
2. Unsupported format (e.g., TIFF, WEBP)
3. File path contains special characters
4. File is locked by another program

**Solutions**:
- Verify file opens in other image viewers
- Convert to JPG or PNG first
- Move file to a simpler path (e.g., `C:\temp\image.jpg`)
- Close other programs using the file

---

## Technical Questions

### What libraries does it use?

- **Pillow 9.5.0**: Image processing (crop, resize, compress)
- **Tkinter**: GUI framework (included with Python)
- **PyInstaller 5.13.2**: Executable packaging (build-time only)

### How is compression optimized?

The compression algorithm uses **binary search** to find the optimal JPEG/PNG quality setting:
1. Try quality = 50 (midpoint of 1-95 range)
2. Check resulting file size
3. If too large, search lower range; if too small, search higher range
4. Repeat until target size is matched (±5%)
5. If minimum quality still too large, reduce resolution by 10% and retry

Time complexity: O(log n) where n = quality range

### What coordinate system is used?

There are two coordinate systems:
1. **Canvas coordinates**: Scaled display coordinates in the Tkinter canvas
2. **Image coordinates**: Original image pixel coordinates

Conversion formulas:
```python
# Canvas to image
img_x = (canvas_x - offset_x) / scale
img_y = (canvas_y - offset_y) / scale

# Image to canvas
canvas_x = img_x * scale + offset_x
canvas_y = img_y * scale + offset_y
```

Where `scale` is the zoom ratio and `offset` is the canvas centering offset.

### How is boundary intersection calculated?

For center-point crops extending beyond image edges:

```python
left = max(0, center_x - width // 2)
right = min(img_width, center_x + width // 2)
top = max(0, center_y - height // 2)
bottom = min(img_height, center_y + height // 2)

cropped = image.crop((left, top, right, bottom))
```

This ensures the crop box is always valid and within image bounds.

### Does it preserve EXIF metadata?

By default, Pillow preserves basic EXIF metadata when saving images. However, some metadata may be lost during heavy processing (rotation, cropping). If metadata preservation is critical, use specialized tools.

### What's the architecture pattern?

Image Tool Pro follows **MVC (Model-View-Controller)**:
- **Model**: `image_processor.py` (business logic)
- **View**: `app.py` (UI presentation)
- **Controller**: `ui_components.py` + `crop_tool.py` (user interactions)

See [DEVELOPMENT.md](DEVELOPMENT.md) for details.

---

## Contributing & Development

### How can I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines. Quick ways to contribute:
- Report bugs or suggest features via GitHub Issues
- Add translations for new languages
- Improve documentation
- Submit code via pull requests

### How do I run from source?

```bash
git clone https://github.com/yourusername/image-tool-pro.git
cd image-tool-pro
pip install -r requirements.txt
python main.py
```

### How do I build the executable myself?

```bash
pip install pyinstaller
python build_exe.py
```

The executable will be in `ImageProcessor_Release/ImageProcessor.exe`.

### Can I use this in my own project?

Yes! Image Tool Pro is MIT licensed. You can:
- Use it in commercial projects
- Modify the code
- Redistribute it
- Include it in other software

Just keep the original copyright notice. See [LICENSE](../LICENSE) for details.

### Will there be a macOS/Linux version?

It's on the roadmap! The source code should work on macOS/Linux with Python, but we haven't built executables yet. Contributions welcome!

---

## Still Have Questions?

- **Check**: [User Guide](USER_GUIDE.md) for detailed usage instructions
- **Search**: [GitHub Issues](https://github.com/yourusername/image-tool-pro/issues) for similar questions
- **Ask**: [GitHub Discussions](https://github.com/yourusername/image-tool-pro/discussions) for community help
- **Report**: [Bug Report](https://github.com/yourusername/image-tool-pro/issues/new?template=bug_report.md) if you found a bug

---

**Last updated**: 2025-11-06 (v1.0.0)
