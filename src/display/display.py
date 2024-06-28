import time
import logging
import multiprocessing
import spidev as SPI
from PIL import Image, ImageDraw, ImageFont
from lib import LCD_1inch5

def display(queue):
    logging.basicConfig(level=logging.DEBUG)
    try:
        # ディスプレイの初期化
        disp = LCD_1inch5.LCD_1inch5()
        disp.Init()
        disp.clear()

        # 描画用の空白の画像を作成
        image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)
        disp.ShowImage(image1)

        logging.info("draw text")
        Font1 = ImageFont.truetype("NotoSansCJK-Regular.ttc", 25)

        while True:
            # キューから値を取得
            if not queue.empty():
                value = queue.get()

                # 画像をクリアして新しいテキストを描画
                draw.rectangle((0, 0, disp.width, disp.height), fill="WHITE")
                draw.text((15, 180), str(value), fill="BLACK", font=Font1)  # str(value)で文字列として扱う
                image1_rotated = image1.rotate(90)
                disp.ShowImage(image1_rotated)

            time.sleep(1)

    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        disp.module_exit()
        logging.info("quit:")
        exit()
