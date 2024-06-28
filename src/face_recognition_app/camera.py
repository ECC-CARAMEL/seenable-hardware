import cv2

# カメラを起動する関数
def capture_video():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        video_capture = cv2.VideoCapture(1)

    if not video_capture.isOpened():
        print("カメラが見つかりませんでした")
        exit()

    return video_capture
