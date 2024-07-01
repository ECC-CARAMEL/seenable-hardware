# seenable-hardware

## 必要なハードウェア機器

### Raspberry Pi
https://www.switch-science.com/products/5680
### ディスプレイ
https://www.switch-science.com/products/9437
### カメラ
https://www.buffalo.jp/product/detail/bswhd06mgy.html

## Raspberry Pi

OSをインストールする
```
//Raspberry Pi OS (Other)を選択
//Raspberry Pi OS (Legacy,64-bit)
```

### pythonの仮想環境の構築(3.11.2)

https://zenn.dev/technicarium/articles/00b32d390e82ec

カメラとディスプレイのセットアップのためにRaspberry Piの設定を変更する
```
sudo raspi-config

//カメラのセットアップ
//Interface Optionsを選択
//Legacy Cameraを選択
//「Would you like to enable legacy camera suport?」で”はい”を選択
//”了解”を押して終了する

//ディスプレイのセットアップ
//Interface Optionsを選択
//SPIを選択
//「Would you like the SPI interface to be enabled?」で”はい”を選択

//ラズパイの再起動
sudo reboot
```

顔認証に必要なライブラリのインストール
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential cmake gfortran git wget curl graphicsmagick libgraphicsmagick1-dev libatlas-base-dev libavcodec-dev libavformat-dev libboost-all-dev libgtk2.0-dev libjpeg-dev liblapack-dev libswscale-dev pkg-config python3-dev python3-numpy python3-pip zip
```

## OpenCVのインストール
インストール時にメモリ不足を防ぐため、 一時的にスワップ領域を拡張する
```
sudo nano /etc/dphys-swapfile
< change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=1024 and save / exit nano >
sudo /etc/init.d/dphys-swapfile restart
```

OpenCVのインストール
```
pip3 install opencv-contrib-python opencv-python
```

## face_recognitionのインストール
```
pip3 install face_recognition
```

拡張したスワップ領域を戻す
```
sudo nano /etc/dphys-swapfile
< change CONF_SWAPSIZE=1024 to CONF_SWAPSIZE=100 and save / exit nano >
sudo /etc/init.d/dphys-swapfile restart
```
