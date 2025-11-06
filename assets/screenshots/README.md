# Screenshots Directory

This directory contains screenshots for the project README and documentation.

## Required Screenshots

To complete the README documentation, please add the following screenshots:

### 1. main-interface.png
**Description**: Main application window showing the canvas area and control panels

**What to capture**:
- Full application window
- Canvas area with an image loaded
- All control panels visible (Pixel Info, Center Crop, Compress, Actions)
- Menu bar at the top
- Status bar at the bottom

**Recommended size**: 1200x800 pixels or similar

---

### 2. crop-demo.gif
**Description**: Animated GIF showing the drag-and-drop cropping process

**What to capture**:
- Mouse cursor visible
- Creating a new crop box by dragging
- Showing the red crop box with corner handles
- Moving the crop box
- Resizing from different corners
- Real-time pixel dimension updates

**Recommended**:
- Duration: 5-10 seconds
- Format: Animated GIF
- Size: 800x600 pixels or similar
- Tool suggestion: ScreenToGif, LICEcap, or similar

---

### 3. center-cut.png
**Description**: Center-point cutting feature with blue crosshair marker

**What to capture**:
- Image with blue crosshair center point visible
- Center Crop Panel with width/height inputs filled
- Showing the intersection of horizontal and vertical blue lines

**Recommended size**: 1000x700 pixels or similar

---

### 4. compression.png
**Description**: Smart compression settings and results

**What to capture**:
- Compress Panel with target size input
- Format selection (JPEG/PNG)
- Before and after file sizes displayed
- Image quality comparison (if possible)

**Recommended size**: 1000x700 pixels or similar

---

### 5. language.png
**Description**: Multi-language interface comparison

**What to capture**:
- Two screenshots side-by-side showing:
  - Left: Application in English
  - Right: Application in Chinese (Simplified)
- Same screen/feature in both languages
- Language menu dropdown visible (optional)

**Recommended size**: 1600x800 pixels (combined) or two separate 800x800 images

---

### 6. preview.png
**Description**: Preview window showing original vs processed image comparison

**What to capture**:
- Preview comparison window
- Original and processed images side-by-side
- Dimension information displayed
- Clear visual comparison

**Recommended size**: 1200x600 pixels or similar

---

## Screenshot Guidelines

### Quality Standards
- **Resolution**: High-DPI preferred (1080p or higher)
- **Format**: PNG for static images, GIF for animations
- **Clarity**: Clear, well-lit, readable text
- **Content**: Professional, no personal information visible

### File Naming
Use exactly these filenames:
- `main-interface.png`
- `crop-demo.gif`
- `center-cut.png`
- `compression.png`
- `language.png`
- `preview.png`

### Tools Recommended

**Screenshot Tools**:
- Windows: Snipping Tool, Snip & Sketch, ShareX
- Cross-platform: Flameshot, Greenshot

**GIF Recording Tools**:
- ScreenToGif (Windows, free)
- LICEcap (Windows/macOS, free)
- Kap (macOS, free)

**Image Editing** (optional):
- GIMP (free, all platforms)
- Paint.NET (Windows, free)
- Photoshop (paid)

### Image Optimization

After creating screenshots, optimize them:

```bash
# Install optimization tools (optional)
pip install pillow

# Optimize PNG images
python -c "from PIL import Image; img=Image.open('image.png'); img.save('image.png', optimize=True)"

# Or use online tools
# - TinyPNG: https://tinypng.com/
# - Squoosh: https://squoosh.app/
```

---

## Adding Screenshots to README

Once you've added all screenshots to this directory, they will automatically appear in:
- `README.md` (English)
- `README-zh.md` (Chinese)

The markdown files already reference these images with:
```markdown
![Main Interface](assets/screenshots/main-interface.png)
```

---

## Checklist

Before committing:
- [ ] All 6 screenshots added
- [ ] Filenames match exactly (case-sensitive on some systems)
- [ ] Images are clear and professional quality
- [ ] No personal information visible in screenshots
- [ ] File sizes are reasonable (< 2MB per image)
- [ ] GIF animation is smooth and demonstrates the feature well
- [ ] Preview README.md locally to verify images display correctly

---

## Questions?

If you need help creating screenshots:
- Check the [CONTRIBUTING.md](../../CONTRIBUTING.md) guide
- Open a discussion on GitHub
- Refer to the application's USER_GUIDE.txt for feature details

---

**Thank you for helping make the documentation complete!**
