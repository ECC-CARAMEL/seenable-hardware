import cv2

def initialize_camera():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        video_capture = cv2.VideoCapture(1)

    if not video_capture.isOpened():
        print("カメラが見つかりませんでした")
        exit()

    return video_capture
