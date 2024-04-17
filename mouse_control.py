import cv2
import mediapipe as mp
import pyautogui as pg

# Initialize mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

screen_width, screen_height=pg.size()

# Open cam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from webcam.")
        break

    # Flip dyal lframe
    frame = cv2.flip(frame, 1)

    # Convert man BGR L RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with mediapipe hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # akhd l2i7datiyat dyal no9at x:y 
            middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            
            height, width, _ = frame.shape

            middle_finger_x,middle_finger_y=int(middle_finger_mcp.x * width), int(middle_finger_mcp.y * height)

            tip_x, tip_y = int(index_finger_tip.x * width), int(index_finger_tip.y * height)
            thumb_x, thumb_y = int(thumb_tip.x * width), int(thumb_tip.y * height)

           # ta7wil dyal l2i7datiyat bach ijiw mazyan m3a x:y dyal pyautogui
            mouse_x=int(screen_width / width * middle_finger_x)
            mouse_y=int(screen_height / height * middle_finger_y)
            
            pg.moveTo(mouse_x, mouse_y)

            
            
            # Rasm dyal no9at
            cv2.circle(frame, (tip_x, tip_y), 8, (0, 255, 0), -1)
            cv2.circle(frame, (thumb_x, thumb_y), 8, (0, 255, 0), -1)

            if tip_x - thumb_x<2:
                # Rasm dyal no9at blhmar mali tclicki
                cv2.circle(frame, (tip_x, tip_y), 5, (0, 0, 255), -1)
                cv2.circle(frame, (thumb_x, thumb_y), 5, (0, 0, 255), -1)
                pg.click()
                



    # Display dyal frame
    cv2.imshow('Hand Tracking', frame)

    # wark 'q' bach ikhroj
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
