from PIL import Image
import cv2
import numpy as np
from main import image_to_ascii, display_in_window

def video_to_ascii(input_source, output_window=False):
    cap = cv2.VideoCapture(input_source)
    
    if output_window:
        import tkinter as tk
        from tkinter import font
        root = tk.Tk()
        root.title("ASCII Video")
        fixed_font = font.Font(family='Courier New', size=6)
        
        text = tk.Text(root, font=fixed_font, 
                      bg='black', fg='white', wrap=tk.NONE,
                      borderwidth=0, padx=0, pady=0)
        text.pack(fill=tk.BOTH, expand=True)
        root.protocol("WM_DELETE_WINDOW", lambda: cap.release())
    
    def update_frame():
        ret, frame = cap.read()
        if not ret or not cap.isOpened():
            if output_window:
                root.destroy()
            return
        
        # Convert frame to ASCII
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)
        ascii_art = image_to_ascii(pil_img)
        
        if output_window:
            # Calculate exact dimensions for each frame
            lines = ascii_art.split('\n')
            longest_line = max(lines, key=len) if lines else ''
            
            exact_width = fixed_font.measure(longest_line)
            line_height = fixed_font.metrics('linespace')
            window_height = len(lines) * line_height
            
            # Update window geometry
            root.geometry(f"{exact_width}x{window_height}")
            
            text.delete(1.0, tk.END)
            text.insert(tk.END, ascii_art)
            root.after(30, update_frame)
        else:
            print("\033[2J\033[H" + ascii_art)
            cv2.waitKey(41)
            update_frame()
    
    if output_window:
        root.after(0, update_frame)
        root.mainloop()
    else:
        update_frame()
    
    cap.release()
    cv2.destroyAllWindows()

def image_to_ascii(pil_img, max_width=None):
    # Modified version of main.py's function to accept PIL images
    img = pil_img.convert('L')
    
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

def open_video_dialog():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")]
    )
    root.destroy()
    return file_path

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert video to ASCII art')
    parser.add_argument('source', nargs='?', default='webcam',
                       help='Video file path or "webcam" (default: webcam)')
    parser.add_argument('--window', action='store_true',
                       help='Display in window instead of terminal')
    parser.add_argument('--gui', action='store_true',
                       help='Open file selection dialog')
    args = parser.parse_args()

    if args.gui:
        file_path = open_video_dialog()
        if not file_path:
            print("No file selected")
            exit()
        input_source = file_path
    else:
        input_source = 0 if args.source.lower() == 'webcam' else args.source

    video_to_ascii(input_source, args.window)
