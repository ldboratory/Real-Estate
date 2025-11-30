"""
영상 합성 (FFmpeg 사용)
"""
import subprocess
import os
from pathlib import Path


class VideoComposer:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def check_ffmpeg(self):
        """FFmpeg 설치 확인"""
        try:
            result = subprocess.run(['ffmpeg', '-version'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ FFmpeg가 설치되어 있습니다.")
                return True
        except FileNotFoundError:
            print("✗ FFmpeg가 설치되어 있지 않습니다.")
            print("설치 방법:")
            print("  macOS: brew install ffmpeg")
            print("  Ubuntu: sudo apt-get install ffmpeg")
            print("  Windows: https://ffmpeg.org/download.html")
            return False

    def combine_video_audio(self, video_file, audio_file, output_file='output/final_video.mp4'):
        """
        비디오와 오디오 합성

        Args:
            video_file: 비디오 파일 경로
            audio_file: 오디오 파일 경로
            output_file: 출력 파일 경로
        """
        if not self.check_ffmpeg():
            return None

        try:
            print(f"\n영상 합성 중...")
            print(f"비디오: {video_file}")
            print(f"오디오: {audio_file}")

            # FFmpeg 명령어
            cmd = [
                'ffmpeg',
                '-i', video_file,
                '-i', audio_file,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-strict', 'experimental',
                '-shortest',  # 짧은 쪽에 맞춤
                '-y',  # 덮어쓰기
                output_file
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✓ 영상 합성 완료: {output_file}")
                return output_file
            else:
                print(f"✗ 영상 합성 실패:")
                print(result.stderr)
                return None

        except Exception as e:
            print(f"영상 합성 중 오류: {e}")
            return None

    def add_background_music(self, video_file, bgm_file, output_file='output/final_with_bgm.mp4',
                           video_volume=1.0, bgm_volume=0.3):
        """
        비디오에 배경음악 추가

        Args:
            video_file: 비디오 파일 경로
            bgm_file: 배경음악 파일 경로
            output_file: 출력 파일 경로
            video_volume: 원본 오디오 볼륨
            bgm_volume: 배경음악 볼륨
        """
        if not self.check_ffmpeg():
            return None

        try:
            print(f"\n배경음악 추가 중...")

            # FFmpeg 명령어 (오디오 믹싱)
            cmd = [
                'ffmpeg',
                '-i', video_file,
                '-i', bgm_file,
                '-filter_complex',
                f'[0:a]volume={video_volume}[a1];[1:a]volume={bgm_volume}[a2];[a1][a2]amix=inputs=2:duration=shortest',
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-y',
                output_file
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✓ 배경음악 추가 완료: {output_file}")
                return output_file
            else:
                print(f"✗ 배경음악 추가 실패:")
                print(result.stderr)
                return None

        except Exception as e:
            print(f"배경음악 추가 중 오류: {e}")
            return None

    def create_shorts_video(self, video_file, audio_file, output_file='output/shorts_final.mp4',
                          bgm_file=None):
        """
        쇼츠용 최종 영상 생성

        Args:
            video_file: 비디오 파일
            audio_file: 내레이션 파일
            output_file: 출력 파일
            bgm_file: 배경음악 파일 (선택)
        """
        # 1단계: 비디오 + 내레이션 합성
        temp_file = os.path.join(self.output_dir, 'temp_with_narration.mp4')
        result = self.combine_video_audio(video_file, audio_file, temp_file)

        if not result:
            return None

        # 2단계: 배경음악 추가 (있으면)
        if bgm_file and os.path.exists(bgm_file):
            final_result = self.add_background_music(temp_file, bgm_file, output_file)
            # 임시 파일 삭제
            try:
                os.remove(temp_file)
            except:
                pass
            return final_result
        else:
            # 배경음악 없으면 temp 파일을 최종 파일로 이동
            try:
                os.rename(temp_file, output_file)
                print(f"✓ 최종 영상 생성 완료: {output_file}")
                return output_file
            except Exception as e:
                print(f"파일 이동 실패: {e}")
                return temp_file

    def convert_to_shorts_format(self, input_file, output_file='output/shorts_formatted.mp4',
                                width=1080, height=1920):
        """
        영상을 쇼츠 포맷으로 변환 (1080x1920)

        Args:
            input_file: 입력 파일
            output_file: 출력 파일
            width: 영상 너비
            height: 영상 높이
        """
        if not self.check_ffmpeg():
            return None

        try:
            print(f"\n쇼츠 포맷으로 변환 중...")

            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black',
                '-c:a', 'copy',
                '-y',
                output_file
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✓ 포맷 변환 완료: {output_file}")
                return output_file
            else:
                print(f"✗ 포맷 변환 실패:")
                print(result.stderr)
                return None

        except Exception as e:
            print(f"포맷 변환 중 오류: {e}")
            return None


if __name__ == "__main__":
    composer = VideoComposer()
    composer.check_ffmpeg()
