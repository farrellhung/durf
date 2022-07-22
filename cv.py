import cv2
import numpy as np
import math

def main():
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    cap = cv2.VideoCapture('cam.mp4')
    while True:
        ret, raw = cap.read()

        # channel
        L, U, V = cv2.split(cv2.cvtColor(raw, cv2.COLOR_BGR2LUV))
        channel = cv2.merge([V, V, V])
        channel = cv2.cvtColor(channel, cv2.COLOR_BGR2GRAY)
        cv2.imshow('pre1', channel)
        
        # threshold
        retval, threshold = cv2.threshold(channel, 130, 255, 0)
        cv2.imshow("threshold", threshold)

        # smooth
        # closed = cv2.erode(cv2.dilate(threshold, kernel, iterations=1), kernel, iterations=1)
        closed = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        closed = cv2.medianBlur(closed, 3)
        cv2.imshow("smooth", closed)

        
        contours, hierarchy = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        cv2.drawContours(closed, contours, -1, (255,0,0), 2)

        for contour in contours:
            contour = cv2.convexHull(contour)
            area = cv2.contourArea(contour)
            bounding_box = cv2.boundingRect(contour)

            extend = area / (bounding_box[2] * bounding_box[3])

            circumference = cv2.arcLength(contour,True)
            circularity = area and circumference ** 2 / (4*math.pi*area)

            # reject the contours with big extend
            if extend > 0.8 or area < 500 or circularity > 1.2:
                continue

            # calculate countour center and draw a dot there
            m = cv2.moments(contour)
            if m['m00'] != 0:
                center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                cv2.circle(raw, center, 3, (0, 255, 0), -1)

            # fit an ellipse around the contour and draw it into the image
            try:
                ellipse = cv2.fitEllipse(contour)
                cv2.ellipse(raw, box=ellipse, color=(0, 255, 0))
            except:
                pass

        cv2.imshow('output', raw)

        if cv2.waitKey(30) & 0xff == ord('q'):
            break

    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def getCirles(frame):
    pass

if __name__ == "__main__":
    main()