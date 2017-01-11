from networktables import NetworkTables
import cv2
import numpy as np

NetworkTables.initialize(server='10.6.11.53')

table = NetworkTables.getTable('datatable')

camera_feed = cv2.VideoCapture(0)


xCentroid = 0
xCentroidOne = 0
xCentroidTwo = 0
xCentroidThree = 0
yCentroid = 0
yCentroidOne = 0
yCentroidTwo = 0
yCentroidThree = 0
counter = 0


while(1):
    _,frame = camera_feed.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerT = np.array([54,71,89])
    upperT = np.array([96,255,255])

    mask = cv2.inRange(hsv, lowerT, upperT)

    element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    mask = cv2.erode(mask,element, iterations=2)
    mask = cv2.dilate(mask,element,iterations=2)
    mask = cv2.erode(mask,element)

    _,contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    secondBestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        x,y,w,h = cv2.boundingRect(bestContour)
        if currentArea > maximumArea:
            if (x+x+w >= (2*(y+y+h) - 50)) and ((x+x+w <= (2*(y+y+h) + 50))):
                secondBestContour = bestContour
                bestContour = contour
                maximumArea = currentArea
            else:
                table.putNumber("xValue",1000)
                table.putNumber("yValue",1000)
                print "NA"

    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
        #cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
        if counter == 0:
            xCentroidOne = (x+x+w)/2
            yCentroidOne = (y+y+h)/2
            counter = counter + 1
        elif counter == 1:
            xCentroidTwo = (x+x+w)/2
            yCentroidTwo = (y+y+h)/2
            counter = counter + 1
        elif counter == 2:
            xCentroidThree = (x+x+w)/2
            yCentroidThree = (y+y+h)/2
            counter = 0
        xCentroid = (xCentroidOne+xCentroidTwo+xCentroidThree)/3
        yCentroid = (yCentroidOne+yCentroidTwo+yCentroidThree)/3
        table.putNumber("xValue",xCentroid)
        print xCentroidOne

    #cv2.imshow('frame',frame)
    
    #cv2.imshow('mask',mask)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows() 
