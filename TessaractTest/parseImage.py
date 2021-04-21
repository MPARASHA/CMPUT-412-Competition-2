# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
# construct the argument parse and parse the arguments

pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"

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

    """
    x1: 30
    y1: 30
    w1: 100

    x2: 30
    y2: 220
    w2: 100
    
    x3: 55
    y3: 440
    w3: 75

    x4: 25
    y4: 610
    w4: 100

    x5: 180
    y5: 70
    w5: 45

    x6: 180
    y6: 170 
    w6: 60
    
    x7: 280
    y7: 40
    w7: 85

    x8: 290
    y8: 180
    w8: 45

    x9: 220
    y9: 310
    w9: 70

    x10: 230
    y10: 640
    w10: 100
    
    x11: 440
    y11: 120
    w11: 100

    x12: 440
    y12: 340
    w12: 100

    x13: 465
    y13: 500
    w13: 55

    x14: 430
    y14: 630
    w14: 100
    
    x15: 620
    y15: 70
    w15: 95

    x16: 640
    y16: 340
    w16: 95

    x17: 640
    y17: 640
    w17: 95
    

    
    x1 = 10
    y1 = 600
    w1 = 150

    img = cv2.imread(path_to_room_fig)
    crop_img = img[y1:y1+w1, x1:x1+w1]
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)

    """
    # load the example image and convert it to grayscale

    x = [30, 30, 55, 25, 180, 180, 280, 290, 220, 230, 440, 440, 465, 430, 620, 640, 640]
    y =  [30, 220, 440, 610, 70, 170, 40, 180, 310, 640, 120, 340, 500, 630, 70, 340, 640]
    w = [100, 100, 75, 100, 45, 60, 85, 45, 70, 100, 100, 100, 55, 100, 95, 95, 95]
    imageFull = cv2.imread(path_to_room_fig)

    rooms = []

    for i in range(17):
        image = imageFull[y[i]:y[i]+w[i], x[i]: x[i] + w[i]]
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

        text =  pytesseract.image_to_string(Image.open(filename))

        if(text == '\x0c'):
            text = pytesseract.image_to_string(Image.open(filename), config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

        textL = text.split("\n")
        rooms.append(textL[0])


        os.remove(filename)

        #cv2.imshow("Output", gray)
        #cv2.waitKey(0)
    print(rooms)


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


def getShapesInfo():
    # load the example image and convert it to grayscale
    image = cv2.imread(path_to_shapes_figure)
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

    colorText = textList[0]
    shapeText = textList[1]

    colorL = colorText.split(" ")
    shapeL = shapeText.split(" ")

    print("\n\nThe Color is:", colorL[-1], "\n")
    print("\nThe Shape is:", shapeL[-1], "\n\n")




# Know if to go to highest or lowest numbered room
# getrch()

# get a list containing room numbers
# getrooms()

# get the information about the RL problem
# getbanditInfo()

# get the color and shape for shapes room
getShapesInfo()