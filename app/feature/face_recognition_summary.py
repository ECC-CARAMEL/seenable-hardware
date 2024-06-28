import cv2
import face_recognition
import os

def load_training_images(train_img_directory, train_img_names):
    train_imgs = []
    for name in train_img_names:
        img_path = os.path.join(train_img_directory, name)
        if os.path.exists(img_path):
            train_imgs.append(face_recognition.load_image_file(img_path))
        else:
            print(f"ファイルが見つかりません: {img_path}")
    return train_imgs

def encode_faces(train_imgs):
    known_face_encodings = []
    known_face_labels = ["Known Person"]

    for img in train_imgs:
        locations = face_recognition.face_locations(img, model="hog")
        encodings = face_recognition.face_encodings(img, locations)
        known_face_encodings.extend(encodings)

    return known_face_encodings, known_face_labels

def recognize_faces(video_capture, known_face_encodings, known_face_labels, queue):
    while True:
        # フレームを取得
        ret, frame = video_capture.read()
        if not ret:
            break

        # フレームのサイズを縮小して処理速度を向上させる（オプション）
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # フレーム内の顔を検出する
        face_locations = face_recognition.face_locations(small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            name = "Unknown"

            # 学習データの顔とカメラの顔を比較する
            if known_face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.40)
                if True in matches:
                    # 一致する場合
                    best_match_index = matches.index(True)
                    name = known_face_labels[best_match_index]

            if name == "Unknown":
                top, right, bottom, left = [v * 4 for v in face_location]
                face_image = frame[top:bottom, left:right]
                queue.put("Unknown")  # ここで文字列を送信
            else:
                queue.put(name)  # 名前が特定できた場合も文字列を送信

            # 検出された顔に枠を描画する
            top, right, bottom, left = [v * 4 for v in face_location]  # 元のサイズに戻す
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # ラベルを描画する
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # フレームを表示する
        cv2.imshow('Video', frame)

        # 'q'キーを押すとループを終了する
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # キャプチャの解放とウィンドウの破棄
    video_capture.release()
    cv2.destroyAllWindows()
