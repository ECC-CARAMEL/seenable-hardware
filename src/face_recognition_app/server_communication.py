import base64
import requests
import time
import cv2

# サーバーに画像を送信する関数
def send_to_server(face_image, server_url):

    # 画像をbase64形式に変換
    _, buffer = cv2.imencode('.jpg', face_image)
    base64_face_image = base64.b64encode(buffer).decode('utf-8')

    try:
        # サーバーにリクエストを送信
        response = requests.post(server_url, json={"image": base64_face_image})
        response.raise_for_status() 
        response_data = response.json()
        name = response_data.get("name", "Unknown")
        
        # サーバーへのリクエストを送った後、一定の時間待機
        time.sleep(3)
        
        return name
    except requests.RequestException as e:
        print(f"Server request failed: {e}")
        return "Error"
