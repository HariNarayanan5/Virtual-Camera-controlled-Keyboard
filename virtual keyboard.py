import cv2
import mediapipe as mp

# Define the virtual keyboard keys
KEYS = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
        'Z', 'X', 'C', 'V', 'B', 'N', 'M']

# Function to check if a point is inside a rectangle
def is_inside(point, rect):
    x, y = point
    x1, y1, w, h = rect
    return x1 <= x <= x1 + w and y1 <= y <= y1 + h

# Function to check if the index finger is extended
def is_index_finger_extended(hand_landmarks):
    index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    index_finger_base = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP]
    return index_finger_tip.y < index_finger_base.y

# Main function
def main():
    cap = cv2.VideoCapture(0)  # Open webcam

    # Initialize Mediapipe hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    pressed_key = None  # Initialize pressed key to None

    while cap.isOpened():
        ret, frame = cap.read()  # Read frame from webcam
        if not ret:
            break

        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect hands
        results = hands.process(rgb_frame)

        # Draw virtual keyboard
        for i, key in enumerate(KEYS):
            x = 50 + (i % 10) * 60
            y = 50 + (i // 10) * 60
            cv2.rectangle(frame, (x, y), (x + 50, y + 50), (255, 255, 255), -1)
            cv2.putText(frame, key, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        # Check for hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                h, w, c = frame.shape
                ix, iy = int(index_finger.x * w), int(index_finger.y * h)

                # Check if the index finger is over a key and extended
                if is_index_finger_extended(hand_landmarks):
                    for key in KEYS:
                        key_x1 = 50 + (KEYS.index(key) % 10) * 60
                        key_y1 = 50 + (KEYS.index(key) // 10) * 60
                        key_x2 = key_x1 + 50
                        key_y2 = key_y1 + 50

                        if is_inside((ix, iy), (key_x1, key_y1, 50, 50)):
                            # Press the key if no key is currently being pressed
                            if pressed_key is None:
                                print(f"Pressed key: {key}")
                                pressed_key = key
                        else:
                            # Release the key if the hand moves away from it
                            if pressed_key == key:
                                print(f"Released key: {key}")
                                pressed_key = None

        # Display frame
        cv2.imshow('Virtual Keyboard', frame)

        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
