#!/usr/bin/env python3
"""
YOLO Image Labeler - Main Entry Point
A simple annotation tool for creating YOLO format labels with integrated with integrated auto-detection capabilities
"""

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
from PIL import Image, ImageTk
import os

try:
    from ultralytics import YOLO
except ImportError:
    print("Warning: ultralytics not found. YOLO auto-detection will not be available.")
    YOLO = None


class ImageDrawer(tk.Tk):
    """Main application class for YOLO Image Labeler."""
    
    def __init__(self):
        super().__init__()
        self.title("Advanced Image Drawer with YOLO")
        self.geometry("1200x850")

        # Store original image dimensions
        self.original_width = 0
        self.original_height = 0
        
        # YOLO initialization variables
        self.model = None
        self.class_names = []
        self.selected_classes = set()
        self.class_checkboxes = {}  # Store checkbox variables
        
        # YOLO control frame
        self.yolo_control_frame = tk.Frame(self, bg="lightgray", width=280)
        self.yolo_control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.yolo_control_frame.pack_propagate(False)
        
        # YOLO section label
        yolo_title = tk.Label(
            self.yolo_control_frame, 
            text="YOLO Detection", 
            font=("Arial", 12, "bold"),
            bg="lightgray"
        )
        yolo_title.pack(pady=(10, 5))
        
        # Load YOLO model button
        self.load_model_btn = tk.Button(
            self.yolo_control_frame, 
            text="Load YOLO Model", 
            command=self.load_yolo_model,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        self.load_model_btn.pack(pady=5, padx=10, fill=tk.X)

        # Classes section
        classes_label = tk.Label(
            self.yolo_control_frame, 
            text="Detection Classes:", 
            font=("Arial", 10, "bold"),
            bg="lightgray"
        )
        classes_label.pack(pady=(15, 5))

        # Select All/None buttons frame
        select_buttons_frame = tk.Frame(self.yolo_control_frame, bg="lightgray")
        select_buttons_frame.pack(pady=5, fill=tk.X, padx=10)
        
        self.select_all_btn = tk.Button(
            select_buttons_frame,
            text="Select All",
            command=self.select_all_classes,
            state=tk.DISABLED
        )
        self.select_all_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        self.select_none_btn = tk.Button(
            select_buttons_frame,
            text="Select None",
            command=self.select_no_classes,
            state=tk.DISABLED
        )
        self.select_none_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Scrollable frame for class checkboxes
        self.class_canvas_frame = tk.Frame(self.yolo_control_frame, bg="white", relief=tk.SUNKEN, borderwidth=1)
        self.class_canvas_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        self.class_canvas = tk.Canvas(self.class_canvas_frame, bg="white", highlightthickness=0)
        self.class_scrollbar = tk.Scrollbar(self.class_canvas_frame, orient=tk.VERTICAL, command=self.class_canvas.yview)
        self.class_inner_frame = tk.Frame(self.class_canvas, bg="white")
        
        self.class_inner_frame.bind(
            "<Configure>",
            lambda e: self.class_canvas.configure(scrollregion=self.class_canvas.bbox("all"))
        )
        
        self.class_canvas.create_window((0, 0), window=self.class_inner_frame, anchor="nw")
        self.class_canvas.configure(yscrollcommand=self.class_scrollbar.set)
        
        self.class_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.class_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind mousewheel to canvas
        self.class_canvas.bind_all("<MouseWheel>", self._on_class_mousewheel)
        
        # Confidence threshold setting
        self.conf_threshold = 0.5

        conf_frame = tk.Frame(self.yolo_control_frame, bg="lightgray")
        conf_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.conf_label = tk.Label(
            conf_frame, 
            text="Confidence: 0.50", 
            font=("Arial", 9),
            bg="lightgray"
        )
        self.conf_label.pack()

        self.conf_slider = tk.Scale(
            conf_frame,
            from_=0, 
            to=1, 
            resolution=0.05,
            orient=tk.HORIZONTAL,
            command=self.update_confidence_label,
            showvalue=False
        )
        self.conf_slider.set(0.5)
        self.conf_slider.pack(fill=tk.X)

        # Auto detect button
        self.auto_detect_btn = tk.Button(
            self.yolo_control_frame, 
            text="Run Auto Detect (A)", 
            command=self.run_yolo_detection,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            state=tk.DISABLED
        )
        self.auto_detect_btn.pack(pady=10, padx=10, fill=tk.X)
        
        # Auto detect on load checkbox
        self.auto_detect_var = tk.BooleanVar()
        self.auto_detect_toggle = tk.Checkbutton(
            self.yolo_control_frame, 
            text="Auto Detect on Load", 
            variable=self.auto_detect_var,
            bg="lightgray"
        )
        self.auto_detect_toggle.pack(pady=5)
        
        # Reset zoom checkbox
        self.reset_zoom_var = tk.BooleanVar(value=True)
        self.reset_zoom_toggle = tk.Checkbutton(
            self.yolo_control_frame,
            text="Reset Zoom on Image Change",
            variable=self.reset_zoom_var,
            bg="lightgray"
        )
        self.reset_zoom_toggle.pack(pady=5)
        
        # Image list section
        images_label = tk.Label(
            self.yolo_control_frame, 
            text="Images:", 
            font=("Arial", 10, "bold"),
            bg="lightgray"
        )
        images_label.pack(pady=(15, 5))
        
        self.image_list_frame = tk.Frame(self.yolo_control_frame)
        self.image_list_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10), padx=10)
        
        self.image_vsb = tk.Scrollbar(self.image_list_frame, orient=tk.VERTICAL)
        self.image_hsb = tk.Scrollbar(self.image_list_frame, orient=tk.HORIZONTAL)
        self.image_listbox = tk.Listbox(
            self.image_list_frame,
            selectmode=tk.SINGLE,
            yscrollcommand=self.image_vsb.set,
            xscrollcommand=self.image_hsb.set
        )
        self.image_vsb.config(command=self.image_listbox.yview)
        self.image_hsb.config(command=self.image_listbox.xview)
        self.image_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.image_hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.image_listbox.bind("<<ListboxSelect>>", self.on_image_select)
        
        # Label colors and initialization
        self.label_colors = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta"]
        self.current_label_id = 0
        self.current_color = self.label_colors[0]
        self.labels = [{"id": 0, "name": "Label", "color": "red"}]
        
        # Main frames setup
        self.sidebar = tk.Frame(self, width=220, bg="lightgray")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Canvas and scrollbars
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.v_scroll = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scroll = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # Grid layout for canvas
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        # Status bar at the bottom
        self.status_bar = tk.Label(
            self.main_frame,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Scroll and zoom bindings
        self.canvas.bind("<MouseWheel>", self.scroll_vertical)
        self.canvas.bind("<Alt-MouseWheel>", self.scroll_horizontal)
        self.canvas.bind("<Control-MouseWheel>", self.zoom)

        # Zoom level variable
        self.zoom_level = 1.0
        
        # Label management section
        labels_title = tk.Label(
            self.sidebar,
            text="Labels",
            font=("Arial", 12, "bold"),
            bg="lightgray"
        )
        labels_title.pack(pady=(10, 5))
        
        self.label_management = tk.Frame(self.sidebar, bg="lightgray")
        self.label_management.pack(pady=5)
        
        self.add_label_btn = tk.Button(
            self.label_management, 
            text="+ Add Label", 
            command=self.add_label,
            cursor="hand2"
        )
        self.add_label_btn.pack(pady=5)
        
        self.labels_frame = tk.Frame(self.sidebar, bg="lightgray")
        self.labels_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        self.create_label_widget(0)        
                      
        # Control buttons
        controls_title = tk.Label(
            self.sidebar,
            text="Controls",
            font=("Arial", 12, "bold"),
            bg="lightgray"
        )
        controls_title.pack(pady=(10, 5))
        
        self.button_frame = tk.Frame(self.sidebar, bg="lightgray")
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.buttons_container = tk.Frame(self.button_frame, bg="lightgray")
        self.buttons_container.pack(fill=tk.X, padx=10)
        
        # Control buttons
        self.load_button = tk.Button(
            self.buttons_container, 
            text="Load Images", 
            command=self.load_images,
            cursor="hand2"
        )
        self.load_button.pack(side=tk.TOP, fill=tk.X, pady=2)
        
        self.clear_button = tk.Button(
            self.buttons_container, 
            text="Clear Rectangles (C)", 
            command=self.clear_rectangles,
            cursor="hand2"
        )
        self.clear_button.pack(side=tk.TOP, fill=tk.X, pady=2)

        self.confirm_button = tk.Button(
            self.buttons_container, 
            text="Save & Next (S)", 
            command=self.confirm_and_save,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9, "bold"),
            cursor="hand2"
        )
        self.confirm_button.pack(side=tk.TOP, fill=tk.X, pady=2)

        # Drawing variables
        self.source_directory = ""
        self.destination_directory = ""
        self.image_files = []
        self.current_index = 0
        self.rectangles = []
        self.rect_coords = []
        self.start_x = None
        self.start_y = None
        self.rect_id = None

        # Right-click selection variables
        self.right_dragging = False
        self.right_drag_start_x = None
        self.right_drag_start_y = None
        self.sel_rect_id = None

        # Left-click drawing bindings
        self.bind("<ButtonPress-1>", self.start_drawing)
        self.bind("<B1-Motion>", self.drawing)
        self.bind("<ButtonRelease-1>", self.finish_drawing)

        # Undo/redo stacks
        self.undo_stack = []
        self.redo_stack = []
        
        # Undo/redo bindings
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)
        self.bind("<Control-Z>", self.undo)
        self.bind("<Control-Y>", self.redo)
        
        # Right-click bindings for selection
        self.canvas.bind("<ButtonPress-3>", self.start_right_drag)
        self.canvas.bind("<B3-Motion>", self.right_drag)
        self.canvas.bind("<ButtonRelease-3>", self.end_right_drag)
        
        # General keyboard shortcuts
        self.bind("<KeyPress-s>", lambda event: self.confirm_and_save())
        self.bind("<KeyPress-a>", lambda event: self.run_yolo_detection())
        self.bind("<KeyPress-c>", lambda event: self.clear_rectangles())
        self.bind("<Delete>", self.delete_selected_label)
        
        # Navigation shortcuts
        self.bind("<Left>", self.previous_image)
        self.bind("<Right>", self.next_image)
        
        # Label shortcuts (0-9)
        for i in range(10):
            self.bind(f"<KeyPress-{i}>", lambda event, d=i: self.select_label_by_number(d))
            self.bind(f"<Alt-KeyPress-{i}>", lambda event, d=i: self.create_new_label_by_number(d))

    def _on_class_mousewheel(self, event):
        """Handle mousewheel scrolling for class list."""
        if self.class_canvas.winfo_exists():
            self.class_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_confidence_label(self, value):
        """Update confidence threshold label."""
        self.conf_threshold = float(value)
        self.conf_label.config(text=f"Confidence: {float(value):.2f}")

    def update_status(self, message, duration=3000):
        """Update status bar with a message."""
        self.status_bar.config(text=message)
        if duration > 0:
            self.after(duration, lambda: self.status_bar.config(text="Ready"))

    def select_all_classes(self):
        """Select all YOLO classes."""
        for var in self.class_checkboxes.values():
            var.set(True)
        self.update_selected_classes()
        self.update_status("All classes selected")

    def select_no_classes(self):
        """Deselect all YOLO classes."""
        for var in self.class_checkboxes.values():
            var.set(False)
        self.update_selected_classes()
        self.update_status("All classes deselected")

    def update_selected_classes(self):
        """Update the set of selected classes based on checkboxes."""
        self.selected_classes = set()
        for class_id, var in self.class_checkboxes.items():
            if var.get():
                self.selected_classes.add(class_id)

    def select_label_by_number(self, num):
        """Select a label by its numeric index."""
        if num < len(self.labels):
            self.current_label_id = self.labels[num]["id"]
            self.current_color = self.labels[num]["color"]
            # Update visual selection
            for label in self.labels:
                if label["id"] == num:
                    label["widget"].config(bg="lightblue")
                else:
                    label["widget"].config(bg="SystemButtonFace")
            self.update_status(f"Selected label: {self.labels[num]['name']}")
    
    def create_new_label_by_number(self, num):
        """Create a new label with Alt+number shortcut."""
        if num == len(self.labels):
            label_name = simpledialog.askstring("New Label", f"Enter name for new label {num}:")
            if label_name:
                new_id = num
                color = self.label_colors[new_id % len(self.label_colors)]
                self.labels.append({
                    "id": new_id,
                    "name": label_name,
                    "color": color
                })
                self.create_label_widget(new_id)
                self.update_status(f"Created label: {label_name}")

    def add_label(self):
        """Add a new label through the UI button."""
        label_name = simpledialog.askstring("New Label", "Enter label name:")
        if label_name:
            new_id = len(self.labels)
            color = self.label_colors[new_id % len(self.label_colors)]
            self.labels.append({
                "id": new_id,
                "name": label_name,
                "color": color
            })
            self.create_label_widget(new_id)
            self.update_status(f"Created label: {label_name}")

    def create_label_widget(self, label_id):
        """Create UI widget for a label."""
        label = next((l for l in self.labels if l["id"] == label_id), None)
        if not label:
            return

        frame = tk.Frame(self.labels_frame, relief=tk.RAISED, borderwidth=1, bg="white")
        frame.pack(fill=tk.X, padx=2, pady=2)
        
        # Color indicator
        color_canvas = tk.Canvas(frame, width=20, height=20, bg=label["color"], highlightthickness=0)
        color_canvas.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Label name with ID
        label_text = f"[{label['id']}] {label['name']}"
        label_name = tk.Label(frame, text=label_text, bg="white")
        label_name.pack(side=tk.LEFT, padx=5)
        
        # Click handler to select label
        def select_label(event):
            self.current_label_id = label["id"]
            self.current_color = label["color"]
            for child in self.labels_frame.winfo_children():
                child.config(bg="white")
            frame.config(bg="lightblue")
            self.update_status(f"Selected label: {label['name']}")
        
        frame.bind("<Button-1>", select_label)
        color_canvas.bind("<Button-1>", select_label)
        label_name.bind("<Button-1>", select_label)
        
        label["widget"] = frame

    def load_yolo_model(self):
        """Load a YOLO model from file."""
        if YOLO is None:
            messagebox.showerror("Error", "Ultralytics not installed. Please install it to use YOLO features.")
            return
            
        model_path = filedialog.askopenfilename(
            title="Select YOLO Model", 
            filetypes=[("PyTorch Model", "*.pt")]
        )
        if model_path:
            try:
                self.update_status("Loading YOLO model...")
                self.model = YOLO(model_path)
                self.class_names = self.model.names
                self.create_class_checkboxes()
                
                # Enable buttons
                self.select_all_btn.config(state=tk.NORMAL)
                self.select_none_btn.config(state=tk.NORMAL)
                self.auto_detect_btn.config(state=tk.NORMAL)
                
                # Auto-select all classes
                self.select_all_classes()
                
                model_name = os.path.basename(model_path)
                self.update_status(f"Model loaded: {model_name} ({len(self.class_names)} classes)")
                messagebox.showinfo("Success", f"Model loaded successfully!\n{len(self.class_names)} classes detected.")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading model: {e}")
                self.update_status("Error loading model")

    def create_class_checkboxes(self):
        """Create checkboxes for each YOLO class."""
        # Clear existing checkboxes
        for widget in self.class_inner_frame.winfo_children():
            widget.destroy()
        self.class_checkboxes.clear()
        
        # Create new checkboxes
        for i, name in self.class_names.items():
            var = tk.BooleanVar(value=False)
            self.class_checkboxes[i] = var
            
            frame = tk.Frame(self.class_inner_frame, bg="white")
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Color indicator
            color = self.label_colors[i % len(self.label_colors)]
            color_box = tk.Canvas(frame, width=15, height=15, bg=color, highlightthickness=0)
            color_box.pack(side=tk.LEFT, padx=(0, 5))
            
            # Checkbox with class name
            cb = tk.Checkbutton(
                frame,
                text=f"[{i}] {name}",
                variable=var,
                command=self.update_selected_classes,
                bg="white",
                anchor="w"
            )
            cb.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def run_yolo_detection(self):
        """Run YOLO detection on the current image."""
        if not self.model or not self.image_files:
            self.update_status("No model or images loaded")
            return

        if not self.selected_classes:
            messagebox.showwarning("No Classes Selected", "Please select at least one class for detection.")
            return

        self.update_status("Running detection...")
        current_image = os.path.join(self.source_directory, self.image_files[self.current_index])
        results = self.model.predict(current_image, verbose=False)

        detection_count = 0
        # Process prediction results
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()

            for box, cls, conf in zip(boxes, classes, confidences):
                if conf >= self.conf_threshold:
                    if int(cls) in self.selected_classes:
                        x1, y1, x2, y2 = box
                        self.add_detected_rectangle(int(cls), (x1, y1, x2, y2))
                        detection_count += 1
        
        self.update_status(f"Detection complete: {detection_count} objects found")

    def add_detected_rectangle(self, class_id, coords):
        """Add a rectangle detected by YOLO."""
        # Create label if it doesn't exist
        if not any(label["id"] == class_id for label in self.labels):
            self.create_new_label_from_id(class_id)
    
        # Calculate scaled coordinates based on current zoom
        scaled_coords = (
            coords[0] * self.zoom_level,
            coords[1] * self.zoom_level,
            coords[2] * self.zoom_level,
            coords[3] * self.zoom_level
        )
    
        # Draw rectangle with scaled coordinates
        rect_id = self.canvas.create_rectangle(
            scaled_coords[0], scaled_coords[1],
            scaled_coords[2], scaled_coords[3],
            outline=self.get_label_color(class_id),
            width=2
        )
    
        # Save original (unscaled) coordinates for later zoom updates
        self.rect_coords.append(rect_id)
        self.rectangles.append({
            "coords": coords,
            "label_id": class_id
        })

    def load_images(self):
        """Load images from source directory."""
        self.source_directory = filedialog.askdirectory(title="Select Source Directory")
        if not self.source_directory:
            return
            
        self.destination_directory = filedialog.askdirectory(title="Select Destination Directory")
        if not self.destination_directory:
            return
            
        self.image_files = [
            f for f in os.listdir(self.source_directory) 
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]
        
        if not self.image_files:
            messagebox.showwarning("No Images", "No valid images found in the selected directory.")
            self.update_status("No images found")
            return
            
        self.update_image_listbox()
        if self.image_files:
            self.current_index = 0
            self.show_image(0)
            self.update_status(f"Loaded {len(self.image_files)} images")

    def update_image_listbox(self):
        """Update the image listbox with loaded images."""
        self.image_listbox.delete(0, tk.END)
        for f in self.image_files:
            self.image_listbox.insert(tk.END, f)

    def on_image_select(self, event):
        """Handle image selection from listbox."""
        selection = self.image_listbox.curselection()
        if selection:
            index = selection[0]
            if index != self.current_index:
                self.current_index = index
                self.show_image(index)

    def next_image(self, event=None):
        """Navigate to next image."""
        if self.image_files and self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.show_image(self.current_index)
            self.image_listbox.selection_clear(0, tk.END)
            self.image_listbox.selection_set(self.current_index)
            self.image_listbox.see(self.current_index)

    def previous_image(self, event=None):
        """Navigate to previous image."""
        if self.image_files and self.current_index > 0:
            self.current_index -= 1
            self.show_image(self.current_index)
            self.image_listbox.selection_clear(0, tk.END)
            self.image_listbox.selection_set(self.current_index)
            self.image_listbox.see(self.current_index)

    def scroll_vertical(self, event):
        """Handle vertical scrolling."""
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")

    def scroll_horizontal(self, event):
        """Handle horizontal scrolling."""
        if event.delta > 0:
            self.canvas.xview_scroll(-1, "units")
        else:
            self.canvas.xview_scroll(1, "units")

    def zoom(self, event):
        """Handle zoom with Ctrl+MouseWheel."""
        # Adjust zoom level
        if event.delta > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level /= 1.1

        # Update image if original exists
        if hasattr(self, 'current_image_original'):
            width, height = self.current_image_original.size
            new_width = int(width * self.zoom_level)
            new_height = int(height * self.zoom_level)
            img_resized = self.current_image_original.resize(
                (new_width, new_height), 
                Image.Resampling.LANCZOS
            )
            self.img_tk = ImageTk.PhotoImage(img_resized)
            self.canvas.itemconfig(self.image_id, image=self.img_tk)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
        # Update rectangle positions
        self.update_rectangles()
        self.update_status(f"Zoom: {self.zoom_level:.1f}x")

    def update_rectangles(self):
        """Update rectangle coordinates based on current zoom level."""
        for idx, rect in enumerate(self.rectangles):
            # Original (unscaled) coordinates
            x1, y1, x2, y2 = rect["coords"]
            new_coords = (
                x1 * self.zoom_level, 
                y1 * self.zoom_level,
                x2 * self.zoom_level, 
                y2 * self.zoom_level
            )
            self.canvas.coords(self.rect_coords[idx], *new_coords)

    def show_image(self, index):
        """Display an image and load its annotations."""
        self.clear_rectangles()
        
        # Reset zoom if option is enabled
        if self.reset_zoom_var.get():
            self.zoom_level = 1.0
        
        image_path = os.path.join(self.source_directory, self.image_files[index])
        self.current_image_original = Image.open(image_path)
        width, height = self.current_image_original.size
        self.original_width = width
        self.original_height = height

        # Apply zoom
        new_width = int(width * self.zoom_level)
        new_height = int(height * self.zoom_level)
        img_resized = self.current_image_original.resize(
            (new_width, new_height), 
            Image.Resampling.LANCZOS
        )
        self.img_tk = ImageTk.PhotoImage(img_resized)

        # Create or update image on canvas
        if hasattr(self, 'image_id'):
            self.canvas.itemconfig(self.image_id, image=self.img_tk)
        else:
            self.image_id = self.canvas.create_image(0, 0, image=self.img_tk, anchor="nw")

        # Ensure image is behind annotations
        self.canvas.tag_lower(self.image_id)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Load existing annotations if present
        txt_filename = os.path.splitext(self.image_files[index])[0] + ".txt"
        txt_filepath = os.path.join(self.destination_directory, txt_filename)

        annotation_count = 0
        if os.path.exists(txt_filepath):
            with open(txt_filepath, 'r') as f:
                lines = f.readlines()
    
            for line in lines:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
        
                try:
                    label_id = int(parts[0])
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    w = float(parts[3])
                    h = float(parts[4])
                except ValueError:
                    continue
            
                # Convert YOLO coordinates to pixels
                x_center_abs = x_center * width
                y_center_abs = y_center * height
                w_abs = w * width
                h_abs = h * height
        
                x1 = max(0, x_center_abs - w_abs/2)
                y1 = max(0, y_center_abs - h_abs/2)
                x2 = min(width, x_center_abs + w_abs/2)
                y2 = min(height, y_center_abs + h_abs/2)
        
                # Scale coordinates based on current zoom
                scaled_coords = (
                    x1 * self.zoom_level,
                    y1 * self.zoom_level,
                    x2 * self.zoom_level,
                    y2 * self.zoom_level
                )
        
                # Create rectangle with scaled coordinates
                rect_id = self.canvas.create_rectangle(
                    *scaled_coords,
                    outline=self.get_label_color(label_id),
                    width=2
                )
        
                self.rect_coords.append(rect_id)
                self.rectangles.append({
                    "coords": (x1, y1, x2, y2),  # Original coordinates
                    "label_id": label_id
                })
                annotation_count += 1
        
                if not any(l["id"] == label_id for l in self.labels):
                    self.create_new_label_from_id(label_id)

        # Run auto-detect if enabled
        if self.auto_detect_var.get() and self.model:
            self.run_yolo_detection()
        
        # Update status bar
        status_msg = f"Image {index + 1}/{len(self.image_files)}: {self.image_files[index]}"
        if annotation_count > 0:
            status_msg += f" ({annotation_count} annotations loaded)"
        self.update_status(status_msg, duration=0)

    def get_label_color(self, label_id):
        """Get the color for a specific label ID."""
        for label in self.labels:
            if label["id"] == label_id:
                return label["color"]
        return self.label_colors[label_id % len(self.label_colors)]

    def create_new_label_from_id(self, label_id):
        """Create a new label from a YOLO class ID."""
        if label_id in self.class_names:
            label_name = self.class_names[label_id]
        else:
            label_name = f"label_{label_id}"
            
        color = self.label_colors[label_id % len(self.label_colors)]
        self.labels.append({
            "id": label_id,
            "name": label_name,
            "color": color
        })
        self.create_label_widget(label_id)

    def delete_selected_label(self, event):
        """Delete the currently selected label after confirmation."""
        selected_label = next((l for l in self.labels if l["id"] == self.current_label_id), None)
        if selected_label:
            confirm = messagebox.askyesno(
                "Confirm Deletion", 
                f"Are you sure you want to delete label '{selected_label['name']}'?"
            )
            if confirm:
                # Destroy widget and remove from list
                selected_label["widget"].destroy()
                self.labels = [l for l in self.labels if l["id"] != self.current_label_id]
                
                # Update selection
                if self.labels:
                    self.current_label_id = self.labels[0]["id"]
                    self.current_color = self.labels[0]["color"]
                    for label in self.labels:
                        if label["id"] == self.current_label_id:
                            label["widget"].config(bg="lightblue")
                        else:
                            label["widget"].config(bg="white")
                else:
                    self.current_label_id = None
                    self.current_color = "black"
                
                self.update_status(f"Deleted label: {selected_label['name']}")

    def start_drawing(self, event):
        """Start drawing a bounding box."""
        x = self.canvas.canvasx(event.x) / self.zoom_level
        y = self.canvas.canvasy(event.y) / self.zoom_level
        self.start_x = max(0, min(x, self.original_width))
        self.start_y = max(0, min(y, self.original_height))
        self.rect_id = None
    
    def drawing(self, event):
        """Update rectangle while dragging."""
        if self.start_x and self.start_y:
            current_x = self.canvas.canvasx(event.x) / self.zoom_level
            current_y = self.canvas.canvasy(event.y) / self.zoom_level
            current_x = max(0, min(current_x, self.original_width))
            current_y = max(0, min(current_y, self.original_height))
        
            if self.rect_id:
                self.canvas.delete(self.rect_id)
            self.rect_id = self.canvas.create_rectangle(
                self.start_x * self.zoom_level, 
                self.start_y * self.zoom_level, 
                current_x * self.zoom_level, 
                current_y * self.zoom_level, 
                outline=self.current_color,
                width=2
            )
    
    def finish_drawing(self, event):
        """Finish drawing a bounding box."""
        if self.rect_id:
            current_x = self.canvas.canvasx(event.x) / self.zoom_level
            current_y = self.canvas.canvasy(event.y) / self.zoom_level
            current_x = max(0, min(current_x, self.original_width))
            current_y = max(0, min(current_y, self.original_height))
        
            x1 = min(self.start_x, current_x)
            y1 = min(self.start_y, current_y)
            x2 = max(self.start_x, current_x)
            y2 = max(self.start_y, current_y)
        
            self.canvas.coords(
                self.rect_id,
                x1 * self.zoom_level,
                y1 * self.zoom_level,
                x2 * self.zoom_level,
                y2 * self.zoom_level
            )
        
            rect_data = {
                "coords": (x1, y1, x2, y2),
                "label_id": self.current_label_id,
                "rect_id": self.rect_id
            }
        
            self.rectangles.append(rect_data)
            self.rect_coords.append(self.rect_id)
            self.undo_stack.append({'type': 'add', 'data': rect_data.copy()})
            self.redo_stack.clear()
            
            self.update_status(f"Added annotation ({len(self.rectangles)} total)", duration=2000)
        
        self.start_x = None
        self.start_y = None

    def delete_rectangle(self, rect_id):
        """Delete a rectangle and add to undo stack."""
        index = next((i for i, r in enumerate(self.rect_coords) if r == rect_id), -1)
        if index >= 0:
            rect_data = self.rectangles[index]
            
            # Add to undo stack
            self.undo_stack.append({
                'type': 'delete',
                'data': rect_data.copy()
            })
            self.redo_stack.clear()
            
            self.canvas.delete(rect_id)
            del self.rect_coords[index]
            del self.rectangles[index]
            
            self.update_status(f"Deleted annotation ({len(self.rectangles)} remaining)", duration=2000)

    def undo(self, event=None):
        """Undo the last action."""
        if self.undo_stack:
            action = self.undo_stack.pop()
        
            if action['type'] == 'add':
                rect_id = action['data']['rect_id']
                self.canvas.delete(rect_id)
                # Find index using rect_id
                if rect_id in self.rect_coords:
                    index = self.rect_coords.index(rect_id)
                    del self.rect_coords[index]
                    del self.rectangles[index]
                self.redo_stack.append(action)
            
            elif action['type'] == 'delete':
                rect_data = action['data']
                new_id = self.canvas.create_rectangle(
                    rect_data['coords'][0] * self.zoom_level,
                    rect_data['coords'][1] * self.zoom_level,
                    rect_data['coords'][2] * self.zoom_level,
                    rect_data['coords'][3] * self.zoom_level,
                    outline=self.get_label_color(rect_data['label_id']),
                    width=2
                )
                self.rectangles.append({
                    "coords": rect_data['coords'],
                    "label_id": rect_data['label_id'],
                    "rect_id": new_id
                })
                self.rect_coords.append(new_id)
                self.redo_stack.append(action)
            
            self.update_status("Undo", duration=1000)

    def redo(self, event=None):
        """Redo the last undone action."""
        if self.redo_stack:
            action = self.redo_stack.pop()
        
            if action['type'] == 'add':
                # Restore rectangle with zoom scaling
                rect_data = action['data']
                new_id = self.canvas.create_rectangle(
                    rect_data['coords'][0] * self.zoom_level,
                    rect_data['coords'][1] * self.zoom_level,
                    rect_data['coords'][2] * self.zoom_level,
                    rect_data['coords'][3] * self.zoom_level,
                    outline=self.get_label_color(rect_data['label_id']),
                    width=2
                )
                rect_data['rect_id'] = new_id
                self.rectangles.append(rect_data)
                self.rect_coords.append(new_id)
                self.undo_stack.append(action)
            
            elif action['type'] == 'delete':
                # Undo restoration
                rect_id = action['data']['rect_id']
                self.canvas.delete(rect_id)
                self.rect_coords = [r for r in self.rect_coords if r != rect_id]
                self.rectangles = [r for r in self.rectangles if r['rect_id'] != rect_id]
                self.undo_stack.append(action)
            
            self.update_status("Redo", duration=1000)

    def clear_rectangles(self):
        """Clear all rectangles from canvas."""
        for rect_id in self.rect_coords:
            self.canvas.delete(rect_id)
        self.rectangles.clear()
        self.rect_coords.clear()
        self.update_status("All annotations cleared")

    def confirm_and_save(self):
        """Save current annotations and move to next image."""
        if not self.image_files:
            return
            
        txt_filename = os.path.splitext(self.image_files[self.current_index])[0] + ".txt"
        txt_filepath = os.path.join(self.destination_directory, txt_filename)
        
        if self.rectangles:
            image_path = os.path.join(self.source_directory, self.image_files[self.current_index])
            image = Image.open(image_path)
            width, height = image.size

            yolo_coords = []
            for rect in self.rectangles:
                x1, y1, x2, y2 = rect["coords"]
                label_id = rect["label_id"]
                
                # Convert to YOLO format (normalized)
                x_center = (x1 + x2) / 2 / width
                y_center = (y1 + y2) / 2 / height
                obj_width = (x2 - x1) / width
                obj_height = (y2 - y1) / height
                
                yolo_coords.append(f"{label_id} {x_center} {y_center} {obj_width} {obj_height}")

            with open(txt_filepath, "w") as file:
                file.write("\n".join(yolo_coords))
            
            self.update_status(f"Saved {len(self.rectangles)} annotations to {txt_filename}")
        else:
            # Create empty file if no annotations
            open(txt_filepath, 'w').close()
            self.update_status(f"Saved empty annotation file: {txt_filename}")

        # Move to next image
        self.current_index += 1
        if self.current_index < len(self.image_files):
            self.show_image(self.current_index)
            self.image_listbox.selection_clear(0, tk.END)
            self.image_listbox.selection_set(self.current_index)
            self.image_listbox.see(self.current_index)
        else:
            self.update_status("All images processed!", duration=0)
            self.canvas.delete("all")

    # Right-click selection functions
    def start_right_drag(self, event):
        """Start right-click drag selection."""
        self.right_dragging = True
        x = self.canvas.canvasx(event.x) / self.zoom_level
        y = self.canvas.canvasy(event.y) / self.zoom_level
        self.right_drag_start_x = max(0, min(x, self.original_width))
        self.right_drag_start_y = max(0, min(y, self.original_height))
        self.sel_rect_id = None

    def right_drag(self, event):
        """Update selection rectangle while dragging."""
        if self.right_dragging:
            current_x = self.canvas.canvasx(event.x) / self.zoom_level
            current_y = self.canvas.canvasy(event.y) / self.zoom_level
            current_x = max(0, min(current_x, self.original_width))
            current_y = max(0, min(current_y, self.original_height))
        
            x1 = min(self.right_drag_start_x, current_x)
            y1 = min(self.right_drag_start_y, current_y)
            x2 = max(self.right_drag_start_x, current_x)
            y2 = max(self.right_drag_start_y, current_y)
        
            if self.sel_rect_id is None:
                self.sel_rect_id = self.canvas.create_rectangle(
                    x1 * self.zoom_level, 
                    y1 * self.zoom_level, 
                    x2 * self.zoom_level, 
                    y2 * self.zoom_level, 
                    outline="blue", 
                    dash=(4,2),
                    width=2
                )
            else:
                self.canvas.coords(
                    self.sel_rect_id,
                    x1 * self.zoom_level,
                    y1 * self.zoom_level,
                    x2 * self.zoom_level,
                    y2 * self.zoom_level
                )

    def end_right_drag(self, event):
        """End right-click drag and delete selected rectangles."""
        if not self.right_dragging:
            return
        self.right_dragging = False

        # Normalized coordinates with zoom factor
        current_x = self.canvas.canvasx(event.x) / self.zoom_level
        current_y = self.canvas.canvasy(event.y) / self.zoom_level
        current_x = max(0, min(current_x, self.original_width))
        current_y = max(0, min(current_y, self.original_height))

        dx = abs(current_x - self.right_drag_start_x)
        dy = abs(current_y - self.right_drag_start_y)
    
        # Adaptive threshold based on zoom level
        threshold = 5 / self.zoom_level
    
        if dx < threshold and dy < threshold:
            # Simple click: delete rectangle under cursor
            x = self.right_drag_start_x
            y = self.right_drag_start_y
            items = self.canvas.find_overlapping(
                (x - 1) * self.zoom_level,
                (y - 1) * self.zoom_level,
                (x + 1) * self.zoom_level,
                (y + 1) * self.zoom_level
            )
            for item in items:
                if item in self.rect_coords:
                    self.delete_rectangle(item)
                    break
        else:
            # Drag: calculate selection rectangle
            x1 = min(self.right_drag_start_x, current_x)
            y1 = min(self.right_drag_start_y, current_y)
            x2 = max(self.right_drag_start_x, current_x)
            y2 = max(self.right_drag_start_y, current_y)

            indices_to_remove = []
        
            if event.state & 0x0001:
                # Shift + right-click: delete partially overlapping rectangles
                for i, rect in enumerate(self.rectangles):
                    rx1, ry1, rx2, ry2 = rect["coords"]
                    if not (rx2 < x1 or rx1 > x2 or ry2 < y1 or ry1 > y2):
                        indices_to_remove.append(i)
            else:
                # Normal right-click: delete fully contained rectangles only
                for i, rect in enumerate(self.rectangles):
                    rx1, ry1, rx2, ry2 = rect["coords"]
                    if rx1 >= x1 and ry1 >= y1 and rx2 <= x2 and ry2 <= y2:
                        indices_to_remove.append(i)

            for i in sorted(indices_to_remove, reverse=True):
                self.delete_rectangle(self.rect_coords[i])
            
            if indices_to_remove:
                self.update_status(f"Deleted {len(indices_to_remove)} annotations")

        # Remove selection rectangle if present
        if self.sel_rect_id is not None:
            self.canvas.delete(self.sel_rect_id)
            self.sel_rect_id = None


if __name__ == "__main__":
    app = ImageDrawer()
    app.mainloop()
