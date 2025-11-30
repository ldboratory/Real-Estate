# 부동산 실거래 쇼츠 영상 자동 생성 시스템

KB 실거래 데이터를 분석하여 유튜브 쇼츠용 부동산 영상을 자동으로 생성하는 프로그램입니다.

## 주요 기능

| 단계 | 도구/코드 | 입력 | 출력 |
|------|-----------|------|------|
| 1. 데이터 | Pandas | KB실거래 XLSX | "광진구 래미안 5.7억 +2%" |
| 2. 시각화 | Matplotlib | 가격 추이 | 15초 애니메이션 그래프 |
| 3. 음성 | gTTS | "오늘 핫딜: 자양동 래미안" | MP3 내레이션 |
| 4. 영상 | FFmpeg | 그래프+음성 | 1080x1920 쇼츠 MP4 |

## 설치 방법

### 1. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. FFmpeg 설치

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows:**
- https://ffmpeg.org/download.html 에서 다운로드
- 환경 변수에 추가

## 사용 방법

### 1. 데이터 준비

KB 부동산 또는 공공데이터포털에서 실거래 데이터를 다운로드하여 프로젝트 폴더에 저장합니다.

현재 지원 파일:
- `광진구_20251130215706.xlsx`

### 2. 프로그램 실행

```bash
python main.py
```

### 3. 결과 확인

`output/` 폴더에 다음 파일들이 생성됩니다:

- `price_trend.mp4` - 가격 추이 애니메이션
- `hot_deals.png` - 핫딜 차트
- `narration.mp3` - 음성 내레이션
- `shorts_final.mp4` - 영상+음성 합성
- `shorts_1080x1920.mp4` - 최종 쇼츠 영상 (1080x1920)

### 4. 유튜브 업로드

`shorts_1080x1920.mp4` 파일을 유튜브 쇼츠에 업로드합니다.

## 파일 구조

```
Real-Estate/
├── main.py                    # 메인 실행 스크립트
├── data_processor.py          # 데이터 분석 및 전처리
├── visualizer.py              # 시각화 (Matplotlib)
├── voice_generator.py         # 음성 생성 (gTTS)
├── video_composer.py          # 영상 합성 (FFmpeg)
├── requirements.txt           # Python 패키지 목록
├── README.md                  # 프로젝트 설명서
├── 광진구_20251130215706.xlsx # 실거래 데이터
└── output/                    # 생성된 파일 출력 폴더
    ├── price_trend.mp4
    ├── narration.mp3
    └── shorts_1080x1920.mp4
```

## 개별 모듈 테스트

각 모듈을 개별적으로 테스트할 수 있습니다:

```bash
# 데이터 처리 테스트
python data_processor.py

# 시각화 테스트
python visualizer.py

# 음성 생성 테스트
python voice_generator.py

# 영상 합성 테스트
python video_composer.py
```

## 커스터마이징

### 데이터 파일 변경

`main.py`에서 파일명 수정:
```python
excel_file = "your_file.xlsx"
```

### 핫딜 기준 변경

`main.py`에서 가격 기준 수정:
```python
hot_deals = processor.find_hot_deals(
    top_n=3,              # 상위 3개
    max_price=600000000   # 6억 이하
)
```

### 영상 길이 조절

`main.py`에서 duration 수정:
```python
video_file = visualizer.create_price_trend_animation(
    trend_data,
    duration=15  # 초 단위
)
```

### 음성 속도 조절

`voice_generator.py`에서 slow 파라미터 수정:
```python
tts = gTTS(text=script, lang='ko', slow=False)  # True로 변경 시 느리게
```

## 문제 해결

### FFmpeg 오류

```bash
# FFmpeg 설치 확인
ffmpeg -version

# 설치 경로 확인
which ffmpeg  # macOS/Linux
where ffmpeg  # Windows
```

### 한글 폰트 오류

시스템에 한글 폰트가 설치되어 있는지 확인:
- macOS: 기본 폰트 사용
- Windows: 맑은 고딕
- Linux: Nanum Gothic 설치 필요

### 메모리 부족

대용량 데이터 처리 시 메모리 부족이 발생할 수 있습니다:
```python
# data_processor.py에서 샘플링
self.df = self.df.sample(n=1000)  # 1000개만 샘플링
```

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트를 환영합니다!
