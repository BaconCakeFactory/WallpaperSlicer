import math
from os import path as os_path, chdir, mkdir
import numpy
import cv2
import tkinter
from tkinter import filedialog
from pathlib import Path
from datetime import datetime
from numpy import any as np_any
from screeninfo import get_monitors
import subprocess
import sys
import os

# for wallpaper change
import shutil

g_border_width = 20
g_saving_res_w = 1920
g_saving_res_h = 1080


def get_monitor_sizes() -> list:
    sizes = []
    for m in get_monitors():
        sizes.append([m.width_mm, m.height_mm, m.is_primary])

    return sizes


def monitor_str(size: list) -> str:
    prim = ""
    if size[2]:
        prim = " Primary"

    return "[w: " + str(size[0]) + " h: " + str(size[1]) + prim + "]"


def choose_arrangement(sizes: list) -> list:
    new_arrangement = []
    if len(sizes) == 1:
        return sizes
    if len(sizes) > 3:
        print("this program currently only supports up to three monitors.\n")
    # list monitors

    for j in range(len(sizes) - 1):
        # list monitors
        for i, s in enumerate(sizes):
            print("(" + str(i + 1) + ") " + monitor_str(s))
        # let user choose left monitor
        left_most_monitor = input("Choose the left most monitor: ")
        if not left_most_monitor.isnumeric() or int(left_most_monitor) < 1:
            print("please enter a valid number.")
            exit()
        if int(left_most_monitor) > len(sizes):
            print("there are not that many monitors.")
            exit()
        # input should now be a valid number ( > 0, < len sizes )
        new_arrangement.append(sizes[int(left_most_monitor) - 1])
        sizes.remove(sizes[int(left_most_monitor) - 1])
    # append last element of sizes
    new_arrangement.extend(sizes)

    return new_arrangement


def choose_slicing_preference(img: numpy.ndarray, sizes: list) -> list:
    offsets = []
    choice = ""
    # vertical alignment: offset from top of image when slicing
    if img.shape[0] >= get_widest_monitor(sizes)[1]:
        # choose vertical alignment
        choice = input("Include top, bottom or middle section of image? (t/m/b): ")
    # switch
    widest_height = get_widest_monitor(sizes)[1]
    img_to_monitor_difference = img.shape[0] - widest_height
    for s in sizes:
        if choice == "b":
            offsets.append(int(img_to_monitor_difference + ((widest_height - s[1]) * 0.5)))
            continue
        if choice == "m":
            offsets.append(int((img_to_monitor_difference + ((widest_height - s[1]) * 0.5)) * 0.5))
            print("> img_to_monitor_difference: " + str(img_to_monitor_difference) + ", widest - this / 2: " +
                  str(((widest_height - s[1]) * 0.5)))
            continue
        offsets.append(int((widest_height - s[1]) * 0.5))

    return offsets


def max_image_size_mm(sizes: list) -> list:
    width = 0
    # init with first monitor height
    height = sizes[0][1]
    for s in sizes:
        width += s[0]
        if s[1] > height:
            height = s[1]
    # border between monitors, each 20mm
    width += (len(sizes) - 1) * g_border_width

    return [width, height]


def get_image() -> numpy.ndarray:
    # remove second window (root)
    tkinter.Tk().withdraw()
    # Select Input Image
    path_to_image = filedialog.askopenfilename(filetypes=[("Image of Video files", ".png .jpg .jpeg")],
                                               title="Select an Image.")
    # Set Input Image
    source_img = cv2.imread(path_to_image)
    # Check If Image Was Selected
    if not np_any(source_img):
        print("Error while choosing input image.")
        exit()

    return source_img


def get_widest_monitor(sizes: list) -> list:
    # get widest monitor
    widest = sizes[0]
    for s in sizes:
        if s[0] > widest[0]:
            widest = s

    return widest


def scale_monitor_sizes(img: numpy.ndarray, sizes_o: list) -> list:
    # copy sizes list
    sizes = copy_please.deepcopy(sizes_o)

    # get image height and image width
    img_height, img_width, _ = img.shape

    # get max possible image size
    max_size = max_image_size_mm(sizes)

    # assume landscape mode (width > height)
    # scale width
    one_percent = max_size[0] / 100
    factor = img_width / one_percent / 100

    print(">>>>> monitors: " + str(max_image_size_mm(sizes)) + " - img: " + str(img_width) + ", " + str(img_height))

    # scale sizes to width
    for s in sizes:
        s[0] *= factor
        s[1] *= factor

    print(">>>>> monitors: " + str(max_image_size_mm(sizes)) + " - img: " + str(img_width) + ", " + str(img_height))

    # get max possible image size
    max_size = max_image_size_mm(sizes)

    # if image is too short (height)
    if img_height < get_widest_monitor(sizes)[1]:
        one_percent = max_size[1] / 100
        factor = img_height / one_percent / 100
        # scale sizes to height
        for s in sizes:
            s[0] *= factor
            s[1] *= factor
        print(">>>>> monitors: " + str(max_image_size_mm(sizes)) + " - img: " + str(img_width) + ", " + str(img_height))

    # floor values
    for s in sizes:
        s[0] = math.floor(s[0])
        s[1] = math.floor(s[1])

    return sizes


def slice_img(img: numpy.ndarray, sizes: list, offset_top: list) -> list:
    sliced_images = []
    offset_x = 0
    # slice image
    for (i, s) in enumerate(sizes):
        print(">>>> " + str(offset_top[i] + s[1]))
        cropped_img = img[offset_top[i]:offset_top[i] + int(s[1]), offset_x:offset_x + int(s[0])]
        sliced_images.append(cropped_img)
        offset_x += int((g_border_width + s[0]))

    return sliced_images


def save_slices(images: list) -> str:
    folder_title = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    current_path = Path().resolve()

    general_folder_path = os_path.join(current_path, "wallpaper-slicer-output/")
    if not os.path.isdir(general_folder_path):
        mkdir(general_folder_path)

    folder_path = os_path.join(general_folder_path, folder_title)

    mkdir(folder_path)
    chdir(folder_path)

    for (i, img) in enumerate(images):
        cv2.imwrite(str(i + 1) + ".jpg", img)

    return folder_path


def open_file(filename):
    # from https://stackoverflow.com/questions/17317219/is-there-an-platform-independent-equivalent-of-os-startfile
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


# wallpaper change
def change_wallpaper(number_of_monitors: int, path: str = "") -> None:
    # remove second window (root)
    tkinter.Tk().withdraw()

    name_convention = ["Transcoded_002", "Transcoded_001", "Transcoded_000"]
    output_directory = "C:/Users/User/AppData/Roaming/Microsoft/Windows/Themes"

    # select path
    if not path:
        print("Choose a random file from the folder that holds the wallpapers.")
        path = filedialog.askopenfilename()
        path = os_path.dirname(path)

    if not path:
        print("No path found.")

    # print(path)

    # create list of files in directory that end with .jpg
    images = [f for f in os.listdir(path) if f.endswith(".jpg") or f.endswith(".png")]

    os.chdir(output_directory)

    # loop through amount of desktops
    for (idx, i) in enumerate(images):
        if idx > number_of_monitors - 1:
            continue
        image_path = f"{path}/{i}"
        new_image_path = f"{output_directory}/{name_convention[idx]}"
        shutil.copy(image_path, new_image_path)

    file_name = "restartExplorer.bat"
    file = open(file_name, "w")
    file.write('taskkill /im explorer.exe /f\nstart explorer.exe\nexit')
    file.close()
    filepath = f"{output_directory}/{file_name}"
    os.startfile(filepath)


if __name__ == "__main__":
    # get monitors
    monitor_sizes = get_monitor_sizes()

    number_of_monitors = len(monitor_sizes)

    change_variations = ["change", "wc", "cw"]
    if len(sys.argv) > 1 and sys.argv[1] in change_variations:
        change_wallpaper(number_of_monitors)
        exit()

    # arrange monitors
    arranged_sizes = choose_arrangement(monitor_sizes)
    print(">>> arranged.")

    # get image
    original_img = get_image()
    print(">>> got original.")

    # scale monitor sizes
    scaled_sizes = scale_monitor_sizes(original_img, arranged_sizes)
    print(">>> scaled.")

    # choose slicing preferences
    slicing_offset_top = choose_slicing_preference(original_img, scaled_sizes)

    # slice original image
    slices = slice_img(original_img, scaled_sizes, slicing_offset_top)
    print(">>> sliced.")

    # save images
    save_path = save_slices(slices)
    print(">>> saved.")

    # set wallpapers (only works for windows)
    if os.name == "nt":
        no_change_variations = ["nochange", "no-change", "nc"]
        if len(sys.argv) > 1 and sys.argv[1] in no_change_variations:
            open_file(save_path)
            exit()
        else:
            change_wallpaper(number_of_monitors, save_path)

    # open saved image path
    open_file(save_path)

    exit()
