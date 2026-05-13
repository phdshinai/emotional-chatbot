#!/bin/bash

echo "=== 감성 챗봇 시작 ==="

# .env 파일 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없어요!"
    echo "cp .env.template .env 하고 API 키 넣어주세요."
    exit 1
fi

# 드라이버 경로 확인
if [ ! -f ~/whisplay/Driver/WhisPlay.py ]; then
    echo "❌ Whisplay 드라이버가 없어요!"
    echo "bash install.sh 먼저 실행하세요."
    exit 1
fi

# 실행
sudo python3 main.py