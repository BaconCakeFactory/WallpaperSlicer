from sys import exit as sys_exit
from os import system as os_system, name as os_name, path as os_path, chdir, mkdir, startfile
from yaml import safe_load as yaml_safe_load
from cv2 import imread, imwrite, resize
from tkinter import filedialog
from tkinter import Tk
from pathlib import Path
from datetime import datetime
from numpy import any as np_any
from past.builtins import raw_input
from screeninfo import get_monitors

x = 10

# Load Config File For Monitor Dimensions
config = yaml_safe_load(open("config/config.yml"))

Tk().withdraw()

# Make Command To Clear Console
clearConsole = lambda: os_system('cls' if os_name in ('nt', 'dos') else 'clear')

clearConsole()

# Select Input Image
pathToImage = filedialog.askopenfilename()

# Set Input Image
sourceImg = imread(pathToImage)

# Check If Image Was Selected
if not np_any(sourceImg):
    print("Fehler beim Aussuchen des Ausgangsbildes :(")
    sys_exit()

# Get Image Heigth And Set Image Width According To Aspect Ratio
sourceImgHeight, sourceImgWidth, _ = sourceImg.shape
cropH = sourceImgHeight
cropW = (cropH / 9) * 16
mmToPixel = cropW / config.get("dl").get("w")

# Main Desktop Width / Right Desktop Width
mDW = config.get("dm").get("w")
rDW = config.get("dr").get("w")
totalCropWidth = (mDW * 2 + rDW + config.get("dl").get("b") + config.get("dm").get("b")) * mmToPixel

totalCropToSourceRatio = 0

# Offset To Top For Cropping (Section Selection (Top, Middle, Bottom))
offsetH = 0

# Offset To Top For Pushing Crop Into The Middle
offsetW = int((sourceImgWidth - (totalCropWidth + int((mDW - rDW) * mmToPixel))) / 2)

if totalCropWidth > sourceImgWidth:
    print("Cropping Width (", totalCropWidth, ") is greater than Image Width (", sourceImgWidth, ")")

    # Select If The Image Contains Focal Object
    clearConsole()
    print("Does the image contain a focal object?")
    responseSection = None
    while responseSection not in {"y", "n"}:
        responseSection = raw_input("Please enter Yes(Y) or No(N): ").lower()

    if responseSection == "y":
        totalCropWidth = totalCropWidth + int((mDW - rDW) * mmToPixel)

    totalCropToSourceRatio = totalCropWidth / (sourceImgWidth / 100)

    print(totalCropToSourceRatio)

    # Resize Image To Correct Size
    cropSourceRatio = (int(sourceImgWidth * (totalCropToSourceRatio / 100)),
                       int(sourceImgHeight * (totalCropToSourceRatio / 100)))
    sourceImgX = resize(sourceImg, cropSourceRatio)

    sourceImg = sourceImgX
    sourceImgHeight, sourceImgWidth, _ = sourceImg.shape

    # Select What Section Of Image Will Be Cropped
    clearConsole()
    print("What section of the image do you want to crop in?")
    responseSection = None
    while responseSection not in {"t", "m", "b"}:
        responseSection = raw_input("Please enter top(T), middle(M) or bottom(B): ").lower()

    if responseSection == "t":
        offsetH = 0
    if responseSection == "m":
        offsetH = int((sourceImgHeight - cropH) / 2)
    if responseSection == "b":
        offsetH = int(sourceImgHeight - cropH)

    offsetW = 0

# Crop Out First Image
croppedImg1 = sourceImg[offsetH:offsetH + int(cropH), offsetW:offsetW + int(cropW)]

# Offset Next Crop And Convert Pixels To Millimeters
imgOffset = cropW + config.get("dl").get("b") * (cropW / config.get("dl").get("w"))

# Crop Out Second Image
croppedImg2 = sourceImg[offsetH:offsetH + int(cropH), offsetW + int(imgOffset):offsetW + int(imgOffset) + int(cropW)]

# Offset Next Crop And Convert Pixels To Millimeters
imgOffset = imgOffset + cropW + config.get("dm").get("b") * (cropW / config.get("dm").get("w"))

# Crop Out Third Image
croppedImg3 = sourceImg[offsetH:offsetH + int(cropH), offsetW + int(imgOffset):offsetW + int(imgOffset) + int(cropW)]

# Crop Out Third Image For Smaller Screen
smallerImageHeightPercent = config.get("dr").get("h") / (config.get("dm").get("h") / 100)
print(smallerImageHeightPercent)

smallerImageHeight = (cropH / 100) * smallerImageHeightPercent
smallerImageWidth = (smallerImageHeight / 9) * 16

croppedImg3 = croppedImg3[int((cropH - smallerImageHeight) / 2):int(smallerImageHeight + (cropH - smallerImageHeight) / 2), 0:int(smallerImageWidth)]

# cv2.imshow("left", croppedImg1)
# cv2.imshow("middle", croppedImg2)
# cv2.imshow("right", croppedImg3)
# cv2.waitKey(0)

print("Hallo Welt luul!")

folderTitle = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

currentPath = Path().resolve()
folderPath = os_path.join(currentPath, "wallpaperSlicerOutput/" + folderTitle)

mkdir(folderPath)

chdir(folderPath)
imwrite("left.jpg", croppedImg1)
imwrite("middle.jpg", croppedImg2)
imwrite("right.jpg", croppedImg3)

startfile(folderPath)