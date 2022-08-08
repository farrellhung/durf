# use this to compare different channels of an image/video

import cv2
import numpy as np

def extract_channel(img):
    B,G,R = cv2.split(img)
    H,S,V = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
    H2,L2,S2 = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HLS))
    L4,U4,V4 = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2LUV))
    L3,A3,B3 = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2LAB))
    channels = (((B, 'blue'), (G, 'green'), (R, 'red')),
                ((H, 'hue'), (S, 'saturation'), (V, 'value')),
                ((H2, 'hue'), (L2, 'luminosity'), (S2, 'saturation')),
                ((L4,'luminance'), (U4, 'chroma u'), (V4, 'chroma v')),
                ((L3, 'lightness'), (A3, 'green-red'), (B3, 'blue-yellow')))
    output = []
    for space in channels:
        img_row = []
        for image, channel in space:
            cv2.putText(image, channel, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
            img_row.append(image)
        output.append(cv2.hconcat(img_row))
    return cv2.vconcat(output)

img = cv2.imread('eyes.png')
# cap = cv2.VideoCapture('cam.mp4')

cv2.namedWindow('channel', cv2.WINDOW_NORMAL)
cv2.resizeWindow('channel', 1920, 1080)


# while True:
#     ret, raw = cap.read()
#     cv2.imshow('channel', extract_channel(raw))
#     if cv2.waitKey(30) & 0xff == ord('q'):
#         break


cv2.imshow('channel', extract_channel(img))
cv2.waitKey(0)
cv2.destroyAllWindows()