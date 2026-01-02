# YOLO Image Labeler

A simple application for creating and managing YOLO format annotations with integrated auto-detection capabilities.

## Features

- 🖼️ **Image Management**: Load and navigate through multiple images with ease
- 🎨 **Multi-Label Support**: Create and manage multiple object classes with color coding
- 🤖 **YOLO Auto-Detection**: Integrate pre-trained YOLO models for automatic annotation
- ✅ **Intuitive Class Selection**: Checkbox-based class selection with Select All/None buttons
- 📊 **Status Bar**: Real-time feedback on actions and image progress
- 🔍 **Zoom & Pan**: Full canvas zoom and scroll support with optional zoom reset
- ⌨️ **Keyboard Shortcuts**: Fast workflow with comprehensive keyboard shortcuts
- 🎯 **Smart Selection**: Right-click selection for batch deletion of annotations
- ↩️ **Undo/Redo**: Full undo/redo support for all drawing operations
- 💾 **YOLO Format**: Export annotations in standard YOLO format (normalized coordinates)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/yolo-image-labeler.git
cd yolo-image-labeler
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Basic Workflow

1. **Load Images**:
   - Click "Load Images" button
   - Select source directory (containing images)
   - Select destination directory (for saving annotations)

2. **Create Labels**:
   - Click "+ Add Label" or press `Alt+[0-9]` to create numbered labels
   - Enter label name when prompted
   - Labels are automatically color-coded

3. **Draw Annotations**:
   - Select a label from the sidebar or press `[0-9]`
   - Click and drag on the image to draw bounding boxes
   - Use zoom (`Ctrl+MouseWheel`) for precise annotations

4. **Save & Continue**:
   - Press `S` or click "Confirm and Save"
   - Annotations are saved in YOLO format
   - Automatically moves to next image

### YOLO Auto-Detection

1. **Load Model**:
   - Click "Load YOLO Model"
   - Select your `.pt` model file
   - Classes are automatically loaded and all selected by default

2. **Configure Detection**:
   - Use checkboxes to select/deselect specific classes
   - Click "Select All" or "Select None" for quick selection
   - Adjust confidence threshold slider (0-1)
   - Enable "Auto Detect on Load" for automatic detection on each image

3. **Run Detection**:
   - Press `A` or click "Run Auto Detect"
   - Detected objects are automatically annotated
   - Review and adjust as needed

### UI Improvements

- **Checkbox Class Selection**: Easy-to-use checkboxes instead of multi-select listbox
- **Color-Coded Classes**: Each class has a visual color indicator
- **Status Bar**: Bottom status bar shows current action, image count, and feedback
- **Zoom Control**: Optional "Reset Zoom on Image Change" for consistent viewing
- **Visual Feedback**: Toast-style messages for all actions (save, load, detect)

### Keyboard Shortcuts

#### Navigation
- `S` - Save and move to next image
- `Left Arrow` - Go to previous image
- `Right Arrow` - Go to next image

#### Drawing & Editing
- `Left Click + Drag` - Draw bounding box
- `Right Click` - Delete single annotation (click) or select area (drag) deleting  annotation boxes  **fully contained** within the selection area.
- `Shift + Right Click + Drag` - Delete partially selected annotations
- `Ctrl+Z` - Undo last action
- `Ctrl+Y` - Redo last undone action
- `Delete` - Delete currently selected label
- `C` - Clear all rectangles

#### Labels
- `0-9` - Select label by number
- `Alt+0-9` - Create new label with number

#### YOLO Detection
- `A` - Run auto-detection

#### View
- `Ctrl+MouseWheel` - Zoom in/out
- `MouseWheel` - Scroll vertically
- `Alt+MouseWheel` - Scroll horizontally

## File Format

### Input
- Supported image formats: `.png`, `.jpg`, `.jpeg`
- Optional: Existing YOLO annotations (`.txt` files)

### Output
YOLO format annotations (`.txt` files):
```
<class_id> <x_center> <y_center> <width> <height>
```
All coordinates are normalized (0-1 range).

Example:
```
0 0.5 0.5 0.3 0.4
1 0.25 0.75 0.15 0.2
```

## Advanced Features

### Zoom & Pan
- Use `Ctrl+MouseWheel` to zoom in/out
- All annotations automatically scale with zoom
- Pan using scrollbars or mouse wheel
- Coordinates are preserved in original image space

### Batch Annotation Management
- Right-click drag to select multiple annotations
- Delete all selected annotations at once
- Shift+Right-click for partial overlap selection

### Label Management
- Create unlimited labels
- Delete labels with confirmation
- Labels automatically assigned to YOLO classes
- Color-coded for easy identification

### Auto-Detection Features
- Filter by class selection
- Adjustable confidence threshold
- Auto-detect on image load option
- Merge manual and auto annotations

## Common Issues

**Q: Images or annotations not loading correctly?**
- When you click **"Load Images"**, first select your **image folder**, then select your **annotation folder** (where `.txt` files are).
- **Note:** It is normal for files to not appear in the selected folder. Just select the correct folder and proceed.

- **Note:** After saving the last image, the session ends. To go back and review your work, you must click **"Load Images"** again to restart the process from the beginning.

> **Note on Deletion:**
> - **Right Click + Drag** will only delete annotation boxes that are **fully contained** within the selection area.
> - **Shift + Right Click + Drag** will delete any annotation box that is **even partially touched** by the selection area.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Tkinter](https://docs.python.org/3/library/tkinter.html)
- YOLO detection powered by [Ultralytics](https://github.com/ultralytics/ultralytics)
- Image processing with [Pillow](https://python-pillow.org/)

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
