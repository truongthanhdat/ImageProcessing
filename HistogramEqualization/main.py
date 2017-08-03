import cv2
import library as lib

def uniform(y):
    return 1.0 / 255.0

def eqhist(image):
    return lib.histogramEqualization(image, uniform)

def HSVImage(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #hsv = lib.convertRGB2HSV(image)
    H = eqhist(hsv[:, :, 0])
    S = eqhist(hsv[:, :, 1])
    V = eqhist(hsv[:, :, 2])
    #hsv[:, :, 0] = H
    hsv[:, :, 1] = S
    #hsv[:, :, 2] = V
    newImage = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return newImage

image = cv2.imread('image.jpg')
newImage = HSVImage(image)
cv2.imwrite('newImage.jpg', newImage)

