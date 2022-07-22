import cv2
import numpy as np
import math

def main():
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    cap = cv2.VideoCapture('cam.mp4')
    while True:
        ret, raw = cap.read()
        cv2.imshow('raw', raw)

        # channel
        B,G,R = cv2.split(raw)
        channel = cv2.merge([R, R, R])
        channel = cv2.cvtColor(channel, cv2.COLOR_BGR2GRAY)
        cv2.imshow('pre1', channel)
        
        # threshold
        retval, threshold = cv2.threshold(channel, 25, 255, 0)
        cv2.imshow("threshold", threshold)

        # smooth
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

            # reject some contours
            if extend > 0.85 or area < 1000 or circularity > 1.15:
                continue

            cv2.putText(raw, 'Area: ' + str(round(area, 2)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 255, 2)
            cv2.putText(raw, 'Circularity: ' + str(round(circularity, 2)), (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 255, 2)
            cv2.putText(raw, 'Extend: ' + str(round(extend, 2)), (5, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 255, 2)

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

        if cv2.waitKey(100) & 0xff == ord('q'):
            break

    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()