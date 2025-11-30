#!/usr/bin/env python3
"""
글로벌 바이럴 쇼츠 자동 생성 시스템

사용법:
    python generate_global_shorts.py --lang en --country US --theme comparison
"""

import argparse
import os
from pathlib import Path
import json
from datetime import datetime

from data_processor import RealEstateDataProcessor
from global_data_api import GlobalRealEstateAPI
from multilingual_script import MultilingualScriptGenerator
from thumbnail_generator import ThumbnailGenerator
from visualizer import RealEstateVisualizer
from video_composer import VideoComposer


class GlobalShortsGenerator:
    """글로벌 바이럴 쇼츠 생성기"""

    def __init__(self, output_dir='output/global'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.api = GlobalRealEstateAPI()
        self.script_gen = MultilingualScriptGenerator(str(self.output_dir))
        self.thumb_gen = ThumbnailGenerator(str(self.output_dir))
        self.visualizer = RealEstateVisualizer(str(self.output_dir))
        self.composer = VideoComposer(str(self.output_dir))

    def generate_shorts(
        self,
        kr_data: dict,
        lang: str = 'en',
        country: str = 'US',
        theme: str = 'comparison',
        ab_test: bool = False
    ) -> dict:
        """바이럴 쇼츠 생성"""

        print(f"\n{'='*60}")
        print(f"글로벌 바이럴 쇼츠 생성 시작")
        print(f"언어: {lang.upper()} | 국가: {country} | 테마: {theme}")
        print(f"{'='*60}\n")

        # 1. 데이터 준비
        kr_price = kr_data.get('price', 600000000)  # 기본 6억
        kr_price_억 = kr_price / 100000000

        # 2. 글로벌 비교 데이터
        comparisons = self.api.get_global_comparison(kr_price)

        if country not in comparisons:
            print(f"경고: {country} 데이터 없음, US로 대체")
            country = 'US'

        comp = comparisons[country]

        # 3. 스크립트 데이터 준비
        script_data = {
            'kr_price_억': kr_price_억,
            'kr_price_usd': comp['kr_price_usd'],
            'city': comp['city'],
            'city_price': comp['avg_price'],
            'diff': comp['difference'],
            'is_cheaper': comp['is_cheaper']
        }

        # 4. A/B 테스트 모드
        if ab_test:
            return self._generate_ab_test_shorts(script_data, lang, country)

        # 5. 단일 쇼츠 생성
        return self._generate_single_shorts(script_data, lang, country, theme)

    def _generate_single_shorts(
        self,
        data: dict,
        lang: str,
        country: str,
        theme: str
    ) -> dict:
        """단일 쇼츠 생성"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{lang}_{country}_{theme}_{timestamp}"

        # 1. 스크립트 생성
        print(f"[1/5] 스크립트 생성 ({lang})")
        script = self.script_gen.generate_viral_script(
            f'global_{theme}',
            data,
            lang
        )
        print(f"스크립트: {script}\n")

        # 2. 음성 생성
        print(f"[2/5] 음성 생성")
        audio_file = self.script_gen.generate_voice(
            script,
            lang,
            str(self.output_dir / f'{base_name}_audio.mp3')
        )

        # 3. 썸네일 생성
        print(f"[3/5] 썸네일 생성")
        thumbnail = self.thumb_gen.create_comparison_thumbnail(
            kr_price=f"${data['kr_price_usd']:,.0f}",
            global_price=f"${data['city_price']:,.0f}",
            city=f"{data.get('emoji', '🌍')} {data['city']}",
            diff_pct=data['diff'],
            output_file=str(self.output_dir / f'{base_name}_thumbnail.png')
        )

        # 4. 비디오 생성 (썸네일을 15초 비디오로)
        print(f"[4/5] 비디오 생성")
        video_file = self._image_to_video(
            thumbnail,
            str(self.output_dir / f'{base_name}_video.mp4')
        )

        # 5. 최종 합성
        print(f"[5/5] 최종 합성")
        if video_file and audio_file:
            final_video = self.composer.create_shorts_video(
                video_file,
                audio_file,
                output_file=str(self.output_dir / f'{base_name}_final.mp4')
            )

            result = {
                'success': True,
                'lang': lang,
                'country': country,
                'theme': theme,
                'script': script,
                'files': {
                    'video': final_video,
                    'audio': audio_file,
                    'thumbnail': thumbnail
                },
                'metadata': {
                    'title': self._generate_title(data, lang, 'shocking'),
                    'description': script,
                    'hashtags': self._generate_hashtags(theme, lang),
                    'upload_time': '08:00'  # 미국 시간대 고려
                }
            }

            # 메타데이터 저장
            meta_file = self.output_dir / f'{base_name}_metadata.json'
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"\n{'='*60}")
            print(f"✓ 쇼츠 생성 완료!")
            print(f"{'='*60}")
            print(f"비디오: {final_video}")
            print(f"썸네일: {thumbnail}")
            print(f"메타데이터: {meta_file}")
            print(f"{'='*60}\n")

            return result

        return {'success': False, 'error': '비디오/음성 생성 실패'}

    def _generate_ab_test_shorts(
        self,
        data: dict,
        lang: str,
        country: str
    ) -> list:
        """A/B 테스트용 여러 쇼츠 생성"""

        print(f"\n{'='*60}")
        print(f"A/B 테스트 모드: 3개 버전 생성")
        print(f"{'='*60}\n")

        results = []
        themes = ['comparison', 'bubble_warning', 'investment_secret']

        for theme in themes:
            try:
                result = self._generate_single_shorts(data, lang, country, theme)
                results.append(result)
            except Exception as e:
                print(f"테마 {theme} 생성 실패: {e}")
                continue

        return results

    def _image_to_video(self, image_file: str, output_file: str, duration: int = 15) -> str:
        """이미지를 비디오로 변환"""
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
                return output_file
        except Exception as e:
            print(f"비디오 변환 실패: {e}")
        return None

    def _generate_title(self, data: dict, lang: str, style: str) -> str:
        """제목 생성"""
        templates = {
            'en': {
                'shocking': f"🔥 SHOCKING! Seoul ${data['kr_price_usd']:,.0f} vs {data['city']} ${data['city_price']:,.0f}!",
                'warning': f"⚠️ WARNING! Seoul Real Estate {abs(data['diff']):.0f}% {'CHEAPER' if data['is_cheaper'] else 'BUBBLE'}!",
                'secret': f"💰 SECRET! Invest in Seoul vs {data['city']} - {abs(data['diff']):.0f}% Difference!"
            },
            'es': {
                'shocking': f"🔥 ¡IMPACTANTE! Seúl ${data['kr_price_usd']:,.0f} vs {data['city']} ${data['city_price']:,.0f}!",
                'warning': f"⚠️ ¡ADVERTENCIA! Inmobiliaria Seúl {abs(data['diff']):.0f}% {'MÁS BARATA' if data['is_cheaper'] else 'BURBUJA'}!",
                'secret': f"💰 ¡SECRETO! Invierte en Seúl vs {data['city']} - ¡{abs(data['diff']):.0f}% Diferencia!"
            }
        }
        return templates.get(lang, templates['en']).get(style, templates['en']['shocking'])

    def _generate_hashtags(self, theme: str, lang: str) -> list:
        """해시태그 생성"""
        common = ['#Shorts', '#RealEstate', '#Investing']

        theme_tags = {
            'comparison': ['#GlobalComparison', '#HousingMarket'],
            'bubble_warning': ['#MarketCrash', '#InvestmentWarning'],
            'investment_secret': ['#PassiveIncome', '#WealthBuilding']
        }

        lang_tags = {
            'en': ['#InvestmentTips', '#FinancialFreedom'],
            'es': ['#Inversiones', '#LibertadFinanciera'],
            'ja': ['#投資', '#不動産']
        }

        return common + theme_tags.get(theme, []) + lang_tags.get(lang, [])


def main():
    parser = argparse.ArgumentParser(description='글로벌 바이럴 쇼츠 생성')
    parser.add_argument('--lang', default='en', choices=['ko', 'en', 'es', 'ja'],
                       help='언어 선택')
    parser.add_argument('--country', default='US', choices=['US', 'JP', 'UK', 'SG', 'CN'],
                       help='비교 국가')
    parser.add_argument('--theme', default='comparison',
                       choices=['comparison', 'bubble_warning', 'investment_secret'],
                       help='테마 선택')
    parser.add_argument('--price', type=int, default=600000000,
                       help='한국 부동산 가격 (원)')
    parser.add_argument('--ab-test', action='store_true',
                       help='A/B 테스트 모드 (3개 버전 생성)')

    args = parser.parse_args()

    # 생성기 초기화
    generator = GlobalShortsGenerator()

    # 데이터 준비
    kr_data = {
        'price': args.price
    }

    # 쇼츠 생성
    result = generator.generate_shorts(
        kr_data,
        lang=args.lang,
        country=args.country,
        theme=args.theme,
        ab_test=args.ab_test
    )

    if isinstance(result, list):
        print(f"\n총 {len(result)}개 쇼츠 생성 완료!")
    elif result.get('success'):
        print(f"\n쇼츠 생성 성공!")
    else:
        print(f"\n쇼츠 생성 실패: {result.get('error')}")


if __name__ == "__main__":
    main()
