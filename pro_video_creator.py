"""
프로 영상 생성 (MoviePy + 무료 툴)
"""
# MoviePy 2.x imports
from moviepy import (
    VideoClip, ImageClip, VideoFileClip, AudioFileClip,
    CompositeVideoClip, TextClip, concatenate_videoclips
)
from moviepy import vfx
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os


class ProVideoCreator:
    """프로페셔널 영상 제작"""

    def __init__(self, output_dir='output/pro'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 쇼츠 사이즈
        self.width = 1080
        self.height = 1920
        self.fps = 30

    def create_animated_intro(
        self,
        title: str,
        subtitle: str,
        duration: float = 3.0
    ) -> VideoClip:
        """애니메이션 인트로 (3초)"""

        def make_frame(t):
            """프레임 생성 함수"""
            # 배경 그라데이션
            img = Image.new('RGB', (self.width, self.height), '#1a1a2e')
            draw = ImageDraw.Draw(img)

            # 그라데이션 효과
            for y in range(self.height):
                r = int(26 + (233 - 26) * (y / self.height) * 0.3)
                g = int(26 + (69 - 26) * (y / self.height) * 0.3)
                b = int(46 + (96 - 46) * (y / self.height) * 0.3)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b))

            # 애니메이션 효과 (fade in + slide up)
            progress = min(t / duration, 1.0)
            alpha = int(255 * progress)

            # 타이틀 위치 (아래에서 위로)
            title_y = int(self.height * 0.4 + (1 - progress) * 200)

            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 80)
                subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 50)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()

            # 제목 그리기
            bbox = draw.textbbox((0, 0), title, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_x = (self.width - text_width) // 2

            # 그림자
            draw.text((text_x + 3, title_y + 3), title, fill=(0, 0, 0, alpha), font=title_font)
            # 실제 텍스트
            draw.text((text_x, title_y), title, fill=(255, 255, 255, alpha), font=title_font)

            # 부제목
            if subtitle and progress > 0.5:
                subtitle_progress = (progress - 0.5) * 2
                subtitle_alpha = int(255 * subtitle_progress)
                bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
                sub_width = bbox[2] - bbox[0]
                sub_x = (self.width - sub_width) // 2
                sub_y = title_y + 120

                draw.text((sub_x, sub_y), subtitle, fill=(255, 215, 0, subtitle_alpha), font=subtitle_font)

            return np.array(img)

        return VideoClip(make_frame, duration=duration)

    def create_data_visualization(
        self,
        opportunity: dict,
        market_data: dict,
        duration: float = 7.0
    ) -> str:
        """데이터 시각화 영상"""

        output_file = str(self.output_dir / 'data_viz.mp4')

        # Matplotlib으로 차트 생성
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10.8, 19.2))
        fig.patch.set_facecolor('#1a1a2e')

        # 1. 가격 비교 (서울 vs 글로벌)
        ax1.set_facecolor('#16213e')
        cities = ['Seoul', 'NY', 'Tokyo', 'London']
        prices = [450, 750, 500, 650]  # 예시
        colors = ['#e94560', '#888', '#888', '#888']
        ax1.bar(cities, prices, color=colors)
        ax1.set_title('Price Comparison (K USD)', color='white', fontsize=16)
        ax1.tick_params(colors='white')

        # 2. ROI 프로젝션
        ax2.set_facecolor('#16213e')
        years = [0, 1, 2, 3, 4, 5]
        seoul_roi = [450, 477, 505, 535, 567, 600]
        ny_roi = [450, 468, 487, 506, 527, 548]
        ax2.plot(years, seoul_roi, 'o-', color='#e94560', linewidth=3, label='Seoul')
        ax2.plot(years, ny_roi, 'o-', color='#888', linewidth=2, label='NY')
        ax2.set_title('5-Year ROI Projection', color='white', fontsize=16)
        ax2.legend(facecolor='#16213e', edgecolor='white')
        ax2.tick_params(colors='white')
        ax2.grid(True, alpha=0.2, color='white')

        # 3. 투자 점수
        ax3.set_facecolor('#16213e')
        categories = ['Value', 'Location', 'Age', 'Floor', 'Size']
        scores = [85, 90, 75, 80, 70]  # 예시
        ax3.barh(categories, scores, color='#e94560')
        ax3.set_title('Investment Score', color='white', fontsize=16)
        ax3.set_xlim(0, 100)
        ax3.tick_params(colors='white')

        # 4. 시장 사이클
        ax4.set_facecolor('#16213e')
        cycle_text = market_data.get('cycle', 'BULL MARKET').upper()
        action_text = market_data.get('action', 'BUY').upper()
        ax4.text(0.5, 0.6, cycle_text, ha='center', va='center',
                fontsize=30, fontweight='bold', color='#e94560',
                transform=ax4.transAxes)
        ax4.text(0.5, 0.3, action_text, ha='center', va='center',
                fontsize=24, color='white',
                transform=ax4.transAxes)
        ax4.set_title('Market Status', color='white', fontsize=16)
        ax4.axis('off')

        # 레이아웃 조정
        plt.tight_layout()

        # 이미지로 저장
        chart_file = str(self.output_dir / 'chart_temp.png')
        plt.savefig(chart_file, dpi=100, facecolor='#1a1a2e')
        plt.close()

        # MoviePy로 영상 변환
        try:
            clip = ImageClip(chart_file, duration=duration)
            # MoviePy 2.x uses vfx module
            clip = clip.with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
            clip.write_videofile(output_file, fps=self.fps, codec='libx264', logger=None)

            return output_file
        except Exception as e:
            print(f"Video creation failed: {e}")
            return None

    def create_final_shorts(
        self,
        intro_text: tuple,
        data_viz_file: str,
        audio_file: str,
        outro_text: str = "INVEST SMART!",
        output_file: str = None
    ) -> str:
        """최종 쇼츠 조립"""

        if output_file is None:
            output_file = str(self.output_dir / 'final_shorts.mp4')

        try:
            # 1. 인트로 (3초)
            intro = self.create_animated_intro(intro_text[0], intro_text[1], duration=3.0)

            # 2. 데이터 시각화 (7초)
            data_clip = VideoFileClip(data_viz_file)

            # 3. 아웃트로 (2초)
            outro = self.create_animated_intro(outro_text, "Check Now!", duration=2.0)

            # 4. 영상 합치기
            final_video = concatenate_videoclips([intro, data_clip, outro])

            # 5. 오디오 추가
            if audio_file and os.path.exists(audio_file):
                audio = AudioFileClip(audio_file)
                final_video = final_video.with_audio(audio)

            # 6. 최종 렌더링
            final_video.write_videofile(
                output_file,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                preset='medium',
                bitrate='3000k',
                logger=None
            )

            print(f"✓ Final shorts created: {output_file}")
            return output_file

        except Exception as e:
            print(f"Final assembly failed: {e}")
            return None

    def add_text_overlay(
        self,
        video_file: str,
        texts: list,
        output_file: str = None
    ) -> str:
        """텍스트 오버레이 추가 (자막)"""

        if output_file is None:
            output_file = str(self.output_dir / 'video_with_text.mp4')

        try:
            video = VideoFileClip(video_file)

            # 텍스트 클립 생성
            text_clips = []
            for text_info in texts:
                # MoviePy 2.x TextClip API
                txt_clip = TextClip(
                    text=text_info['text'],
                    font_size=text_info.get('fontsize', 60),
                    color=text_info.get('color', 'white'),
                    font='Arial-Bold',
                    stroke_color=text_info.get('stroke', 'black'),
                    stroke_width=text_info.get('stroke_width', 2),
                    duration=text_info['duration']
                ).with_position(('center', text_info.get('position', 'bottom'))).with_start(text_info['start'])

                text_clips.append(txt_clip)

            # 오버레이 합성
            final = CompositeVideoClip([video] + text_clips)
            final.write_videofile(output_file, fps=self.fps, codec='libx264', logger=None)

            return output_file

        except Exception as e:
            print(f"Text overlay failed: {e}")
            return video_file


if __name__ == "__main__":
    creator = ProVideoCreator()

    # 테스트 데이터
    opportunity = {
        'price': 600000000,
        'score': 85
    }

    market_data = {
        'cycle': 'BULL MARKET',
        'action': 'BUY NOW'
    }

    # 인트로 생성
    print("Creating professional intro...")
    intro = creator.create_animated_intro(
        "SEOUL INVESTMENT",
        "Grade A Opportunity"
    )

    print("\nCreating data visualization...")
    viz = creator.create_data_visualization(opportunity, market_data)

    print("\n✓ Professional video components ready!")
