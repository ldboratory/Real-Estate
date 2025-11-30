"""
바이럴 썸네일 자동 생성 (Pillow 사용)
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
from typing import Tuple, List


class ThumbnailGenerator:
    """유튜브 쇼츠용 썸네일 생성"""

    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 쇼츠 썸네일 사이즈 (세로형)
        self.width = 1080
        self.height = 1920

    def create_viral_thumbnail(
        self,
        title: str,
        subtitle: str = "",
        style: str = "shocking",
        output_file: str = None
    ) -> str:
        """바이럴 썸네일 생성"""

        if output_file is None:
            output_file = f'{self.output_dir}/thumbnail_{style}.png'

        # 배경 생성
        if style == "shocking":
            bg_color = (220, 20, 60)  # 빨강
            text_color = (255, 255, 255)
            emoji = "🔥"
        elif style == "warning":
            bg_color = (255, 140, 0)  # 주황
            text_color = (0, 0, 0)
            emoji = "⚠️"
        elif style == "secret":
            bg_color = (50, 50, 50)  # 검정
            text_color = (255, 215, 0)
            emoji = "💰"
        else:
            bg_color = (30, 30, 30)
            text_color = (255, 255, 255)
            emoji = "📊"

        # 이미지 생성
        img = Image.new('RGB', (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(img)

        # 그라데이션 효과 (간단한 어둡기 효과)
        for y in range(self.height):
            darkness = int(255 * (y / self.height) * 0.3)
            color = tuple(max(0, c - darkness) for c in bg_color)
            draw.line([(0, y), (self.width, y)], fill=color)

        # 폰트 설정 (시스템 기본 폰트 사용)
        try:
            # macOS 기본 폰트
            title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 100)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 60)
            emoji_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 150)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            emoji_font = ImageFont.load_default()

        # 이모지 추가 (상단)
        emoji_bbox = draw.textbbox((0, 0), emoji, font=emoji_font)
        emoji_width = emoji_bbox[2] - emoji_bbox[0]
        emoji_x = (self.width - emoji_width) // 2
        draw.text((emoji_x, 200), emoji, fill=text_color, font=emoji_font)

        # 제목 텍스트 (중앙, 여러 줄)
        title_words = title.split()
        lines = []
        current_line = ""

        for word in title_words:
            test_line = current_line + word + " "
            bbox = draw.textbbox((0, 0), test_line, font=title_font)
            if bbox[2] - bbox[0] < self.width - 100:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())

        # 텍스트 그리기 (그림자 효과)
        y_offset = 600
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_x = (self.width - text_width) // 2

            # 그림자
            draw.text((text_x + 5, y_offset + 5), line, fill=(0, 0, 0), font=title_font)
            # 실제 텍스트
            draw.text((text_x, y_offset), line, fill=text_color, font=title_font)
            y_offset += 120

        # 부제목
        if subtitle:
            bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = bbox[2] - bbox[0]
            subtitle_x = (self.width - subtitle_width) // 2
            subtitle_y = y_offset + 50

            # 배경 박스
            padding = 20
            draw.rectangle(
                [subtitle_x - padding, subtitle_y - padding,
                 subtitle_x + subtitle_width + padding, subtitle_y + 80],
                fill=(0, 0, 0, 180)
            )

            draw.text((subtitle_x, subtitle_y), subtitle, fill=(255, 255, 0), font=subtitle_font)

        # 저장
        img.save(output_file, quality=95)
        print(f"썸네일 생성 완료: {output_file}")
        return output_file

    def create_ab_test_thumbnails(self, title: str, base_name: str = "thumbnail") -> List[str]:
        """A/B 테스트용 여러 스타일 썸네일 생성"""
        thumbnails = []

        styles = [
            ("shocking", "🔥 SHOCKING!", "shocking"),
            ("warning", "⚠️ WARNING!", "warning"),
            ("secret", "💰 SECRET!", "secret"),
        ]

        for i, (style_name, prefix, style) in enumerate(styles, 1):
            output_file = f'{self.output_dir}/{base_name}_{style_name}.png'
            full_title = f"{prefix} {title}"
            self.create_viral_thumbnail(
                full_title,
                subtitle="Check NOW!",
                style=style,
                output_file=output_file
            )
            thumbnails.append(output_file)

        return thumbnails

    def create_comparison_thumbnail(
        self,
        kr_price: str,
        global_price: str,
        city: str,
        diff_pct: float,
        output_file: str = None
    ) -> str:
        """가격 비교 썸네일"""

        if output_file is None:
            output_file = f'{self.output_dir}/comparison_thumbnail.png'

        # 배경
        img = Image.new('RGB', (self.width, self.height), (20, 20, 50))
        draw = ImageDraw.Draw(img)

        try:
            large_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 120)
            medium_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 80)
            small_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 60)
        except:
            large_font = ImageFont.load_default()
            medium_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        # 제목
        title = "VS"
        bbox = draw.textbbox((0, 0), title, font=large_font)
        title_width = bbox[2] - bbox[0]
        draw.text(((self.width - title_width) // 2, 100), title, fill=(255, 255, 255), font=large_font)

        # 한국 가격 (상단)
        kr_text = f"🇰🇷 Seoul"
        bbox = draw.textbbox((0, 0), kr_text, font=medium_font)
        kr_width = bbox[2] - bbox[0]
        draw.text(((self.width - kr_width) // 2, 400), kr_text, fill=(255, 200, 0), font=medium_font)

        price_text = kr_price
        bbox = draw.textbbox((0, 0), price_text, font=large_font)
        price_width = bbox[2] - bbox[0]
        draw.text(((self.width - price_width) // 2, 550), price_text, fill=(255, 255, 255), font=large_font)

        # VS
        vs_text = "VS"
        bbox = draw.textbbox((0, 0), vs_text, font=medium_font)
        vs_width = bbox[2] - bbox[0]
        draw.text(((self.width - vs_width) // 2, 800), vs_text, fill=(255, 100, 100), font=medium_font)

        # 글로벌 도시 가격 (하단)
        city_text = f"{city}"
        bbox = draw.textbbox((0, 0), city_text, font=medium_font)
        city_width = bbox[2] - bbox[0]
        draw.text(((self.width - city_width) // 2, 1000), city_text, fill=(100, 200, 255), font=medium_font)

        global_price_text = global_price
        bbox = draw.textbbox((0, 0), global_price_text, font=large_font)
        global_price_width = bbox[2] - bbox[0]
        draw.text(((self.width - global_price_width) // 2, 1150), global_price_text, fill=(255, 255, 255), font=large_font)

        # 차이 표시
        diff_text = f"{abs(diff_pct):.0f}% {'CHEAPER' if diff_pct < 0 else 'MORE'}"
        diff_color = (0, 255, 100) if diff_pct < 0 else (255, 50, 50)
        bbox = draw.textbbox((0, 0), diff_text, font=medium_font)
        diff_width = bbox[2] - bbox[0]

        # 배경 박스
        padding = 30
        draw.rectangle(
            [(self.width - diff_width) // 2 - padding, 1450,
             (self.width + diff_width) // 2 + padding, 1600],
            fill=diff_color
        )
        draw.text(((self.width - diff_width) // 2, 1470), diff_text, fill=(0, 0, 0), font=medium_font)

        img.save(output_file, quality=95)
        print(f"비교 썸네일 생성 완료: {output_file}")
        return output_file


if __name__ == "__main__":
    generator = ThumbnailGenerator()

    # 테스트: 바이럴 썸네일
    print("\n=== 바이럴 썸네일 생성 ===")
    generator.create_viral_thumbnail(
        "SEOUL REAL ESTATE CRASH!",
        subtitle="40% CHEAPER!",
        style="shocking"
    )

    # 테스트: A/B 테스트 썸네일
    print("\n=== A/B 테스트 썸네일 ===")
    generator.create_ab_test_thumbnails("Real Estate Secrets")

    # 테스트: 비교 썸네일
    print("\n=== 비교 썸네일 ===")
    generator.create_comparison_thumbnail(
        kr_price="$450K",
        global_price="$750K",
        city="🇺🇸 New York",
        diff_pct=-40
    )
