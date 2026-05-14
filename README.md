# 감성 챗봇 (Emotional Chatbot)

따뜻하게 위로해주는 AI 감성 챗봇입니다.
Raspberry Pi Zero 2W + Whisplay HAT 기반입니다.

## 하드웨어
- Raspberry Pi Zero 2W WH (핀 헤더 포함)
- PiSugar Whisplay HAT

## 설치 방법

### 1. 라즈비안 OS 설치
Raspberry Pi Imager로 SD카드에 Raspberry Pi OS Lite (64-bit) 설치
- SSH 활성화
- WiFi 설정
- 사용자: pi

### 2. SSH 접속
ssh pi@raspberrypi.local

### 3. 저장소 클론
git clone https://github.com/phdshinai/emotional-chatbot.git
cd emotional-chatbot

### 4. 설치
bash install.sh

### 5. API 키 입력
nano .env
GEMINI_API_KEY= 뒤에 키 입력 후 저장 (Ctrl+X → Y → Enter)

### 6. 재부팅
sudo reboot

### 7. 실행
cd ~/emotional-chatbot && bash run.sh

## API 키 발급
- Gemini: https://aistudio.google.com

## 사용법
- 버튼 길게 누르고 말하기
- 버튼 떼면 AI가 답변