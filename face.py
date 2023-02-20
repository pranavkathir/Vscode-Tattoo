import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpFace = mp.solutions.face_mesh
face = mpFace.FaceMesh()
mpDraw = mp.solutions.drawing_utils
mpStyle = mp.solutions.drawing_styles

prevTime = 0
currTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face.process(imgRGB)
    h, w, c = img.shape
    # print(results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE])
    # print(type(results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE]))
    # time.sleep(1)
    print(results.face_landmarks)
    #mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)


    cv2.imshow("Image", img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()