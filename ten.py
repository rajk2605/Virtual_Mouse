import cv2
import mediapipe as mp
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

# Initialize volume control variables
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_control = cast(interface, POINTER(IAudioEndpointVolume))

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:  # Index finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    pyautogui.moveTo(index_x, index_y)

                if id == 4:  # Thumb finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                if id == 12:  # Middle finger tip for volume control
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    # Calculate the volume based on the position of the middle finger tip
                    normalized_volume = (thumb_y - y) / screen_height
                    normalized_volume = max(0, min(1, normalized_volume))
                    volume_control.SetMasterVolumeLevelScalar(normalized_volume, None)

                if id == 16:  # Ring finger tip for right-click
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    ring_x = screen_width / frame_width * x
                    ring_y = screen_height / frame_height * y

            # Click Functionality
            if abs(index_y - thumb_y) < 20:
                pyautogui.click()

            # Right-Click Functionality
            right_click_distance = math.dist((ring_x, ring_y), (thumb_x, thumb_y))
            if right_click_distance < 20:
                pyautogui.rightClick()

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)




