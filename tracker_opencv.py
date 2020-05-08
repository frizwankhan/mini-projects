#!/usr/bin/env python
import cv2



tracker = cv2.TrackerMIL_create()


cap = cv2.VideoCapture(0)

ret, frame = cap.read()

roi = cv2.selectROI(frame, False)


ret = tracker.init(frame, roi)


while True:

    ret, frame = cap.read()

    success, roi = tracker.update(frame)

    (x,y,w,h) = tuple(map(int,roi))

    if success:

        p1 = (x,y)
        p2 = (x+w, y+h)
        print(f'p1 = {p1} and p2 = {p2}')
        cv2.rectangle(frame, p1, p2, (0,0,255), 3)
        
    else:

        cv2.putText(frame, "failued to detect", (100,200), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 3, cv2.LINE_AA)


    cv2.imshow('tracking',frame)
        
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

