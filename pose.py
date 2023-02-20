import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
mpStyle = mp.solutions.drawing_styles

prevTime = 0
currTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    h, w, c = img.shape
    # print(results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE])
    print(type(results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE]))
    # time.sleep(1)
    mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    #print(results.pose_landmarks)

    lms = []
    #for count, val in enumerate(results.pose_landmarks.landmark):
        #print(val, val.x, val.y)
  
    #lms.append(results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE].x * w)
    #lms.append(results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE].y * h)

    

    #for data_point in results.pose_landmarks.landmark:
        #print('x is', data_point.x, 'y is', data_point.y, 'z is', data_point.z, 'visibility is', data_point.visibility)
    
    # if (results.pose_landmarks):
        # lms = []
        # if (len(lms) > 2):
        #     lms.pop(0)
        #     lms.pop(1)
        # lms.append(results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE].x * w)
        # lms.append(results.pose_landmarks.landmark[mpPose.PoseLandmark.NOSE].y * h)
        

    #     print(lms)

    #     mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    # #print(results.multi_hand_landmarks)
    # if (results.pose_landmarks.landmark):
    #     for poseLms in results.pose_landmarks.landmark:
    #         for id, lm in enumerate(poseLms.landmark):
    #             #print(id,lm)
    #             h, w, c = img.shape
    #             cx, cy= int(lm.x*w), int(lm.y*h)
    #             # if id == 4:
    #             #     cv2.circle(img, (cx,cy), 20, (255,0,255), cv2.FILLED)

    #         mpDraw.draw_landmarks(img, poseLms, mpPose.POSE_CONNECTIONS)


    cv2.imshow("Image", img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()