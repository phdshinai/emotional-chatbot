#!/bin/bash

echo "=== 감성 챗봇 설치 시작 ==="

# 1. 기본 패키지 설치
echo "[1/4] 패키지 설치 중..."
sudo apt update
sudo apt install -y python3-pip python3-pil python3-numpy python3-pygame portaudio19-dev git

# 2. Python 라이브러리 설치
echo "[2/4] Python 라이브러리 설치 중..."
sudo python3 -m pip install cairosvg --break-system-packages
sudo python3 -m pip install pyaudio --break-system-packages
sudo python3 -m pip install python-dotenv --break-system-packages
sudo python3 -m pip install google-generativeai --break-system-packages

# 3. Whisplay HAT 드라이버 설치
echo "[3/4] Whisplay HAT 드라이버 설치 중..."
cd ~
git clone https://github.com/PiSugar/whisplay.git
cd whisplay/Driver
sudo bash install_wm8960_drive.sh
cd ~

echo "[4/4] 완료!"
echo ""
echo "=== 설치 완료! ==="
echo "다음 명령어로 실행하세요:"
echo "cd emotional-chatbot && bash run.sh"