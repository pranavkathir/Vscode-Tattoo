import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands = 2, modelComplex=1, detectionConf = 0.5, trackConf = 0.5):

        #Initializing instance variables
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplex
        self.detectionConf = detectionConf
        self.trackConf = trackConf

        #setting up hands stuff for mediapipe
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionConf, self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4,8,12,16,20] #ids of the fingertips

    def findHands(self, img, draw = True): # Initializes the hand tracking
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Converts image so that cv2 can read it properly
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks: #If it sees a hand, and draw is true, it will draw landmarks on the hand
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNum=0, draw = True):
        xList = []
        yList = []
        #zList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum] #Defines which hand ur talking abt, within that hand it will put the landmarks in a list below

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy, cz = int(lm.x*w), int(lm.y*h), int(lm.z*1000)
                xList.append(cx)
                yList.append(cy)
                #zList.append(cz)
                self.lmList.append([id, cx, cy, cz]) #Adding landmark position to lmList
                if draw:
                     cv2.circle(img, (cx,cy), 5, (0, 215, 255), cv2.FILLED)
            xMin, xMax = min(xList), max(xList) # min and max vals of hand for bounding box
            yMin, yMax = min(yList), max(yList)
            bbox = xMin, yMin, xMax, yMax # Bounding box
            if (draw):
                cv2.rectangle(img, (bbox[0]-20, bbox[1]-20), (bbox[2]+20, bbox[3]+20), (0,255,0), 2) # Bounding box rectangle

        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        # Thumb
        if (self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]):
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range (1,5):
            if (self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]):
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def fingersLeft(self):
        fingers = []
        # Thumb
        if (self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]):
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range (1,5):
            if (self.lmList[self.tipIds[id]][1] > self.lmList[self.tipIds[id] - 2][1]):
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def fingersRight(self):
        fingers = []
        # Thumb
        if (self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]):
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range (1,5):
            if (self.lmList[self.tipIds[id]][1] < self.lmList[self.tipIds[id] - 2][1]):
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def isFist(self):
        fingers = self.fingersUp()
        if (not (fingers[1] and fingers[2] and fingers[3] and fingers[4])):
            return True
        return False

    def findDist(self, lm1, lm2):
        dist = math.sqrt(((self.lmList[lm2][1]-self.lmList[lm1][1])**2) + ((self.lmList[lm2][2]-self.lmList[lm1][2])**2))
        return dist


    def findDistance(self, p1, p2, img, draw=True):
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if (draw):
            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1,y1,x2,y2,cx,cy]



def main():
    prevTime = 0
    currTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()


    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        # if (len(lmList) != 0):
        #     print(lmList[4])

        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()