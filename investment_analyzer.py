"""
실제 투자 가치 분석 시스템
Real investment value analysis for decision-making
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class InvestmentAnalyzer:
    """투자 가치 분석 및 추천 시스템"""

    def __init__(self):
        self.risk_threshold = 0.15  # 15% 위험 임계값
        self.roi_target = 0.08      # 연 8% 목표 수익률

    def analyze_market_cycle(self, trend_data: pd.DataFrame) -> Dict:
        """시장 사이클 분석 (상승/하락/횡보)"""

        if len(trend_data) < 3:
            return {'cycle': 'insufficient_data', 'confidence': 0}

        # 가격 변화율 계산
        prices = trend_data['평균가격'].values
        changes = np.diff(prices) / prices[:-1]

        # 최근 3개월 평균 변화율
        recent_change = np.mean(changes[-3:]) if len(changes) >= 3 else 0

        # 변동성 (표준편차)
        volatility = np.std(changes)

        # 사이클 판단
        if recent_change > 0.02:  # 2% 이상 상승
            cycle = 'bull_market'
            action = 'BUY_OPPORTUNITY'
            confidence = min(abs(recent_change) * 50, 0.95)
        elif recent_change < -0.02:  # 2% 이상 하락
            cycle = 'bear_market'
            action = 'WAIT_OR_BARGAIN'
            confidence = min(abs(recent_change) * 50, 0.95)
        else:
            cycle = 'sideways'
            action = 'HOLD_POSITION'
            confidence = 0.6

        return {
            'cycle': cycle,
            'action': action,
            'change_rate': recent_change * 100,
            'volatility': volatility * 100,
            'confidence': confidence,
            'trend': 'upward' if recent_change > 0 else 'downward'
        }

    def calculate_roi_projection(
        self,
        current_price: float,
        historical_growth: float,
        holding_period: int = 5
    ) -> Dict:
        """ROI 예측 (5년 기준)"""

        # 보수적 성장률 (역사적 성장률의 70%)
        conservative_growth = historical_growth * 0.7

        # 시나리오별 예측
        scenarios = {
            'conservative': conservative_growth * 0.5,
            'moderate': conservative_growth,
            'optimistic': conservative_growth * 1.3
        }

        projections = {}
        for scenario, growth_rate in scenarios.items():
            future_value = current_price * ((1 + growth_rate) ** holding_period)
            total_return = future_value - current_price
            roi_percentage = (total_return / current_price) * 100

            projections[scenario] = {
                'future_value': future_value,
                'profit': total_return,
                'roi_pct': roi_percentage,
                'annual_roi': roi_percentage / holding_period
            }

        return projections

    def find_investment_opportunities(
        self,
        df: pd.DataFrame,
        budget: float = 600000000,  # 6억
        min_roi: float = 0.06        # 연 6% 최소 수익
    ) -> List[Dict]:
        """투자 기회 발견"""

        opportunities = []

        for idx, row in df.iterrows():
            price = row.get('거래금액_숫자', 0)

            if price > budget:
                continue

            # 가격 대비 면적 (가성비)
            area = row.get('전용면적(㎡)', 0)
            if area == 0:
                continue

            price_per_sqm = price / area

            # 층수 (높은 층 선호)
            floor = row.get('층', 0)

            # 건축년도 (신축 선호)
            year = row.get('건축년도', 2000)
            building_age = 2025 - year

            # 점수 계산
            score = 0
            reasons = []

            # 1. 가격 (예산의 80% 이하면 좋음)
            if price < budget * 0.8:
                score += 30
                reasons.append(f"Budget fit: ${price/10000:.0f}M under budget")

            # 2. 가성비 (평당 가격)
            if price_per_sqm < 15000000:  # 1500만원/㎡ 이하
                score += 25
                reasons.append(f"Great value: ${price_per_sqm/10000:.0f}/sqm")

            # 3. 층수
            if floor >= 10:
                score += 15
                reasons.append(f"High floor: {floor}F")

            # 4. 신축도
            if building_age < 10:
                score += 20
                reasons.append(f"New building: {building_age}y old")
            elif building_age < 20:
                score += 10

            # 5. 위치 프리미엄
            location = row.get('번지', '')
            if any(premium in str(location) for premium in ['자양', '구의', '광장']):
                score += 10
                reasons.append("Premium location")

            if score >= 50:  # 50점 이상만 추천
                opportunities.append({
                    'score': score,
                    'price': price,
                    'price_usd': price * 0.00075,
                    'area_sqm': area,
                    'area_sqft': area * 10.764,
                    'price_per_sqm': price_per_sqm,
                    'floor': floor,
                    'building_age': building_age,
                    'location': location,
                    'apartment': row.get('단지명', 'Unknown'),
                    'reasons': reasons,
                    'investment_grade': 'A' if score >= 80 else 'B' if score >= 65 else 'C'
                })

        # 점수순 정렬
        opportunities.sort(key=lambda x: x['score'], reverse=True)
        return opportunities

    def compare_global_roi(
        self,
        seoul_price: float,
        seoul_growth: float = 0.06,
        comparison_city: str = 'New York'
    ) -> Dict:
        """글로벌 투자 수익률 비교"""

        # 도시별 역사적 성장률 (2015-2024 평균)
        global_growth_rates = {
            'New York': 0.04,      # 4%
            'Tokyo': 0.02,         # 2%
            'London': 0.05,        # 5%
            'Singapore': 0.03,     # 3%
            'Shanghai': 0.08       # 8% (높은 리스크)
        }

        # 세금/비용
        seoul_costs = {
            'acquisition_tax': 0.04,      # 취득세 4%
            'registration_tax': 0.02,     # 등록세 2%
            'annual_property_tax': 0.01,  # 재산세 1%
            'maintenance': 0.02           # 관리비 2%
        }

        global_costs = {
            'New York': {'total': 0.12},      # 12% (높은 세금)
            'Tokyo': {'total': 0.08},         # 8%
            'London': {'total': 0.10},        # 10%
            'Singapore': {'total': 0.05},     # 5% (낮은 세금)
            'Shanghai': {'total': 0.07}       # 7%
        }

        # 서울 실제 수익률
        seoul_total_cost = sum(seoul_costs.values())
        seoul_net_roi = seoul_growth - seoul_total_cost

        # 비교 도시 실제 수익률
        city_growth = global_growth_rates.get(comparison_city, 0.04)
        city_cost = global_costs.get(comparison_city, {}).get('total', 0.08)
        city_net_roi = city_growth - city_cost

        # 5년 투자 시뮬레이션
        years = 5
        seoul_future = seoul_price * ((1 + seoul_net_roi) ** years)
        city_future = seoul_price * ((1 + city_net_roi) ** years)

        return {
            'seoul': {
                'growth_rate': seoul_growth * 100,
                'costs': seoul_total_cost * 100,
                'net_roi': seoul_net_roi * 100,
                'future_value': seoul_future,
                'profit': seoul_future - seoul_price
            },
            'comparison_city': comparison_city,
            'global': {
                'growth_rate': city_growth * 100,
                'costs': city_cost * 100,
                'net_roi': city_net_roi * 100,
                'future_value': city_future,
                'profit': city_future - seoul_price
            },
            'winner': 'Seoul' if seoul_net_roi > city_net_roi else comparison_city,
            'advantage': abs(seoul_net_roi - city_net_roi) * 100,
            'years': years
        }

    def generate_investment_report(
        self,
        opportunities: List[Dict],
        market_analysis: Dict,
        global_comparison: Dict
    ) -> str:
        """투자 리포트 생성 (영어)"""

        if not opportunities:
            return "No investment opportunities found in current market."

        top_pick = opportunities[0]

        report = f"""INVESTMENT ALERT: Seoul Real Estate Analysis

🎯 TOP PICK - Grade {top_pick['investment_grade']}
Location: {top_pick['location']} - {top_pick['apartment']}
Price: ${top_pick['price_usd']:,.0f} ({top_pick['price']/100000000:.1f}억원)
Size: {top_pick['area_sqft']:.0f} sqft ({top_pick['area_sqm']:.0f}㎡)
Floor: {top_pick['floor']}F, Building: {top_pick['building_age']} years old

💡 Why This Property:
{chr(10).join(['• ' + r for r in top_pick['reasons']])}

📊 MARKET ANALYSIS
Cycle: {market_analysis['cycle'].upper().replace('_', ' ')}
Recommendation: {market_analysis['action']}
Recent Trend: {market_analysis['trend']} ({market_analysis['change_rate']:+.1f}%)
Confidence: {market_analysis['confidence']*100:.0f}%

🌍 GLOBAL COMPARISON
Seoul vs {global_comparison['comparison_city']}:
• Seoul Net ROI: {global_comparison['seoul']['net_roi']:.1f}% annually
• {global_comparison['comparison_city']} ROI: {global_comparison['global']['net_roi']:.1f}% annually
• Winner: {global_comparison['winner']} (by {global_comparison['advantage']:.1f}%)

5-Year Projection:
• Seoul: ${global_comparison['seoul']['future_value']/100000000:.1f}B (profit: ${global_comparison['seoul']['profit']/100000000:.1f}B)
• {global_comparison['comparison_city']}: ${global_comparison['global']['future_value']/100000000:.1f}B

💰 INVESTMENT STRATEGY
1. Entry Point: {market_analysis['action']}
2. Target Hold: 5 years
3. Expected ROI: {global_comparison['seoul']['net_roi']:.1f}% per year
4. Risk Level: {'LOW' if market_analysis['volatility'] < 5 else 'MEDIUM' if market_analysis['volatility'] < 10 else 'HIGH'}

⚡ ACTION ITEMS:
{'• BUY NOW - Market is favorable' if market_analysis['cycle'] == 'bull_market' else '• WAIT - Monitor for better entry point' if market_analysis['cycle'] == 'bear_market' else '• SELECTIVE BUYING - Choose premium locations'}
• Budget allocation: {top_pick['price']/100000000:.1f}억 / 6억
• Reserve: {(600000000 - top_pick['price'])/100000000:.1f}억 for opportunities

🎬 Ready for viral content!
"""

        return report


if __name__ == "__main__":
    # 테스트
    analyzer = InvestmentAnalyzer()

    # 샘플 트렌드 데이터
    trend_data = pd.DataFrame({
        '년월': ['202401', '202402', '202403', '202404', '202405'],
        '평균가격': [1200000000, 1250000000, 1280000000, 1350000000, 1400000000]
    })

    market = analyzer.analyze_market_cycle(trend_data)
    print("Market Analysis:", market)

    global_comp = analyzer.compare_global_roi(600000000)
    print("\nGlobal Comparison:", global_comp)
