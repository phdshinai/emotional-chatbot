#!/bin/bash

echo "=== 감성 챗봇 시작 ==="

# .env 파일 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없어요!"
    echo "cp .env.template .env 하고 API 키 넣어주세요."
    exit 1
fi

# whisplay-ai-chatbot 폴더로 .env 복사
cp .env whisplay-ai-chatbot/.env

# 챗봇 실행
cd whisplay-ai-chatbot
sudo env PATH=$PATH:/home/pi/.nvm/versions/node/v20.20.2/bin bash run_chatbot.sh