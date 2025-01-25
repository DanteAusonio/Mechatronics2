import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

landmark_drawing_spec = mp_draw.DrawingSpec(color=(0, 255, 0), thickness=5, circle_radius=5)  # Green dots
connection_drawing_spec = mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)  # Blue lines



while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    thumb_x = 0
    thumb_y = 0

    pointer_x = 0
    pointer_y = 0

    line_length = 0

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS, landmark_drawing_spec, connection_drawing_spec)
            for id, lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx, cy =  int(lm.x*w), int(lm.y*h)  # Position of Center
                if id == 4:
                    thumb_x = cx
                    thumb_y = cy
                    print(f"Thumb Location: x: {cx}, y:{cy}")
                if id == 8:
                    pointer_x = cx
                    pointer_y = cy
                    print(f"Pointer LocationL x: {cx}, y:{cy}")
                delta_y = abs(thumb_y - pointer_y)
                delta_x = abs(thumb_x - pointer_x)
                line_length = ((delta_y ** 2) + (delta_x ** 2)) ** 0.5
                # Normalization:
                line_length = round(line_length, -1) - 40

    line = cv2.line(img, (thumb_x, thumb_y), (pointer_x, pointer_y), (255,0,0), 10)

    label = f"{line_length:.2f}"  # Format to 2 decimal places
    mid_x = (thumb_x + pointer_x) // 2
    mid_y = (thumb_y + pointer_y) // 2
    cv2.putText(img, label, (mid_x, mid_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1) 