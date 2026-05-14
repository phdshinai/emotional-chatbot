#!/bin/bash

echo "================================================"
echo "  감성 챗봇 설치 시작 (클린 라즈베리파이용)"
echo "================================================"

# 1. 시스템 패키지
echo ""
echo "[1/5] 시스템 패키지 설치 중..."
sudo apt update -y
sudo apt install -y \
    python3-pip \
    python3-pil \
    python3-numpy \
    python3-spidev \
    python3-libgpiod \
    portaudio19-dev \
    ffmpeg \
    git \
    wget

# 2. Python 라이브러리
echo ""
echo "[2/5] Python 라이브러리 설치 중..."
sudo python3 -m pip install --break-system-packages \
    pyaudio \
    python-dotenv \
    google-genai

# 3. Whisplay HAT 드라이버
echo ""
echo "[3/5] Whisplay HAT 드라이버 설치 중..."
cd ~
if [ ! -d "whisplay" ]; then
    git clone https://github.com/PiSugar/whisplay.git
fi
cd ~/whisplay/Driver
sudo bash install_wm8960_drive.sh
cd ~

# 4. 드라이버 경로 설정
echo ""
echo "[4/5] 드라이버 경로 설정 중..."
DRIVER_PATH="$HOME/whisplay/Driver"
if ! grep -q "whisplay/Driver" ~/.bashrc; then
    echo "export PYTHONPATH=\$PYTHONPATH:$DRIVER_PATH" >> ~/.bashrc
fi

# 5. .env 설정 안내
echo ""
echo "[5/5] 설정 파일 준비 중..."
cd ~/emotional-chatbot
if [ ! -f .env ]; then
    cp .env.template .env
    echo ""
    echo "⚠️  .env 파일에 API 키를 넣어주세요:"
    echo "    nano .env"
fi

echo ""
echo "================================================"
echo "  설치 완료!"
echo ""
echo "  다음 단계:"
echo "  1. nano .env  (API 키 입력)"
echo "  2. sudo reboot"
echo "  3. cd ~/emotional-chatbot && bash run.sh"
echo "================================================"