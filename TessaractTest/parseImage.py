# import the necessary packages

"""

commands to run to make tesseract run:

pip install pillow
pip install pytesseract

sudo apt-get update
sudo apt-get install libleptonica-dev 
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev

"""
from PIL import Image
import pytesseract
import argparse
import cv2
import os
# construct the argument parse and parse the arguments

# pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"

path_to_rch_lobby = "one2.png"

path_to_room_fig = "one.png"

path_to_bandit_img = "one1.png"

preproc = "thresh" # "blur"

rch = None

passcode = None

num_arms = None


def getrch():
    # load the example image and convert it to grayscale
    image = cv2.imread(path_to_rch_lobby)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the
    # image
    if preproc == "thresh":
        gray = cv2.threshold(gray, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove
    # noise
    elif preproc == "blur":
        gray = cv2.medianBlur(gray, 3)
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    textList = text.split(" ")
    s = "\n"

    string = s.join(textList)

    finaltextList = string.split("\n")

    rch = finaltextList[3]

    print("\n\nNext room is that with the",rch, "number...\n\n")
    # show the output images


def getrooms():
    pass

def getbanditInfo():
        # load the example image and convert it to grayscale
    image = cv2.imread(path_to_bandit_img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the
    # image
    if preproc == "thresh":
        gray = cv2.threshold(gray, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove
    # noise
    elif preproc == "blur":
        gray = cv2.medianBlur(gray, 3)
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)

    textList = text.split("\n")

    passString = textList[5]

    narmString = textList[7]

    passList = passString.split(" ")
    narmList = narmString.split(" ")

    passcode = int(passList[-1])
    num_arms = int(narmList[-1])

    print("\n\nThe Passcode is:",passcode,"\n")
    print("\nThe Number of Arms is:",num_arms,"\n\n")


# Know if to go to highest or lowest numbered room
# getrch()

# get a list containing room numbers
# getrooms()

# get the information about the RL problem
# getbanditInfo()