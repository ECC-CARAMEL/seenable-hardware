import cv2
import face_recognition
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from .server_communication import send_to_server

def load_training_images(train_img_directory, train_img_names):
    train_imgs = []
    for name in train_img_names:
        img_path = os.path.join(train_img_directory, name)
        if os.path.exists(img_path):
            train_imgs.append(face_recognition.load_image_file(img_path), name.split(".")[0])
        else:
            print(f"ファイルが見つかりません: {img_path}")
    return train_imgs

def encode_faces(train_imgs):
    known_face_encodings = []
    known_face_labels = []

    for img , label in train_imgs:
        locations = face_recognition.face_locations(img, model="hog")
        encodings = face_recognition.face_encodings(img, locations)
        known_face_encodings.extend(encodings)
        known_face_labels.extend([label] * len(encodings))

    return known_face_encodings, known_face_labels

def recognize_faces(video_capture, known_face_encodings, known_face_labels, queue, train_img_directory):
    proess_this_frame = True
    font_path = "/usr/share/fonts/truetype/note/NotoSansCJK-Regular.ttc"

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
                top, right, bottom, left = face_location
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                face_image = frame[top:bottom, left:right]

                #サーバーに画像を送信
                name_from_server = send_to_server(face_image, train_img_directory)
                if name_from_server:
                    name = os.path.splitext(name_from_server)[0]
                else:
                    name = "Unknown"

            # キューに名前を送信
            queue.put(name)

            # 検出された顔に枠を描画する
            top, right, bottom, left = [v * 4 for v in face_location]  # 元のサイズに戻す
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # フレームに名前を描画するためにPILを使用
            plil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(plil_image)
            font = ImageFont.truetype(font_path, 30)
            draw.text((left + 6, bottom - 35), name, font=font, fill=(255, 255, 255))
            frame = cv2.cvtColor(np.array(plil_image), cv2.COLOR_RGB2BGR)

        # フレームを表示する
        cv2.imshow('Video', frame)

        # 'q'キーを押すとループを終了する
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # キャプチャの解放とウィンドウの破棄
    video_capture.release()
    cv2.destroyAllWindows()
