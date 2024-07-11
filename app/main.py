import sys
from feature.camera import initialize_camera
from feature.display import display_process
from feature.face_recognition_summary import load_training_images, encode_faces, recognize_faces
from multiprocessing import Process, Queue

if __name__ == "__main__":
    queue = Queue()
    display_proc = Process(target=display_process, args=(queue,))
    display_proc.start()

    # 学習データの読み込みとエンコード
    train_img_directory = "学習させたい画像のディレクトリ"
    train_img_names = ["学習させたい画像"]
    train_imgs = load_training_images(train_img_directory, train_img_names)
    known_face_encodings, known_face_labels = encode_faces(train_imgs)

    # カメラの初期化
    video_capture = initialize_camera()

    # 顔認識の実行
    recognize_faces(video_capture, known_face_encodings, known_face_labels, queue, train_img_directory)

    display_proc.join()