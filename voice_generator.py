"""
음성 내레이션 생성 (gTTS)
"""
from gtts import gTTS
import os


class VoiceGenerator:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_narration(self, script, output_file='output/narration.mp3', lang='ko'):
        """
        텍스트를 음성으로 변환

        Args:
            script: 읽을 텍스트
            output_file: 출력 파일 경로
            lang: 언어 (ko, en, etc.)
        """
        try:
            print(f"음성 생성 중...")
            print(f"스크립트: {script}")

            # gTTS로 음성 생성
            tts = gTTS(text=script, lang=lang, slow=False)
            tts.save(output_file)

            print(f"음성 파일 저장 완료: {output_file}")
            return output_file

        except Exception as e:
            print(f"음성 생성 실패: {e}")
            return None

    def generate_intro(self, output_file='output/intro.mp3'):
        """인트로 음성"""
        intro_text = "광진구 부동산 핫딜을 소개합니다!"
        return self.generate_narration(intro_text, output_file)

    def generate_outro(self, output_file='output/outro.mp3'):
        """아웃트로 음성"""
        outro_text = "지금 바로 확인해보세요! 구독과 좋아요 부탁드립니다!"
        return self.generate_narration(outro_text, output_file)


if __name__ == "__main__":
    # 테스트
    vg = VoiceGenerator()
    script = "오늘의 광진구 부동산 핫딜을 소개합니다! 1위, 자양동 래미안크레시티, 84평형, 5.7억원! 2위, 구의동 현대아파트, 59평형, 4.8억원! 지금 바로 확인해보세요!"
    vg.generate_narration(script, 'output/test_narration.mp3')
