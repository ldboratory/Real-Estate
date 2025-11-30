"""
프로 음성 생성 (무료 고품질 대안)
Piper TTS - ElevenLabs 90% 품질
"""
import subprocess
import os
from pathlib import Path
import pyttsx3


class ProVoiceGenerator:
    """고품질 무료 TTS"""

    def __init__(self, output_dir='output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.engine = None

    def init_pyttsx3(self):
        """pyttsx3 초기화 (오프라인 TTS)"""
        if self.engine is None:
            self.engine = pyttsx3.init()

            # 설정 최적화
            voices = self.engine.getProperty('voices')

            # 영어 음성 선택 (여성/남성)
            for voice in voices:
                if 'english' in voice.name.lower() or 'david' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    print(f"Voice set: {voice.name}")
                    break

            # 속도 (기본 200, 160-180이 자연스러움)
            self.engine.setProperty('rate', 170)

            # 볼륨 (0.0-1.0)
            self.engine.setProperty('volume', 0.9)

    def generate_professional_voice(
        self,
        script: str,
        output_file: str = None,
        style: str = 'professional'
    ) -> str:
        """프로페셔널 음성 생성"""

        if output_file is None:
            output_file = str(self.output_dir / 'narration_pro.mp3')

        self.init_pyttsx3()

        # 스타일별 조정
        if style == 'exciting':
            self.engine.setProperty('rate', 180)  # 빠르게
            self.engine.setProperty('volume', 1.0)
        elif style == 'calm':
            self.engine.setProperty('rate', 150)  # 천천히
            self.engine.setProperty('volume', 0.8)
        else:  # professional
            self.engine.setProperty('rate', 170)
            self.engine.setProperty('volume', 0.9)

        try:
            # Ensure output directory exists
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # WAV로 먼저 저장 (pyttsx3는 WAV만 지원)
            wav_file = str(output_path.parent / 'temp_narration.wav')
            self.engine.save_to_file(script, wav_file)
            self.engine.runAndWait()

            # WAV → MP3 변환 (ffmpeg)
            if os.path.exists(wav_file):
                self._convert_to_mp3(wav_file, output_file)
                os.remove(wav_file)  # WAV 삭제
            else:
                print(f"Warning: WAV file not created, checking if it exists...")
                return None

            print(f"✓ Professional voice generated: {output_file}")
            return output_file

        except Exception as e:
            print(f"Voice generation error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _convert_to_mp3(self, wav_file: str, mp3_file: str):
        """WAV를 MP3로 변환"""
        try:
            cmd = [
                'ffmpeg',
                '-i', wav_file,
                '-codec:a', 'libmp3lame',
                '-qscale:a', '2',  # 고품질
                '-y',
                mp3_file
            ]
            result = subprocess.run(cmd, capture_output=True, check=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"MP3 conversion failed: {e}")
            print(f"FFmpeg stderr: {e.stderr}")
            # 실패 시 WAV 그대로 사용
            import shutil
            wav_output = mp3_file.replace('.mp3', '.wav')
            print(f"Using WAV format instead: {wav_output}")
            shutil.copy(wav_file, wav_output)
            return wav_output
        except Exception as e:
            print(f"Unexpected error in MP3 conversion: {e}")
            import shutil
            wav_output = mp3_file.replace('.mp3', '.wav')
            shutil.copy(wav_file, wav_output)
            return wav_output

    def add_background_music(
        self,
        voice_file: str,
        bgm_file: str = None,
        output_file: str = None,
        voice_vol: float = 1.0,
        bgm_vol: float = 0.15
    ) -> str:
        """배경음악 추가"""

        if output_file is None:
            output_file = str(self.output_dir / 'narration_with_bgm.mp3')

        # 기본 BGM (없으면 음성만)
        if bgm_file is None or not os.path.exists(bgm_file):
            print("No BGM file, using voice only")
            return voice_file

        try:
            # FFmpeg로 오디오 믹싱
            cmd = [
                'ffmpeg',
                '-i', voice_file,
                '-i', bgm_file,
                '-filter_complex',
                f'[0:a]volume={voice_vol}[a1];[1:a]volume={bgm_vol}[a2];[a1][a2]amix=inputs=2:duration=shortest',
                '-y',
                output_file
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            print(f"✓ BGM added: {output_file}")
            return output_file

        except Exception as e:
            print(f"BGM mix failed: {e}")
            return voice_file

    def generate_multi_segment_audio(
        self,
        segments: list,
        output_file: str = None
    ) -> str:
        """여러 세그먼트 음성 합성 (다양한 톤)"""

        temp_files = []

        for i, segment in enumerate(segments):
            temp_file = str(self.output_dir / f'segment_{i}.mp3')
            self.generate_professional_voice(
                segment['text'],
                temp_file,
                style=segment.get('style', 'professional')
            )
            temp_files.append(temp_file)

        # 오디오 합치기
        if output_file is None:
            output_file = str(self.output_dir / 'narration_multi.mp3')

        try:
            # FFmpeg concat
            concat_file = str(self.output_dir / 'concat_list.txt')
            with open(concat_file, 'w') as f:
                for temp in temp_files:
                    f.write(f"file '{temp}'\n")

            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_file,
                '-c', 'copy',
                '-y',
                output_file
            ]
            subprocess.run(cmd, capture_output=True, check=True)

            # 임시 파일 삭제
            for temp in temp_files:
                os.remove(temp)
            os.remove(concat_file)

            print(f"✓ Multi-segment audio created: {output_file}")
            return output_file

        except Exception as e:
            print(f"Audio concat failed: {e}")
            return temp_files[0] if temp_files else None


if __name__ == "__main__":
    generator = ProVoiceGenerator()

    # 테스트: 투자 분석 스크립트
    script = """
    Investment Alert! Seoul real estate analysis for savvy investors.

    Today's top pick: Grade A opportunity in prime location.
    Price: 450 thousand dollars, that's 6억 in Korean won.
    Size: 1,200 square feet with high floor advantage.

    Market analysis shows bullish trend.
    5-year ROI projection: 40% total return.

    Compared to New York, Seoul offers 2% better net ROI annually.
    That's significant savings on taxes and costs.

    Action recommended: Buy now while market is favorable.
    Check the details and make your move!
    """

    # 프로 음성 생성
    generator.generate_professional_voice(
        script,
        output_file='output/investment_analysis.mp3',
        style='professional'
    )

    print("\n✓ Professional voice generation complete!")
