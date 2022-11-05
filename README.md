<pre><code>__/\\\\\\\\\\\\_________/\\\\\\\\\______/\\\________/\\\___/\\\\\\\\\\\___/\\\\\\\\\\\\_____________/\\\________/\\\________
 _\/\\\////////\\\_____/\\\\\\\\\\\\\___\/\\\_______\/\\\__\/////\\\///___\/\\\////////\\\__________\/\\\_______\/\\\________
  _\/\\\______\//\\\___/\\\/////////\\\__\//\\\______/\\\_______\/\\\______\/\\\______\//\\\_________\/\\\_______\/\\\________
   _\/\\\_______\/\\\__\/\\\_______\/\\\___\//\\\____/\\\________\/\\\______\/\\\_______\/\\\_________\/\\\\\\\\\\\\\\\________
    _\/\\\_______\/\\\__\/\\\\\\\\\\\\\\\____\//\\\__/\\\_________\/\\\______\/\\\_______\/\\\_________\/\\\/////////\\\________
     _\/\\\_______\/\\\__\/\\\/////////\\\_____\//\\\/\\\__________\/\\\______\/\\\_______\/\\\_________\/\\\_______\/\\\________
      _\/\\\_______/\\\___\/\\\_______\/\\\______\//\\\\\___________\/\\\______\/\\\_______/\\\__________\/\\\_______\/\\\________
       _\/\\\\\\\\\\\\/____\/\\\_______\/\\\_______\//\\\_________/\\\\\\\\\\\__\/\\\\\\\\\\\\/___________\/\\\_______\/\\\___/\\\_
        _\////////////______\///________\///_________\///_________\///////////___\////////////_____________\///________\///___\///__
</code></pre>

# Wallpaper Slicer

## README for WallpaperSlicer

### What is it?

- tool that crops images
- can change your wallpaper

### Why?

- let's say you have three monitors of different sizes.
- this tool will crop an image into parts of the image that match the real world size of your monitors.
- it can also automatically set the new wallpapers

### How does it work?

- splits an image into how many monitors you have
- upscales the according cropped image for smaller monitors
- saves new images
- replaces old wallpaper

### Variations

- start with <$ python3 main.py> to run in normal mode (cropping and replacing)
- start with <$ python3 main.py no-change> to run in but not replace old wallpapers
- start with <$ python3 main.py change> to just replace old wallpapers
    - for that: run python file > select folder with images > select random one
    - program will set wallpapers according to the list order of images

### How to run?

- install libraries
- run with python

### Libraries

- update pip: $ pip install --upgrade pip
- install the following libraries in your terminal:

&nbsp;

- $ pip install tk
- $ pip install opencv-python
- $ pip install pathlib
- $ pip install numpy
- $ pip install screeninfo

### Run with python

- unpack zip, if you haven't already
- from your terminal: navigate to "WallpaperSlicer" folder
- run command: **$ python3 main.py**

&nbsp;

- follow on-screen prompt:
    - select left monitor
    - select next left monitor of remaining monitors
- choose which section of the original image the cropped images will be taken from
    - choose top, middle or bottom 

- the finished files (images) will be saved as .jpg in "WallpaperSlicer/wallpaper-slicer-output".

### Keep In mind!

- at the moment, changing the wallpapers automatically is only supported on windows
