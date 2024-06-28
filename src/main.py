import multiprocessing
from display import display
from face_recognition_app import capture_video, load_known_faces, recognize_faces, send_to_server

if __name__ == "__main__":
    queue = multiprocessing.Queue()

    # 設定
    train_img_directory = "学習させたい画像のディレクトリ"
    train_img_names = ["学習させたい画像.jpg"]
    server_url = 'サーバーのURL'

    # 学習データの読み込み
    known_face_encodings, known_face_labels = load_known_faces(train_img_directory, train_img_names)

    # カメラのキャプチャ
    video_capture = capture_video()

    # ディスプレイプロセスの起動
    p = multiprocessing.Process(target=display, args=(queue,))
    p.start()

    # 顔認識の実行
    recognize_faces(video_capture, known_face_encodings, known_face_labels, queue)

    p.join()
