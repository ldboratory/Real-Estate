#!/usr/bin/env python3
"""
부동산 실거래 쇼츠 영상 자동 생성 메인 스크립트

사용법:
    python main.py

단계:
    1. 데이터 로드 및 분석 (Pandas)
    2. 시각화 생성 (Matplotlib)
    3. 음성 내레이션 생성 (gTTS)
    4. 영상 합성 (FFmpeg)
    5. 최종 쇼츠 영상 출력
"""

import os
import sys
from pathlib import Path

from data_processor import RealEstateDataProcessor
from visualizer import RealEstateVisualizer
from voice_generator import VoiceGenerator
from video_composer import VideoComposer


def main():
    print("=" * 60)
    print("부동산 실거래 쇼츠 영상 자동 생성 시스템")
    print("=" * 60)

    # 설정
    base_dir = Path(__file__).parent

    # xlsx 파일 자동 찾기
    xlsx_files = list(base_dir.glob("*.xlsx"))
    if not xlsx_files:
        print("오류: 디렉터리에 xlsx 파일이 없습니다.")
        return

    excel_file = str(xlsx_files[0])
    print(f"발견된 데이터 파일: {xlsx_files[0].name}")

    output_dir = base_dir / "output"
    os.makedirs(output_dir, exist_ok=True)

    # 1단계: 데이터 처리
    print("\n[1/5] 데이터 로드 및 분석")
    print("-" * 60)
    processor = RealEstateDataProcessor(excel_file)

    try:
        processor.load_data()
        processor.analyze_data()
        processor.clean_data()
        hot_deals = processor.find_hot_deals(top_n=3, max_price=600000000)
        trend_data = processor.calculate_price_trend()
        script = processor.generate_script()

        if hot_deals is None or len(hot_deals) == 0:
            print("핫딜 데이터가 없습니다. 프로그램을 종료합니다.")
            return

    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return

    # 2단계: 시각화 생성
    print("\n[2/5] 시각화 그래프 생성")
    print("-" * 60)
    visualizer = RealEstateVisualizer(str(output_dir))

    try:
        # 가격 추이 애니메이션
        if trend_data is not None and len(trend_data) > 0:
            video_file = visualizer.create_price_trend_animation(
                trend_data,
                output_file=str(output_dir / 'price_trend.mp4'),
                duration=15
            )
        else:
            print("가격 추이 데이터가 없어 핫딜 차트만 생성합니다.")
            # 핫딜 차트를 이미지로 저장
            chart_file = visualizer.create_hot_deals_chart(
                hot_deals,
                output_file=str(output_dir / 'hot_deals.png')
            )
            # 이미지를 비디오로 변환 (15초)
            video_file = convert_image_to_video(chart_file, str(output_dir / 'price_trend.mp4'))

    except Exception as e:
        print(f"시각화 생성 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return

    # 3단계: 음성 내레이션 생성
    print("\n[3/5] 음성 내레이션 생성")
    print("-" * 60)
    voice_gen = VoiceGenerator(str(output_dir))

    try:
        audio_file = voice_gen.generate_narration(
            script,
            output_file=str(output_dir / 'narration.mp3')
        )

        if audio_file is None:
            print("음성 생성에 실패했습니다. 프로그램을 종료합니다.")
            return

    except Exception as e:
        print(f"음성 생성 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return

    # 4단계: 영상 합성
    print("\n[4/5] 영상 합성")
    print("-" * 60)
    composer = VideoComposer(str(output_dir))

    if not composer.check_ffmpeg():
        print("\nFFmpeg가 설치되어 있지 않습니다.")
        print("영상 합성을 건너뛰고 개별 파일만 생성합니다.")
        print(f"\n생성된 파일:")
        print(f"  - 비디오: {video_file}")
        print(f"  - 오디오: {audio_file}")
        return

    try:
        final_video = composer.create_shorts_video(
            video_file,
            audio_file,
            output_file=str(output_dir / 'shorts_final.mp4')
        )

        if final_video:
            # 5단계: 쇼츠 포맷으로 변환
            print("\n[5/5] 쇼츠 포맷 변환 (1080x1920)")
            print("-" * 60)
            shorts_video = composer.convert_to_shorts_format(
                final_video,
                output_file=str(output_dir / 'shorts_1080x1920.mp4'),
                width=1080,
                height=1920
            )

            if shorts_video:
                print("\n" + "=" * 60)
                print("✓ 쇼츠 영상 생성 완료!")
                print("=" * 60)
                print(f"\n최종 파일: {shorts_video}")
                print(f"\n이 영상을 유튜브 쇼츠에 업로드할 수 있습니다!")
            else:
                print(f"\n포맷 변환은 실패했지만, 기본 영상은 생성되었습니다: {final_video}")
        else:
            print("\n영상 합성에 실패했습니다.")

    except Exception as e:
        print(f"영상 합성 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return


def convert_image_to_video(image_file, output_file, duration=15):
    """이미지를 비디오로 변환 (FFmpeg 사용)"""
    try:
        import subprocess
        cmd = [
            'ffmpeg',
            '-loop', '1',
            '-i', image_file,
            '-c:v', 'libx264',
            '-t', str(duration),
            '-pix_fmt', 'yuv420p',
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black',
            '-y',
            output_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ 이미지를 비디오로 변환 완료: {output_file}")
            return output_file
        else:
            print(f"이미지 변환 실패: {result.stderr}")
            return None
    except Exception as e:
        print(f"이미지 변환 중 오류: {e}")
        return None


if __name__ == "__main__":
    main()
