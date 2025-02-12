

# ArtScii 

## Overview
This project allows you to convert images and videos into ASCII art. You can display the output in the terminal or within a graphical window. The tool supports uploading images and videos or even capturing live video using a webcam.

### Features
- Convert static images to ASCII art.
- Convert videos (files or webcam feed) into ASCII art streams.
- Display ASCII art in the terminal or a graphical window.

---


## Setup Instructions

```bash
# On Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

Install the required Python libraries:
```bash
pip install -r requirements.txt
```


For GUI functionalities, ensure that `tkinter` is installed. It is typically included with Python, but if not, install it via your package manager:
```bash
# On Ubuntu/Debian
sudo apt-get install python3-tk

# On MacOS (already included with Python)
# No extra step required

# On Windows
# Already included with the Python installer
```

---

## Usage

### For Image to ASCII Conversion
Convert an image to ASCII art and display it in the terminal or a GUI window:
```bash
# Display ASCII in terminal
python main.py <image_path>

# Display ASCII in a GUI window
python main.py <image_path> --window

# Open a GUI file selection dialog
python main.py --gui
```

### For Video to ASCII Conversion
Convert a video or webcam feed into ASCII art:
```bash
# Display webcam feed as ASCII in terminal
python experiment.py webcam

# Display webcam feed as ASCII in a GUI window
python experiment.py webcam --window

# Convert a video file into ASCII
python experiment.py <video_path>

# Open a GUI file selection dialog for video
python experiment.py --gui
```

---

## Examples

### Image to ASCII
Run the following command to convert an image:
```bash
python main.py example.jpg
```

### Video to ASCII
Run the following command to stream video as ASCII art:
```bash
python experiment.py example.mp4 --window
```

### Webcam Feed
Display your webcam feed as ASCII art:
```bash
python experiment.py webcam
```

---

## Notes
- Ensure the video/image files exist at the specified paths.
- Resize larger images/videos for better performance.
- The ASCII output works best in monospaced fonts like Courier New.

---

## Dependencies
The following libraries are required:
- **Pillow**: For image processing.
- **OpenCV**: For video processing.
- **Tkinter**: For GUI-based display.
- **NumPy**: For efficient array computations.


---

## Contributing
Feel free to submit issues and pull requests to enhance this project!

## License
This project is licensed under the MIT License.

---

Happy ASCII art creation! 😊
