import math

import cv2
import time
import HandTrackingModule as htm
import cvzone
import numpy as np
import imutils
import TattooSelection as tats

#####################################################
wCam, hCam = 640, 480 #Cam width and height
#####################################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)                   #Setting up capture stuff
cap.set(4, hCam)
success, img = cap.read() 

selection = tats.tatSelection()         # TattooSelection class for choosing tattoo
path, size, rot = selection.getPath()   # Getting path, size, and rotation adjustment for the chosen tattoo

imgFront = cv2.imread(path, cv2.IMREAD_UNCHANGED) #600x530

detector = htm.handDetector(detectionConf=0.7, maxHands=1)

while (True and (path != "end")): # if path is "end" it means the user pressed 'q' to end the program, so skip the loop
    success, img = cap.read()

    # Find Hand
    img = detector.findHands(img, draw=False)
    imgResult = img                                             #Setting up mediapipe module stuff
    lmList, bbox = detector.findPosition(img, draw=False)

    if (len(lmList) != 0): # Only run if there is a hand

        if (not detector.isFist()): # Only run your hand is not a fist

            x2, y2 = lmList[0][1], lmList[0][2]  # bottom of hand

            if (lmList[19][1] < lmList[6][1]):
                x1, y1 = lmList[17][1], lmList[17][2]     # Calculations for middle of hand, changes depending on if hand is front or back facing
            else:
                x1, y1 = lmList[5][1], lmList[5][2]

            scaleDist = detector.findDist(12,0) # Using findDist to find distance between top of middle finger and bottom of palm.
            scaling = np.interp(scaleDist, [100, 370], size)   # Scale factor calculation
            scaledTat = cv2.resize(imgFront, (0,0), None, scaling, scaling) # Actually resizing the tattoo

            tatH = scaledTat.shape[0]    # Height and width of the scaled tattoo - changes constantly bc the tattoo size changes constantly
            tatW = scaledTat.shape[1]

            center = [abs((lmList[9][1] + lmList[0][1])//2), abs((lmList[9][2] + lmList[0][2])//2)] # center of hand calculation

            if y1-y2!=0:
                angle = (math.atan((x2 - x1) / (y1 - y2))) * (180 / math.pi) # angle of hand calculation

            adjX = int((center[0] - (tatW / 2))) # Adjusting x and y in order to make the image overlay properly in the middle of the hand
            adjY = int((center[1] - (tatH / 2)))

            if (adjX >= 5 and adjX <= (635-tatW) and adjY >= 10 and adjY <= (475-tatH)): # checks if the entire tattoo can fit on the screen before displaying it
                 imgResult = cvzone.overlayPNG(img, (imutils.rotate(scaledTat, -angle+rot)), (adjX, adjY)) # overlaying the rotated and scaled tattoo on the adjusted x and y points
                 #imgResult = cvzone.overlayPNG(img, (imutils.rotate_bound(scaledTat, angle-rot)), (adjX, adjY))

    cv2.imshow("Image", imgResult) #displaying camera stream
    k = cv2.waitKey(1)
    if (k == ord('q')): # if q is pressed, end program
        break

cap.release()
cv2.destroyAllWindows()