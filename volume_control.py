import cv2
import mediapipe as mp
import numpy as np
import os
import math 

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Open Webcam Feed (0 is usually the default built-in camera)
cap = cv2.VideoCapture(0)

# Exponential smoothing factor (alpha) and initial volume state
alpha = 0.7
smooth_vol = 50 

print("System running... Press 'q' in the video window to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # Convert the BGR image to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the 21 landmarks and connections on the hand
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates for Thumb tip (Landmark 4) and Index tip (Landmark 8)
            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]

            # Convert normalized coordinates (0.0 to 1.0) to pixel coordinates
            cx_thumb, cy_thumb = int(thumb.x * w), int(thumb.y * h)
            cx_index, cy_index = int(index.x * w), int(index.y * h)

            # Draw visual circles on the fingertips
            cv2.circle(frame, (cx_thumb, cy_thumb), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (cx_index, cy_index), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(frame, (cx_thumb, cy_thumb), (cx_index, cy_index), (0, 255, 0), 3)

            # Calculate Euclidean distance between the two tips
            distance = math.hypot(cx_index - cx_thumb, cy_index - cy_thumb)

            # --- NEW PINCH TO MUTE FEATURE ---
            # If fingers are practically touching (under 15 pixels), mute the system
            if distance < 15:
                smooth_vol = 0
                cv2.putText(frame, 'MUTED 🤫', (40, 100), 
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            else:
                # Map the pixel distance to Mac volume range (0 to 100)
                target_vol = np.interp(distance, [20, 200], [0, 100])
                
                # Apply Exponential Smoothing
                smooth_vol = (alpha * target_vol) + ((1 - alpha) * smooth_vol)
                smooth_vol = int(np.clip(smooth_vol, 0, 100))

            # Execute macOS native volume control command
            os.system(f"osascript -e 'set volume output volume {smooth_vol}'")

            # Display the volume percentage on the screen
            cv2.putText(frame, f'Volume: {smooth_vol}%', (40, 50), 
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            # Map the pixel distance to Mac volume range (0 to 100)
            # Adjust 20 (pinched) and 200 (spread) based on how close you sit to the camera
            target_vol = np.interp(distance, [20, 300], [0, 100])

            # Apply Exponential Smoothing: smooth = (alpha * target) + ((1 - alpha) * smooth)
            smooth_vol = (alpha * target_vol) + ((1 - alpha) * smooth_vol)
            smooth_vol = int(np.clip(smooth_vol, 0, 100))

            # Execute macOS native volume control command
            os.system(f"osascript -e 'set volume output volume {smooth_vol}'")

            # Display the volume percentage on the screen
            cv2.putText(frame, f'Volume: {smooth_vol}%', (40, 50), 
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    # Display the output window
    cv2.imshow('Gesture Volume Control', frame)

    # Break loop cleanly by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

