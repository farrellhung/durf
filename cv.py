import cv2 as cv
import numpy as np

def main():
    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()

        a,b,c = cv.split(frame)

        cframe = c
        cframe = cv.medianBlur(cframe,5)
        cv.imshow("input", c)
        cv.imshow("blur", cframe)
        # cframe = cv.Canny(cframe,100,250)
        circles = cv.HoughCircles(cframe,cv.HOUGH_GRADIENT,1,2000,param1=50,param2=30,minRadius=10,maxRadius=300)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv.circle(frame,(i[0],i[1]),2,(0,0,255),3)

        cv.imshow('test', frame)

        if cv.waitKey(1) & 0xff == ord('q'):
            break
    cap.release()
    cv.waitKey(0)
    cv.destroyAllWindows()

def getCirles(frame):
    pass

if __name__ == "__main__":
    main()
