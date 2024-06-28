# main.py

import multiprocessing
from app.feature.camera import initialize_camera
from app.feature.face_recognition_summary import load_training_images, encode_faces, recognize_faces
from app.feature.display import display

if __name__ == "__main__":
    train_img_directory = "学習させたい画像のディレクトリ"
    train_img_names = ["学習させたい画像"]

    # 学習データの顔画像を読み込む
    train_imgs = load_training_images(train_img_directory, train_img_names)
    # 学習データの顔画像から特徴量を抽出する
    known_face_encodings, known_face_labels = encode_faces(train_imgs)
    # カメラを初期化する
    video_capture = initialize_camera()

    # プロセスとキューを作成
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=display, args=(queue,))
    p.start()

    # 顔認識を開始する
    recognize_faces(video_capture, known_face_encodings, known_face_labels, queue)

    # プロセスの終了を待機
    p.join()
