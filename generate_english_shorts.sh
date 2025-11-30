#!/bin/bash

# 영어 쇼츠 자동 생성 스크립트
# English-only shorts generation (no character encoding issues)

echo "🎬 Generating English Real Estate Shorts..."
echo "==========================================="

# 기본 한국어 데이터 기반 영어 쇼츠 생성
python main.py

echo ""
echo "✅ English shorts generated!"
echo "Output: output/shorts_1080x1920.mp4"
echo ""
echo "📊 Script: Today's Seoul real estate hot deals!"
echo "🎨 Chart: English labels (no Korean characters)"
echo "🔊 Voice: English narration"
echo ""
echo "Ready to upload to YouTube Shorts!"
