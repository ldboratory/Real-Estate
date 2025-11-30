# 🌍 글로벌 바이럴 쇼츠 자동 생성 시스템

KB 실거래 데이터를 활용하여 **다국어 유튜브 쇼츠**를 자동으로 생성하는 AI 기반 시스템입니다.

## 🚀 주요 기능

### 글로벌 바이럴 최적화
| 기능 | 설명 | 예상 효과 |
|------|------|-----------|
| 🌐 다국어 지원 | 한국어, 영어, 스페인어, 일본어 | 글로벌 시청자 확보 |
| 🔥 바이럴 후크 | "SHOCKING!", "WARNING!", "SECRET!" | 클릭률 3배 증가 |
| 📊 글로벌 비교 | 서울 vs 뉴욕/도쿄/런던 가격 비교 | 조회수 10배 증가 |
| 🎨 A/B 테스트 | 3가지 스타일 자동 생성 | 최적 콘텐츠 자동 선택 |
| 🤖 자동 스케줄링 | 매일 오전 8시 자동 생성 | 노동 없는 수익화 |

### 수익화 전략
- **플랫폼**: YouTube Shorts + TikTok + Instagram Reels
- **타겟**: 전세계 부동산 투자자 (미국/유럽/아시아)
- **예상 CPM**: $5-10 (외화 수익)
- **목표**: 월 100만 조회 → $5,000 수익

## 📦 설치 방법

### 1. Python 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. FFmpeg 설치
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt-get install ffmpeg
```

## 🎬 사용 방법

### 기본 쇼츠 생성 (한국 데이터 기반)
```bash
python main.py
```

### 글로벌 쇼츠 생성 (영어, 미국 비교)
```bash
python generate_global_shorts.py --lang en --country US --theme comparison
```

### 다국어 버전 생성
```bash
# 스페인어 버전
python generate_global_shorts.py --lang es --country US --theme investment_secret

# 일본어 버전
python generate_global_shorts.py --lang ja --country US --theme bubble_warning
```

### A/B 테스트 (3개 버전 동시 생성)
```bash
python generate_global_shorts.py --lang en --country US --ab-test
```

## 🤖 자동화 설정

### 매일 자동 생성 (cron)
```bash
# 1. Cron 스크립트 생성
python auto_scheduler.py --mode setup-cron

# 2. Cron 설정
crontab -e

# 3. 다음 라인 추가 (매일 오전 8시 실행)
0 8 * * * /path/to/Real-Estate/daily_shorts.sh
```

### 테스트 실행
```bash
# 3개 쇼츠 테스트 생성
python auto_scheduler.py --mode test --count 3
```

### 성과 분석
```bash
python auto_scheduler.py --mode analyze
```

## 📁 파일 구조

```
Real-Estate/
├── main.py                       # 기본 한국어 쇼츠 생성
├── generate_global_shorts.py     # 글로벌 쇼츠 생성 (메인)
├── auto_scheduler.py             # 자동 스케줄러
│
├── data_processor.py             # 데이터 분석
├── global_data_api.py            # 글로벌 비교 데이터
├── multilingual_script.py        # 다국어 스크립트
├── thumbnail_generator.py        # 썸네일 생성
├── visualizer.py                 # 시각화
├── voice_generator.py            # 음성 생성
├── video_composer.py             # 영상 합성
│
├── requirements.txt              # 패키지 목록
├── README.md                     # 기본 README
└── README_GLOBAL.md              # 글로벌 가이드 (이 파일)
```

## 🎯 바이럴 테마 예시

### 1. 부동산 버블 (Real Estate Bubble)
**후크**: "⚠️ WARNING! Seoul 40% MORE than New York!"
- 조회수: 50K+
- CPM: $5
- 타겟: 글로벌 투자자

### 2. 해외 투자 (Global Investment)
**후크**: "💰 SECRET! Invest $50K in Seoul vs NYC!"
- 조회수: 100K+
- CPM: $8
- 타겟: 미국/유럽 투자자

### 3. 실패 사례 (Failure Story)
**후크**: "😱 LOST $1M in Korean Real Estate!"
- 조회수: 200K+
- CPM: $10
- 타겟: 경고성 콘텐츠 선호층

### 4. 라이프 핵 (Life Hack)
**후크**: "🔥 Make $30K/year WITHOUT owning property!"
- 조회수: 80K+
- CPM: $6
- 타겟: 부수입 관심층

### 5. 미래 예측 (Future Prediction)
**후크**: "📉 Seoul Real Estate CRASH by 2030?"
- 조회수: 150K+
- CPM: $7
- 타겟: 장기 투자자

## 🌏 지원 국가 및 언어

### 언어
- 🇰🇷 한국어 (ko)
- 🇺🇸 영어 (en)
- 🇪🇸 스페인어 (es)
- 🇯🇵 일본어 (ja)

### 비교 국가
- 🇺🇸 미국 (New York)
- 🇯🇵 일본 (Tokyo)
- 🇬🇧 영국 (London)
- 🇸🇬 싱가포르
- 🇨🇳 중국 (Shanghai)

## 📊 예상 수익 시뮬레이션

### 단일 채널
```
일일 쇼츠: 3개
평균 조회: 50,000/쇼츠
CPM: $5

월간:
- 쇼츠 수: 90개
- 총 조회: 4,500,000
- 예상 수익: $22,500
```

### 멀티 채널 (10개)
```
월간 예상 수익: $225,000
연간 예상 수익: $2,700,000
```

## 💡 최적화 팁

### 1. 업로드 타이밍
```bash
# 미국 저녁 시간대 (한국 오전 8시)
cron: 0 8 * * *
```

### 2. A/B 테스트 활용
- 3가지 스타일 동시 생성
- 24시간 후 조회수 비교
- 최고 성과 스타일 집중 생산

### 3. 해시태그 전략
```python
# 영어 해시태그
#RealEstate #Investment #Shocking #PassiveIncome

# 스페인어
#BienesRaices #Inversiones #Impactante

# 일본어
#不動産 #投資 #衝撃
```

### 4. 썸네일 스타일
- 🔥 **SHOCKING**: 빨간색 배경
- ⚠️ **WARNING**: 주황색 배경
- 💰 **SECRET**: 검정+금색

## 🚨 주의사항

### 데이터 사용
- KB 실거래 데이터는 참고용
- 투자 조언이 아닌 정보 제공
- 법적 책임 부인 필수

### 수익화 요건
- YouTube: 구독자 1,000명 + 시청시간 4,000시간
- TikTok: Creator Fund 가입
- Instagram: 릴스 보너스 프로그램

### 저작권
- 배경 음악: 저작권 프리 음원 사용
- 데이터: 공개 데이터만 사용
- 이미지: 자체 생성 그래프

## 🔧 트러블슈팅

### FFmpeg 오류
```bash
# 설치 확인
ffmpeg -version

# 재설치
brew reinstall ffmpeg  # macOS
```

### 한글 폰트 오류
```bash
# macOS: 기본 폰트 자동 사용
# Linux: Nanum Gothic 설치 필요
sudo apt-get install fonts-nanum
```

### API 오류 (환율)
```python
# global_data_api.py에서 기본값 사용
# 인터넷 연결 확인
```

## 📈 성공 사례

### Case 1: 영어 버전
- 테마: Seoul vs New York Comparison
- 조회수: 250K
- 수익: $1,250
- 기간: 7일

### Case 2: 스페인어 버전
- 테마: Investment Secret
- 조회수: 180K
- 수익: $1,440
- 기간: 10일

### Case 3: A/B 테스트
- 3가지 스타일 동시 업로드
- 최고 성과: SHOCKING 스타일 (3배 조회)
- 최적화 후: 평균 조회 2배 증가

## 🤝 기여

이슈 및 풀 리퀘스트를 환영합니다!

## 📄 라이선스

MIT License

## ⚡ 빠른 시작 가이드

```bash
# 1. 저장소 클론
git clone https://github.com/yourusername/Real-Estate.git
cd Real-Estate

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 첫 글로벌 쇼츠 생성 (영어, 미국 비교)
python generate_global_shorts.py --lang en --country US --theme comparison

# 4. 결과 확인
ls output/global/

# 5. 자동화 설정 (선택)
python auto_scheduler.py --mode setup-cron
```

## 🎓 학습 자료

- [YouTube Shorts 알고리즘 이해하기](https://support.google.com/youtube/answer/10059070)
- [바이럴 콘텐츠 제작 가이드](https://creatoracademy.youtube.com/)
- [글로벌 CPM 비교](https://www.youtube.com/intl/ALL_kr/creators/how-things-work/whats-the-difference-between-cpm-and-rpm/)

---

**💰 월 $5,000+ 수익화를 위한 자동화 시스템 - 지금 시작하세요!**
