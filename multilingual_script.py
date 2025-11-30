"""
다국어 바이럴 스크립트 생성 (영어, 스페인어, 일본어)
"""
from gtts import gTTS
import os
from typing import Dict, List


class MultilingualScriptGenerator:
    """다국어 스크립트 및 음성 생성"""

    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 언어별 템플릿
        self.templates = {
            'ko': {
                'intro': "오늘의 {topic} 핫딜을 소개합니다!",
                'comparison': "{city1} {price1}억 vs {city2} ${price2}! {diff}% 차이!",
                'warning': "⚠️ 경고! {topic}에서 {percentage}% 버블 발견!",
                'secret': "💰 비밀 공개: {topic}로 {amount}억 버는 법!",
                'outro': "지금 바로 확인하고 댓글로 의견 남겨주세요!"
            },
            'en': {
                'intro': "Today's SHOCKING {topic} deals revealed!",
                'comparison': "{city1} ${price1} vs {city2} ${price2}! {diff}% difference!",
                'warning': "⚠️ WARNING! {percentage}% bubble detected in {topic}!",
                'secret': "💰 SECRET: How to make ${amount} from {topic}!",
                'outro': "Check now and drop your thoughts in comments!"
            },
            'es': {
                'intro': "¡Ofertas IMPACTANTES de {topic} reveladas!",
                'comparison': "¡{city1} ${price1} vs {city2} ${price2}! ¡{diff}% diferencia!",
                'warning': "⚠️ ¡ADVERTENCIA! ¡{percentage}% burbuja en {topic}!",
                'secret': "💰 SECRETO: ¡Cómo ganar ${amount} con {topic}!",
                'outro': "¡Comprueba ahora y deja tus comentarios!"
            },
            'ja': {
                'intro': "今日の{topic}激安情報を公開!",
                'comparison': "{city1} ${price1} vs {city2} ${price2}! {diff}%の差!",
                'warning': "⚠️ 警告! {topic}で{percentage}%バブル発見!",
                'secret': "💰 秘密公開: {topic}で${amount}稼ぐ方法!",
                'outro': "今すぐチェックしてコメントしてください!"
            }
        }

    def generate_viral_script(
        self,
        theme: str,
        data: Dict,
        lang: str = 'en',
        style: str = 'comparison'
    ) -> str:
        """바이럴 스크립트 생성"""

        if lang not in self.templates:
            lang = 'en'

        template = self.templates[lang].get(style, self.templates[lang]['intro'])

        # 테마별 스크립트
        if theme == 'global_comparison':
            script = self._generate_comparison_script(data, lang)
        elif theme == 'bubble_warning':
            script = self._generate_warning_script(data, lang)
        elif theme == 'investment_secret':
            script = self._generate_secret_script(data, lang)
        elif theme == 'failure_story':
            script = self._generate_failure_script(data, lang)
        else:
            script = self._generate_default_script(data, lang)

        return script

    def _generate_comparison_script(self, data: Dict, lang: str) -> str:
        """글로벌 비교 스크립트"""
        templates = {
            'ko': (
                f"충격! 서울 {data['kr_price_억']:.1f}억 아파트, "
                f"{data['city']} ${data['city_price']:,}와 비교하면 {abs(data['diff']):.0f}% "
                f"{'더 싸다' if data['is_cheaper'] else '더 비싸'}! "
                f"이게 바로 {'기회' if data['is_cheaper'] else '버블'}입니다! "
                f"지금 바로 확인하세요!"
            ),
            'en': (
                f"SHOCKING! Seoul ${data['kr_price_usd']:,} apartment "
                f"vs {data['city']} ${data['city_price']:,} - {abs(data['diff']):.0f}% "
                f"{'CHEAPER' if data['is_cheaper'] else 'MORE EXPENSIVE'}! "
                f"This is {'your OPPORTUNITY' if data['is_cheaper'] else 'a BUBBLE'}! "
                f"Check it NOW!"
            ),
            'es': (
                f"¡IMPACTANTE! Apartamento en Seúl ${data['kr_price_usd']:,} "
                f"vs {data['city']} ${data['city_price']:,} - ¡{abs(data['diff']):.0f}% "
                f"{'MÁS BARATO' if data['is_cheaper'] else 'MÁS CARO'}! "
                f"¡Esta es {'tu OPORTUNIDAD' if data['is_cheaper'] else 'una BURBUJA'}! "
                f"¡Compruébalo AHORA!"
            ),
            'ja': (
                f"衝撃! ソウル${data['kr_price_usd']:,}マンション、"
                f"{data['city']} ${data['city_price']:,}と比べて{abs(data['diff']):.0f}% "
                f"{'安い' if data['is_cheaper'] else '高い'}! "
                f"これが{'チャンス' if data['is_cheaper'] else 'バブル'}です! "
                f"今すぐ確認!"
            )
        }
        return templates.get(lang, templates['en'])

    def _generate_warning_script(self, data: Dict, lang: str) -> str:
        """버블 경고 스크립트"""
        templates = {
            'ko': (
                f"⚠️ 경고! 한국 부동산 {data['bubble_pct']:.0f}% 과열! "
                f"지난 {data['years']}년간 {data['increase_pct']:.0f}% 상승! "
                f"글로벌 평균 대비 {data['vs_global']:.0f}% 높음! "
                f"투자 전 반드시 확인하세요!"
            ),
            'en': (
                f"⚠️ WARNING! Korean real estate {data['bubble_pct']:.0f}% OVERHEATED! "
                f"Rose {data['increase_pct']:.0f}% in past {data['years']} years! "
                f"{data['vs_global']:.0f}% HIGHER than global average! "
                f"MUST check before investing!"
            ),
            'es': (
                f"⚠️ ¡ADVERTENCIA! ¡Inmobiliaria coreana {data['bubble_pct']:.0f}% SOBRECALENTADA! "
                f"¡Subió {data['increase_pct']:.0f}% en {data['years']} años! "
                f"¡{data['vs_global']:.0f}% MÁS ALTO que promedio global! "
                f"¡DEBES verificar antes de invertir!"
            )
        }
        return templates.get(lang, templates['en'])

    def _generate_secret_script(self, data: Dict, lang: str) -> str:
        """투자 비밀 스크립트"""
        templates = {
            'ko': (
                f"💰 비밀 공개! {data['location']} 투자로 "
                f"연 {data['annual_return']:.0f}% 수익! "
                f"{data['years']}년 후 {data['profit_억']:.1f}억 수익 예상! "
                f"지금이 마지막 기회입니다!"
            ),
            'en': (
                f"💰 SECRET revealed! Invest in {data['location']} for "
                f"{data['annual_return']:.0f}% annual return! "
                f"Projected ${data['profit_usd']:,} profit in {data['years']} years! "
                f"This is your LAST chance!"
            ),
            'es': (
                f"💰 ¡SECRETO revelado! ¡Invierte en {data['location']} para "
                f"{data['annual_return']:.0f}% retorno anual! "
                f"¡Ganancia proyectada de ${data['profit_usd']:,} en {data['years']} años! "
                f"¡Esta es tu ÚLTIMA oportunidad!"
            )
        }
        return templates.get(lang, templates['en'])

    def _generate_failure_script(self, data: Dict, lang: str) -> str:
        """투자 실패담 스크립트"""
        templates = {
            'ko': (
                f"😱 실화! {data['year']}년 {data['location']} 투자, "
                f"{data['loss_억']:.1f}억 손실! "
                f"원인: {data['reason']}! "
                f"같은 실수 하지 마세요!"
            ),
            'en': (
                f"😱 TRUE STORY! {data['year']} investment in {data['location']}, "
                f"${data['loss_usd']:,} LOSS! "
                f"Reason: {data['reason']}! "
                f"Don't make the SAME mistake!"
            ),
            'es': (
                f"😱 ¡HISTORIA REAL! Inversión {data['year']} en {data['location']}, "
                f"¡PÉRDIDA de ${data['loss_usd']:,}! "
                f"Razón: {data['reason']}! "
                f"¡No cometas el MISMO error!"
            )
        }
        return templates.get(lang, templates['en'])

    def _generate_default_script(self, data: Dict, lang: str) -> str:
        """기본 스크립트"""
        return self.templates[lang]['intro'].format(topic=data.get('topic', 'Real Estate'))

    def generate_voice(self, script: str, lang: str = 'en', filename: str = None) -> str:
        """다국어 음성 생성"""
        if filename is None:
            filename = f'{self.output_dir}/narration_{lang}.mp3'

        # gTTS 언어 코드 매핑
        gtts_langs = {
            'ko': 'ko',
            'en': 'en',
            'es': 'es',
            'ja': 'ja'
        }

        try:
            tts = gTTS(text=script, lang=gtts_langs.get(lang, 'en'), slow=False)
            tts.save(filename)
            print(f"음성 생성 완료 ({lang}): {filename}")
            return filename
        except Exception as e:
            print(f"음성 생성 실패: {e}")
            return None

    def generate_ab_test_scripts(self, data: Dict, lang: str = 'en') -> List[Dict]:
        """A/B 테스트용 다양한 스크립트 생성"""
        scripts = []

        # 스타일 1: SHOCKING
        scripts.append({
            'style': 'shocking',
            'title': f"🔥 SHOCKING! {data.get('title', 'Real Estate Secrets')}",
            'script': self.generate_viral_script('global_comparison', data, lang),
            'hashtags': ['#Shocking', '#RealEstate', '#Viral']
        })

        # 스타일 2: WARNING
        if 'bubble_pct' in data:
            scripts.append({
                'style': 'warning',
                'title': f"⚠️ WARNING! {data.get('title', 'Market Alert')}",
                'script': self.generate_viral_script('bubble_warning', data, lang),
                'hashtags': ['#Warning', '#Investment', '#Alert']
            })

        # 스타일 3: SECRET
        if 'annual_return' in data:
            scripts.append({
                'style': 'secret',
                'title': f"💰 SECRET! {data.get('title', 'Investment Hack')}",
                'script': self.generate_viral_script('investment_secret', data, lang),
                'hashtags': ['#Secret', '#PassiveIncome', '#Investment']
            })

        return scripts


if __name__ == "__main__":
    generator = MultilingualScriptGenerator()

    # 테스트 데이터
    test_data = {
        'kr_price_억': 6.0,
        'kr_price_usd': 450000,
        'city': '뉴욕',
        'city_price': 750000,
        'diff': -40,
        'is_cheaper': True
    }

    print("\n=== 다국어 스크립트 생성 ===")
    for lang in ['ko', 'en', 'es', 'ja']:
        script = generator.generate_viral_script('global_comparison', test_data, lang)
        print(f"\n[{lang.upper()}]")
        print(script)
