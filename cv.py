from tabnanny import check
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


def main():
    plt.figure(figsize=(10, 6))
    plt.axis([0, 200, 0, 3000])
    plt.xlabel("Tick")
    plt.ylabel("Value")
    areavec = []
    areaplot, = plt.plot([])

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13))
    cap = cv2.VideoCapture('camnir.mp4')
    # cap = cv2.VideoCapture('./nir/%02d.jpg')

    ret, raw = cap.read()
    size = (raw.shape[1], raw.shape[0]) # w*h
    checkingrange = [[0,0],[size[0],size[1]]]
    crop = raw.copy()

    while ret:
        cv2.imshow('raw', raw)

        # channel
        B,G,R = cv2.split(crop)
        # cv2.imshow('channel', R)
        
        # morphology transformations
        # note that the binary image is inversed. we are performing transformations for the white area while our object of focus is the black pupil
        closed = cv2.erode(R, kernel)
        closed = cv2.dilate(closed, kernel)
        closed = cv2.medianBlur(closed, 7)
        cv2.imshow('closed', closed)

        # threshold
        retval, closed = cv2.threshold(closed, 130, 255, cv2.ADAPTIVE_THRESH_MEAN_C)
        cv2.imshow('threshold', closed)

        # contour
        contours, hierarchy = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # cv2.drawContours(closed, contours, -1, (0, 255, 0), 2)

        for contour in contours:
            contour = cv2.convexHull(contour)
            area = cv2.contourArea(contour)
            bounding_box = cv2.boundingRect(contour)

            extend = area / (bounding_box[2] * bounding_box[3])

            circumference = cv2.arcLength(contour,True)
            circularity = area and circumference ** 2 / (4*math.pi*area)

            # reject some contours
            if extend > 0.8 or area < 200 or circularity > 1.05:
                continue

            cv2.putText(raw, 'Area: ' + str(round(area, 2)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 255, 2)
            cv2.putText(raw, 'Circularity: ' + str(round(circularity, 2)), (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 255, 2)
            cv2.putText(raw, 'Extend: ' + str(round(extend, 2)), (5, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 255, 2)

            # calculate countour center and draw a dot there
            m = cv2.moments(contour)
            if m['m00'] != 0:
                center = (int(m['m10'] / m['m00'])+checkingrange[0][0], int(m['m01'] / m['m00'])+checkingrange[0][1])
                cv2.circle(raw, center, 2, (255, 0, 0), -1)
                checkingrange = [[int(center[0]-(size[0]/4)),int(center[1]-(size[1]/4))],[int(center[0]+(size[0]/4)),int(center[1]+(size[1]/4))]]

            # fit an ellipse around the contour and draw it into the image
            try:
                ellipse = list(cv2.fitEllipse(contour))
                ellipse[0] = [ellipse[0][0]+checkingrange[0][0],ellipse[0][1]+checkingrange[0][1]]
                cv2.ellipse(raw, box=ellipse, color=(255, 0, 0))
            except Exception as e:
                print(e)

            areavec.append(int(round(area,0)))
            break
        else:
            areavec.append(0)

        areaplot.set_data(range(len(areavec[-200:])),areavec[-200:])
        plt.draw()
        plt.pause(0.00001)

        cv2.imshow('result', raw)
        ret, raw = cap.read()

        crop = raw[checkingrange[0][1]:checkingrange[1][1],checkingrange[0][0]:checkingrange[1][0]]

        if cv2.waitKey(10) & 0xff == ord(' '):          # press spacebar to pause/play
            if cv2.waitKey(0) & 0xff == ord('q'):       # press q after pausing to quit
                break
    cap.release()
    cv2.destroyAllWindows()
    plt.show()
    

if __name__ == "__main__":
    main()