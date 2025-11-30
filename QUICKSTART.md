# ⚡ 빠른 시작 가이드

## 5분 안에 첫 글로벌 쇼츠 만들기!

### 1단계: 기본 한국어 쇼츠 생성 (테스트)
```bash
# 기존 광진구 데이터로 한국어 쇼츠 생성
python main.py
```
**출력**: `output/shorts_1080x1920.mp4`

---

### 2단계: 글로벌 영어 쇼츠 생성
```bash
# 서울 vs 뉴욕 비교 (영어)
python generate_global_shorts.py --lang en --country US --theme comparison
```
**출력**: `output/global/en_US_comparison_*_final.mp4`

---

### 3단계: 다양한 버전 생성

#### 스페인어 버전 (미국 시장)
```bash
python generate_global_shorts.py --lang es --country US --theme investment_secret
```

#### 일본어 버전
```bash
python generate_global_shorts.py --lang ja --country US --theme bubble_warning
```

#### A/B 테스트 (3개 동시 생성)
```bash
python generate_global_shorts.py --lang en --country US --ab-test
```

---

### 4단계: 자동화 설정 (선택사항)

#### 성과 분석
```bash
python auto_scheduler.py --mode analyze
```

**출력 예시**:
```
월간 예상:
  - 쇼츠 수: 90개
  - 총 조회수: 4,500,000
  - 예상 수익: $22,500
  - 채널 10개 운영 시: $225,000
```

#### Cron 자동화 설정
```bash
# 1. Cron 스크립트 생성
python auto_scheduler.py --mode setup-cron

# 2. Cron 편집
crontab -e

# 3. 매일 오전 8시 자동 실행 추가
0 8 * * * /Users/dongbin/Projects/Real-Estate/daily_shorts.sh
```

---

## 📊 주요 명령어 비교

| 목적 | 명령어 | 언어 | 시간 |
|------|--------|------|------|
| 기본 테스트 | `python main.py` | 한국어 | 2분 |
| 영어 쇼츠 | `python generate_global_shorts.py --lang en --country US` | 영어 | 3분 |
| A/B 테스트 | `python generate_global_shorts.py --ab-test` | 선택 | 9분 |
| 자동 생성 (3개) | `python auto_scheduler.py --mode daily --count 3` | 랜덤 | 9분 |

---

## 🎯 테마 선택 가이드

### `--theme comparison` (가격 비교)
- **후크**: "Seoul $450K vs New York $750K!"
- **타겟**: 투자 비교 관심층
- **예상 조회**: 50K+

### `--theme bubble_warning` (버블 경고)
- **후크**: "⚠️ WARNING! Seoul 40% OVERHEATED!"
- **타겟**: 리스크 관리 투자자
- **예상 조회**: 100K+

### `--theme investment_secret` (투자 비밀)
- **후크**: "💰 SECRET! Make $10K/year!"
- **타겟**: 부수입 관심층
- **예상 조회**: 80K+

---

## 🌍 국가 선택 가이드

| 국가 코드 | 도시 | 평균 가격 | 비교 효과 |
|-----------|------|-----------|-----------|
| `US` | 뉴욕 | $750K | ⭐⭐⭐⭐⭐ 최고 |
| `JP` | 도쿄 | $500K | ⭐⭐⭐⭐ 높음 |
| `UK` | 런던 | $650K | ⭐⭐⭐⭐ 높음 |
| `SG` | 싱가포르 | $1.2M | ⭐⭐⭐⭐⭐ 최고 |
| `CN` | 상하이 | $450K | ⭐⭐⭐ 중간 |

---

## 🔥 바이럴 팁

### 제목 작성 공식
```
[이모지] [감탄사]! [핵심 메시지] [숫자]%!

예시:
🔥 SHOCKING! Seoul 40% CHEAPER than NYC!
⚠️ WARNING! Korean Real Estate Bubble!
💰 SECRET! Invest in Seoul vs Tokyo - Save 20%!
```

### 해시태그 전략
```python
# 필수 해시태그 (모든 영상)
#Shorts #RealEstate #Investment

# 영어권
#PassiveIncome #WealthBuilding #FIRE

# 스페인어권
#Inversiones #DineroExtra #LibertadFinanciera

# 일본어권
#投資 #不動産 #資産運用
```

### 업로드 최적 시간
```
미국 동부 시간 18:00-22:00 (저녁 시간대)
= 한국 시간 08:00-12:00 (오전)

→ Cron 설정: 0 8 * * *
```

---

## 🚀 수익화 로드맵

### Phase 1: 테스트 (1-7일)
- 영어 쇼츠 5개 생성
- A/B 테스트로 최적 스타일 파악
- 조회수 분석

### Phase 2: 확장 (8-30일)
- 일일 3개 자동 생성 (Cron)
- 다국어 확장 (스페인어, 일본어)
- 멀티 플랫폼 (YouTube + TikTok)

### Phase 3: 스케일링 (31-90일)
- 채널 10개 동시 운영
- A/B 테스트 결과 기반 최적화
- 월 $5,000+ 수익 달성

---

## ⚠️ 자주 묻는 질문

### Q: FFmpeg 오류가 발생합니다
```bash
# FFmpeg 재설치
brew reinstall ffmpeg  # macOS
sudo apt-get install --reinstall ffmpeg  # Linux
```

### Q: 한글 폰트가 깨집니다
- macOS: 자동으로 AppleGothic 사용
- Linux: `sudo apt-get install fonts-nanum`

### Q: 환율 API가 작동하지 않습니다
- 기본값(2024년 기준)이 자동으로 사용됨
- 인터넷 연결 확인

### Q: 음성이 이상합니다
- gTTS는 무료이지만 품질 제한
- 업그레이드: ElevenLabs API 사용 (유료)

---

## 📈 다음 단계

1. **품질 개선**:
   - ElevenLabs API로 자연스러운 음성
   - Canva API로 전문 썸네일

2. **자동 업로드**:
   - YouTube API 연동
   - TikTok API 연동

3. **분석 대시보드**:
   - 조회수/수익 실시간 추적
   - A/B 테스트 결과 자동 분석

---

**지금 바로 첫 쇼츠를 만들어보세요!** 🚀
```bash
python generate_global_shorts.py --lang en --country US --theme comparison
```
