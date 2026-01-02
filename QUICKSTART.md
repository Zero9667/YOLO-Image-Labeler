# Quick Start Guide

This guide will help you get started with YOLO Image Labeler.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/yolo-image-labeler.git
cd yolo-image-labeler

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## First Annotation Session

### Step 1: Prepare Your Data
- Create a folder with your images (`.jpg`, `.png`, `.jpeg`)
- Create a destination folder for annotations

### Step 2: Load Images
1. Click **"Load Images"** button
2. Select your source folder (with images)
3. Select your destination folder (for annotations)

### Step 3: Create Labels
1. Click **"+ Add Label"** or press `Alt+0`
2. Enter a name (e.g., "person", "car", "dog")
3. Repeat for all object classes you want to label

### Step 4: Draw Annotations
1. Select a label from the sidebar (or press `0-9`)
2. Click and drag on the image to draw a box around objects
3. Repeat for all objects in the image

### Step 5: Save and Continue
- Press `S` or click **"Confirm and Save"**
- The app automatically moves to the next image
- Repeat steps 4-5 for all images

## Using YOLO Auto-Detection (Optional)

### Step 1: Load Model
1. Click **"Load YOLO Model"**
2. Select your `.pt` model file (e.g., `yolov8n.pt`)

### Step 2: Configure
1. Select desired classes from the list
2. Adjust confidence threshold slider (default: 0.5)
3. Check **"Auto Detect on Load"** for automatic detection

### Step 3: Run Detection
- Press `A` or click **"Auto Detect"**
- Review and adjust detected boxes as needed

## Essential Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `S` | Save and next image |
| `Left Arrow` | Previous image |
| `Right Arrow` | Next image |
| `A` | Auto detect |
| `C` | Clear all boxes |
| `0-9` | Select label |
| `Alt+0-9` | Create new label |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Right Click` | Delete box |
| `Ctrl+Wheel` | Zoom |

## Output Format

Annotations are saved as `.txt` files in YOLO format:
```
<class_id> <x_center> <y_center> <width> <height>
```

Example:
```
0 0.716797 0.395833 0.216406 0.147222
1 0.323438 0.791667 0.446875 0.208333
```

All coordinates are normalized (0-1 range) relative to image dimensions.

## Tips for Efficient Labeling

1. **Use keyboard shortcuts** - Much faster than clicking buttons
2. **Zoom in** (Ctrl+Wheel) for precise annotations
3. **Enable auto-detect** for initial annotations, then correct manually
4. **Right-click drag** to select and delete multiple boxes at once
5. **Use undo/redo** freely - experiment without fear

## Common Issues

**Q: Images or annotations not loading correctly?**
- When you click **"Load Images"**, first select your **image folder**, then select your **annotation folder** (where `.txt` files are).
- **Note:** It is normal for files to not appear in the selected folder. Just select the correct folder and proceed.

- **Note:** After saving the last image, the session ends. To go back and review your work, you must click **"Load Images"** again to restart the process from the beginning.

> **Note on Deletion:**
> - **Right Click + Drag** will only delete annotation boxes that are **fully contained** within the selection area.
> - **Shift + Right Click + Drag** will delete any annotation box that is **even partially touched** by the selection area.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore advanced features like batch deletion and label management

## Getting Help

- Open an issue on GitHub
- Check existing issues for solutions
- Contribute improvements via pull requests

Happy labeling! 🏷️
