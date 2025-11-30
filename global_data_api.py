"""
글로벌 부동산 데이터 API 연동
"""
import requests
from typing import Dict, Optional


class GlobalRealEstateAPI:
    """글로벌 부동산 데이터 수집"""

    def __init__(self):
        self.exchange_rates = {}
        self.global_prices = {}

    def get_exchange_rate(self, from_currency='KRW', to_currency='USD'):
        """환율 정보 가져오기"""
        try:
            # 무료 환율 API 사용
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url, timeout=5)
            data = response.json()

            if 'rates' in data and to_currency in data['rates']:
                rate = data['rates'][to_currency]
                print(f"환율: 1 {from_currency} = {rate:.4f} {to_currency}")
                return rate
        except Exception as e:
            print(f"환율 조회 실패: {e}")
            # 기본값 사용 (2024년 기준)
            default_rates = {
                'USD': 0.00075,  # 1 KRW = 0.00075 USD
                'EUR': 0.00070,
                'JPY': 0.11,
            }
            return default_rates.get(to_currency, 0.00075)

    def get_global_comparison(self, kr_price: int) -> Dict[str, Dict]:
        """한국 가격과 글로벌 비교"""
        usd_price = kr_price * self.get_exchange_rate('KRW', 'USD')

        # 주요 도시 평균 아파트 가격 (2024년 기준, USD)
        global_avg_prices = {
            'US': {
                'city': '뉴욕',
                'avg_price': 750000,
                'currency': 'USD',
                'emoji': '🇺🇸'
            },
            'JP': {
                'city': '도쿄',
                'avg_price': 500000,
                'currency': 'USD',
                'emoji': '🇯🇵'
            },
            'UK': {
                'city': '런던',
                'avg_price': 650000,
                'currency': 'USD',
                'emoji': '🇬🇧'
            },
            'SG': {
                'city': '싱가포르',
                'avg_price': 1200000,
                'currency': 'USD',
                'emoji': '🇸🇬'
            },
            'CN': {
                'city': '상하이',
                'avg_price': 450000,
                'currency': 'USD',
                'emoji': '🇨🇳'
            }
        }

        # 한국 가격과 비교
        comparisons = {}
        for country, data in global_avg_prices.items():
            diff_pct = ((usd_price - data['avg_price']) / data['avg_price'] * 100)
            comparisons[country] = {
                **data,
                'kr_price_usd': usd_price,
                'difference': diff_pct,
                'is_cheaper': usd_price < data['avg_price']
            }

        return comparisons

    def generate_viral_hook(self, kr_price: int, country: str = 'US') -> str:
        """바이럴 후크 생성"""
        comparisons = self.get_global_comparison(kr_price)

        if country not in comparisons:
            country = 'US'

        comp = comparisons[country]
        kr_price_억 = kr_price / 100000000

        if comp['is_cheaper']:
            diff = abs(comp['difference'])
            hooks = [
                f"🔥 한국 {kr_price_억:.1f}억 vs {comp['emoji']}{comp['city']} ${comp['avg_price']:,}? {diff:.0f}% 더 싸다!",
                f"⚠️ SHOCKING! 서울 아파트가 {comp['city']}보다 저렴한 이유",
                f"💰 SECRET: {comp['city']} 대신 한국에 투자하면 {diff:.0f}% 절약!",
            ]
        else:
            diff = abs(comp['difference'])
            hooks = [
                f"😱 한국 집값 버블? {comp['city']}보다 {diff:.0f}% 비싸!",
                f"⚠️ WARNING: 서울 {kr_price_억:.1f}억 = {comp['emoji']}{comp['city']} ${comp['kr_price_usd']:,.0f}",
                f"🚨 한국 부동산 위험 신호! {comp['city']} 대비 {diff:.0f}% 과열",
            ]

        return hooks

    def get_investment_returns(self, kr_price: int, years: int = 10) -> Dict:
        """투자 수익률 계산"""
        # 한국 부동산 역사적 수익률 (연평균 약 5-7%)
        kr_annual_return = 0.06

        # 글로벌 평균 수익률
        global_returns = {
            'US': 0.04,   # 미국 4%
            'JP': 0.02,   # 일본 2%
            'UK': 0.05,   # 영국 5%
            'SG': 0.03,   # 싱가포르 3%
        }

        kr_future = kr_price * ((1 + kr_annual_return) ** years)

        comparisons = {}
        for country, rate in global_returns.items():
            future = kr_price * ((1 + rate) ** years)
            comparisons[country] = {
                'future_value': future,
                'profit': future - kr_price,
                'profit_pct': ((future / kr_price) - 1) * 100,
                'vs_korea': ((kr_future - future) / future) * 100
            }

        return {
            'korea': {
                'future_value': kr_future,
                'profit': kr_future - kr_price,
                'profit_pct': ((kr_future / kr_price) - 1) * 100
            },
            'global': comparisons
        }


if __name__ == "__main__":
    api = GlobalRealEstateAPI()

    # 테스트: 6억원 아파트
    kr_price = 600000000

    print("\n=== 글로벌 비교 ===")
    comparisons = api.get_global_comparison(kr_price)
    for country, data in comparisons.items():
        print(f"{data['emoji']} {data['city']}: ${data['avg_price']:,}")
        print(f"  한국과 차이: {data['difference']:.1f}%")

    print("\n=== 바이럴 후크 ===")
    hooks = api.generate_viral_hook(kr_price, 'US')
    for i, hook in enumerate(hooks, 1):
        print(f"{i}. {hook}")

    print("\n=== 투자 수익률 (10년) ===")
    returns = api.get_investment_returns(kr_price, 10)
    print(f"한국: {returns['korea']['profit']/100000000:.1f}억 수익 ({returns['korea']['profit_pct']:.1f}%)")
