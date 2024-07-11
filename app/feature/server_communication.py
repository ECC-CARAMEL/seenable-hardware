import base64
import requests
import time
import cv2
import os

def send_to_server(face_image, train_img_directory):
    try:
        # 画像をbase64形式に変換
        _, buffer = cv2.imencode('.jpg', face_image)
        base64_face_image = base64.b64encode(buffer).decode('utf-8')

        # サーバーにリクエストを送信    
        response = requests.post('サーバーのURL', json={"image": base64_face_image})
        response.raise_for_status()  # HTTPエラーチェック
        print(response.status_code)
        response_data = response.json()
        name = response_data.get("name")

        # 画像をローカルに保存する
        save_path = os.path.join(train_img_directory, f"{name}.jpg")
        with open(save_path, "wb") as f:
            f.write(buffer)
        
    except requests.RequestException as e:
        print(f"Server request failed: {e}")
        name = "Error"

    # サーバーへのリクエストを送った後、一定の時間待機(必要に応じて調整)
    time.sleep(3)  # 3秒待機（必要に応じて調整）

    return name