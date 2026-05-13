# 감성 챗봇 (Emotional Chatbot)

따뜻하게 위로해주는 AI 감성 챗봇입니다.
Raspberry Pi Zero 2W + Whisplay HAT 기반으로 만들어졌어요.

## 하드웨어
- Raspberry Pi Zero 2W
- PiSugar Whisplay HAT

## 설치 방법

### 1. 저장소 클론
git clone https://github.com/phdshinai/emotional-chatbot.git
cd emotional-chatbot

### 2. 환경변수 설정
cp .env.template .env
nano .env
# API 키 입력

### 3. 설치 및 실행
bash install.sh

## API 키 발급
- Gemini: aistudio.google.com
- Anthropic: console.anthropic.com
- OpenAI: platform.openai.com