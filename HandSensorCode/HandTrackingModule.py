import cv2
import mediapipe as mp
import time



class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils
          
        self.landmark_drawing_spec = self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=5, circle_radius=5)  # Green dots
        self.connection_drawing_spec = self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)  # Blue lines



    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS, self.landmark_drawing_spec, self.connection_drawing_spec)



    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                h,w = img.shape
                cx, cy =  int(lm.x*w), int(lm.y*h)  # Position of Center
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 15, (255, 0 ,255), cv2.FILLED)
        return lmList





     




def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    hand_point_number = 4
    while True:
        success, img = cap.read()
        if not success:
            print("Image Capute Failed")
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if lmList !=0:
            print(lmList[hand_point_number])


        cv2.imshow("Image", img)
        cv2.waitKey(1) 



if __name__ == "__main__":
    main()

