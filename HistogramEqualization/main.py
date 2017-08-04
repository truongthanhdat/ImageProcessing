import cv2
import library as lib
import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument('--Hue', type=int, default=1)
parser.add_argument('--Saturation', type=int, default=1)
parser.add_argument('--Value', type=int, default=1)
args = parser.parse_args()

def uniform(y):
    return 1.0 / 255.0

def gaussian(x):
    mean = 128
    std = 70
    return 1.0 / np.sqrt(2.0 * np.pi * std * std) * np.exp(0.5 * (x - mean) * (x - mean) / (std * std))

def eqhist(image):
    return lib.histogramEqualization(image, gaussian)

def HSVImage(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #hsv = lib.convertRGB2HSV(image)
    H = eqhist(hsv[:, :, 0])
    S = eqhist(hsv[:, :, 1])
    V = eqhist(hsv[:, :, 2])
    if (args.Hue == 1):
        hsv[:, :, 0] = H
    if (args.Saturation == 1):
        hsv[:, :, 1] = S
    if (args.Value == 1):
        hsv[:, :, 2] = V
    newImage = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return newImage

image = cv2.imread('image.jpg')
newImage = HSVImage(image)
cv2.imshow('Image', newImage)
cv2.waitKey(0)
