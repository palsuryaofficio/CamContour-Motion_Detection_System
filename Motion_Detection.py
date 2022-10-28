import cv2 as cv
import time
import serial
from datetime import datetime
import pywhatkit as pwk


# serial init

# serialCom = serial.Serial('COM3', baudrate=9600, timeout=1)  # for connection to arduino serial communication

cap = cv.VideoCapture("http://10.10.68.113:81/stream")

flag1, curr_frame = cap.read()

flag2, next_frame = cap.read()

while True:
    dtTime = datetime.now().strftime('%d %m %Y %H:%M:%S')    # datetime init
    diff = cv.absdiff(curr_frame, next_frame)
    gray = cv.cvtColor(diff, cv.COLOR_RGB2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    cannyEdge = cv.Canny(blur, 100, 200)
    _, thresh = cv.threshold(cannyEdge, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=3)

    contours, hierarchy = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv.boundingRect(contour)

        if cv.contourArea(contour) < 1500:
            continue

        cv.rectangle(curr_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv.putText(curr_frame, "Status: {}".format('Movement'), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        print("Movement Detected!!")



    cv.imshow("SECURITY FEED", curr_frame)
    curr_frame = next_frame
    _, next_frame = cap.read()

    if cv.waitKey(50) == 27:
        break

    time.sleep(15)

cv.destroyAllWindows()
cap.release()
