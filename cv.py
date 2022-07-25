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
    radiusvec = []
    blobvec = []
    areaplot, = plt.plot([])
    radiusplot, = plt.plot([])
    blobplot, = plt.plot([])

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13))
    cap = cv2.VideoCapture('cam.mp4')

    ret, raw = cap.read()
    
    while ret:
        cv2.imshow('raw', raw)
        raw_clone = raw.copy()

        # channel
        B,G,R = cv2.split(raw)
        # cv2.imshow('channel', R)
        
        # morphology transformations
        # note that the binary image is inversed. we are performing transformations for the white area while our object of focus is the black pupil
        closed = cv2.erode(R, kernel)
        closed = cv2.dilate(closed, kernel)
        closed = cv2.medianBlur(closed, 7)
        # cv2.imshow('closed', closed)

        # threshold
        retval, closed = cv2.threshold(closed, 25, 255, cv2.ADAPTIVE_THRESH_MEAN_C)
        cv2.imshow('threshold', closed)

        # blob
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 900
        params.filterByCircularity = True
        params.minCircularity = 0.1
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(closed)
        blob = cv2.drawKeypoints(raw, keypoints, np.zeros((1, 1)), (0, 255, 0),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        try:
            blobvec.append(int(round(keypoints[0].size*35,0)))
        except:
            blobvec.append(0)

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
            if extend > 0.8 or area < 1000 or circularity > 1.1:
                continue

            cv2.putText(raw, 'Area: ' + str(round(area, 2)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 255, 2)
            cv2.putText(raw, 'Circularity: ' + str(round(circularity, 2)), (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 255, 2)
            cv2.putText(raw, 'Extend: ' + str(round(extend, 2)), (5, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 255, 2)
            cv2.putText(raw_clone, 'Area: ' + str(round(area, 2)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 255, 2)
            cv2.putText(raw_clone, 'Circularity: ' + str(round(circularity, 2)), (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 255, 2)
            cv2.putText(raw_clone, 'Extend: ' + str(round(extend, 2)), (5, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 255, 2)

            # calculate countour center and draw a dot there
            m = cv2.moments(contour)
            if m['m00'] != 0:
                center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                cv2.circle(raw, center, 2, (255, 0, 0), -1)

            # fit an ellipse around the contour and draw it into the image
            try:
                c, r = cv2.minEnclosingCircle(contour)
                ellipse = cv2.fitEllipse(contour)
                cv2.ellipse(raw, box=ellipse, color=(255, 0, 0))
                cv2.circle(raw_clone, center, 2, (100,100,255), -1)
                cv2.circle(raw_clone, center, int(r), (100,100,255), 1)
                cv2.putText(raw_clone, 'Radius: ' + str(round(r, 2)), (5, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 255, 2)
            except Exception as e:
                print(e)

            areavec.append(int(round(area,0)))
            radiusvec.append(int(round(r*100,0)))
            break
        else:
            areavec.append(0)
            radiusvec.append(0)

        areaplot.set_data(range(len(areavec[-200:])),areavec[-200:])
        radiusplot.set_data(range(len(radiusvec[-200:])),radiusvec[-200:])
        blobplot.set_data(range(len(blobvec[-200:])),blobvec[-200:])

        plt.draw()
        plt.pause(0.00001)
        cv2.imshow('contour ellipse', raw)
        cv2.imshow('contour circle', raw_clone)
        cv2.imshow('blob', blob)
        ret, raw = cap.read()

        if cv2.waitKey(10) & 0xff == ord(' '):          # press spacebar to pause/play
            if cv2.waitKey(0) & 0xff == ord('q'):       # press q after pausing to quit
                break
    cap.release()
    cv2.destroyAllWindows()
    plt.show()
    

if __name__ == "__main__":
    main()