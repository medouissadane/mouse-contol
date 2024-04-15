import cv2
import mediapipe as mp
import pyautogui as pg

# Initialize mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

screen_width, screen_height=pg.size()

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from webcam.")
        break

    # Flip the frame horizontally for a selfie view
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with mediapipe hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the coordinates of the tip of the index finger (landmark index 8)
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            
            height, width, _ = frame.shape
            tip_x, tip_y = int(index_finger_tip.x * width), int(index_finger_tip.y * height)
            thumb_x, thumb_y = int(thumb_tip.x * width), int(thumb_tip.y * height)
           
            mouse_x=int(screen_width / width * tip_x)
            mouse_y=int(screen_height / height * tip_y)
            
            pg.moveTo(mouse_x, mouse_y)
            print(tip_x-thumb_x)
            
            if tip_x - thumb_x<0:
                pg.click()


            # Draw a circle around the index finger tip
            cv2.circle(frame, (tip_x, tip_y), 8, (0, 255, 0), -1)
            cv2.circle(frame, (thumb_x, thumb_y), 8, (0, 255, 0), -1)

    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
