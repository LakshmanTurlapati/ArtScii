import argparse
import os
from PIL import Image, ImageOps

try:
    from PIL import Image
except ImportError:
    print("Please install Pillow first: pip install pillow")
    exit()

def image_to_ascii(image_path, output_window=False):
    # Open and convert image to grayscale
    img = Image.open(image_path).convert('L')
    
    # Calculate dimensions based on exact font metrics
    TARGET_PIXEL_WIDTH = 1280
    CHAR_WIDTH = 6  # From 6pt Courier New font
    MAX_CHARS = TARGET_PIXEL_WIDTH // CHAR_WIDTH
    
    # Calculate aspect ratio
    width, height = img.size
    aspect_ratio = height / width / 1.8
    
    # Resize to fit character limits
    new_width = min(MAX_CHARS, width)
    new_height = int(new_width * aspect_ratio)
    
    # Ensure height doesn't exceed max character height
    if new_height > MAX_CHARS:
        new_height = MAX_CHARS
        new_width = int(new_height / aspect_ratio)
    
    # Final dimensions check
    new_width = max(min(new_width, MAX_CHARS), 1)
    new_height = max(min(new_height, MAX_CHARS), 1)
    
    # Resize image
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Enhanced ASCII character set for better gradation
    ascii_chars = "@%#*+=-:. "  # Original set
    # Try this alternative for more detail: "█▓▒░○≡⧆☉⦿⦾◦‧⋅⋄⋯⌇⌲⍟○◌◉◎⁖⁘⁙⁚⁛⁜⁞⁖⁘⁙⁚⁛⁜︎⸳･•"
    # Or simpler: "@%#*+=-:. " (keep original but ensure proper mapping)
    
    # Normalize pixel values to ASCII index
    pixels = resized_img.getdata()
    ascii_str = ''
    char_range = len(ascii_chars) - 1  # Maximum index
    
    for i, pixel_value in enumerate(pixels):
        # Normalize and invert value (0=black→darkest char)
        normalized = min(max(pixel_value, 0), 255) / 255
        inverted = 1 - normalized  # Dark pixels should use dark chars
        index = int(inverted * char_range)
        ascii_str += ascii_chars[index]
        
        if (i + 1) % new_width == 0:
            ascii_str += '\n'
    
    return ascii_str

def display_in_window(ascii_art):
    import tkinter as tk
    from tkinter import font
    
    root = tk.Tk()
    root.title("ASCII Art")
    fixed_font = font.Font(family='Courier New', size=6)
    
    # Calculate exact dimensions
    lines = ascii_art.split('\n')
    longest_line = max(lines, key=len) if lines else ''
    
    # Calculate pixel-perfect width
    exact_width = fixed_font.measure(longest_line)
    line_height = fixed_font.metrics('linespace')
    window_height = len(lines) * line_height
    
    # Set window size
    root.geometry(f"{exact_width}x{window_height}")
    root.resizable(False, False)
    
    # Create text widget with centered alignment
    text = tk.Text(root, font=fixed_font, 
                  bg='black', fg='white', 
                  wrap=tk.NONE, borderwidth=0,
                  padx=0, pady=0)
    text.insert(tk.END, ascii_art)
    text.config(state=tk.DISABLED)
    
    # Add horizontal scrollbar just in case
    x_scroll = tk.Scrollbar(root, orient='horizontal', command=text.xview)
    text.configure(xscrollcommand=x_scroll.set)
    
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    text.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()

def open_file_dialog():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    root.destroy()
    return file_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert images to ASCII art')
    parser.add_argument('image_path', nargs='?', help='Path to the image file (optional if using --gui)')
    parser.add_argument('--window', action='store_true', help='Display in a window instead of terminal')
    parser.add_argument('--gui', action='store_true', help='Open file selection dialog')
    args = parser.parse_args()

    try:
        if args.gui:
            file_path = open_file_dialog()
            if not file_path:
                print("No file selected")
                exit()
            ascii_art = image_to_ascii(file_path)
        else:
            if not args.image_path:
                parser.error("Either provide an image path or use --gui")
            ascii_art = image_to_ascii(args.image_path)

        if args.window:
            display_in_window(ascii_art)
        else:
            print(ascii_art)
    except Exception as e:
        print(f"Error: {e}")
