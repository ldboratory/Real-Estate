#!/usr/bin/env python3
"""
프로 투자 분석 쇼츠 생성기
Professional Investment Analysis Shorts Generator

무료 고품질 툴 사용:
- pyttsx3: 자연스러운 영어 음성
- MoviePy: 프로 영상 편집
- 실제 투자 가치 분석

사용법:
    python generate_pro_shorts.py
    python generate_pro_shorts.py --budget 800000000 --city "New York"
"""

import argparse
from pathlib import Path
import os

from data_processor import RealEstateDataProcessor
from investment_analyzer import InvestmentAnalyzer
from pro_voice_generator import ProVoiceGenerator
from pro_video_creator import ProVideoCreator
from global_data_api import GlobalRealEstateAPI


def main():
    parser = argparse.ArgumentParser(description='Pro Investment Shorts Generator')
    parser.add_argument('--budget', type=int, default=600000000,
                       help='Investment budget in KRW (default: 600M = $450K)')
    parser.add_argument('--city', default='New York',
                       choices=['New York', 'Tokyo', 'London', 'Singapore', 'Shanghai'],
                       help='Comparison city')
    parser.add_argument('--data', default=None,
                       help='Excel data file (optional)')

    args = parser.parse_args()

    print("="*70)
    print("🎬 PROFESSIONAL INVESTMENT ANALYSIS SHORTS GENERATOR")
    print("="*70)
    print(f"Budget: ${args.budget * 0.00075:,.0f} (₩{args.budget/100000000:.1f}억)")
    print(f"Comparison: Seoul vs {args.city}")
    print("="*70)

    # 1. 데이터 로드
    print("\n[1/6] Loading real estate data...")
    base_dir = Path(__file__).parent

    if args.data:
        excel_file = args.data
    else:
        # 자동 xlsx 파일 찾기
        xlsx_files = list(base_dir.glob("*.xlsx"))
        if not xlsx_files:
            print("❌ No Excel data file found!")
            print("Download data from KB real estate or provide --data argument")
            return
        excel_file = str(xlsx_files[0])

    processor = RealEstateDataProcessor(excel_file)
    processor.load_data()
    processor.clean_data()

    # 2. 투자 분석
    print("\n[2/6] Analyzing investment opportunities...")
    analyzer = InvestmentAnalyzer()

    # 투자 기회 발견
    opportunities = analyzer.find_investment_opportunities(
        processor.df,
        budget=args.budget,
        min_roi=0.06
    )

    if not opportunities:
        print("❌ No investment opportunities found in budget range")
        return

    top_pick = opportunities[0]
    print(f"\n✓ Found {len(opportunities)} opportunities")
    print(f"TOP PICK: {top_pick['apartment']} - Grade {top_pick['investment_grade']}")
    print(f"Price: ${top_pick['price_usd']:,.0f} | Score: {top_pick['score']}/100")

    # 시장 분석
    trend_data = processor.calculate_price_trend()
    if trend_data is not None and len(trend_data) > 0:
        market_analysis = analyzer.analyze_market_cycle(trend_data)
        print(f"\nMarket Cycle: {market_analysis['cycle']}")
        print(f"Recommendation: {market_analysis['action']}")
    else:
        market_analysis = {
            'cycle': 'sideways',
            'action': 'HOLD_POSITION',
            'change_rate': 0,
            'volatility': 5,
            'confidence': 0.5
        }

    # 글로벌 비교
    global_api = GlobalRealEstateAPI()
    comparison = global_api.get_global_comparison(top_pick['price'])

    # 도시 코드 변환
    city_code_map = {
        'New York': 'US',
        'Tokyo': 'JP',
        'London': 'UK',
        'Singapore': 'SG',
        'Shanghai': 'CN'
    }
    city_code = city_code_map.get(args.city, 'US')

    global_roi = analyzer.compare_global_roi(
        top_pick['price'],
        comparison_city=args.city
    )

    # 3. 투자 리포트 생성
    print("\n[3/6] Generating investment report...")
    report = analyzer.generate_investment_report(
        opportunities[:3],  # Top 3
        market_analysis,
        global_roi
    )

    print("\n" + "="*70)
    print(report)
    print("="*70)

    # 4. 음성 생성 (프로 품질)
    print("\n[4/6] Generating professional narration...")
    voice_gen = ProVoiceGenerator()

    # 투자 스크립트 (간결하고 임팩트 있게)
    investment_script = f"""
Investment Alert! Seoul real estate analysis.

Top pick: Grade {top_pick['investment_grade']} opportunity.
Location: {top_pick['apartment']}.
Price: {top_pick['price_usd']:.0f} thousand dollars.
Size: {top_pick['area_sqft']:.0f} square feet.

Why this property?
{'. '.join(top_pick['reasons'][:3])}.

Market analysis: {market_analysis['cycle'].replace('_', ' ')}.
Recommendation: {market_analysis['action'].replace('_', ' ')}.

Seoul versus {args.city}:
Seoul net ROI: {global_roi['seoul']['net_roi']:.1f} percent annually.
{args.city}: {global_roi['global']['net_roi']:.1f} percent.

Winner: {global_roi['winner']} by {global_roi['advantage']:.1f} percent!

Five year projection: {global_roi['seoul']['profit']/100000000:.1f} billion won profit.

Action: {'Buy now' if market_analysis['cycle'] == 'bull_market' else 'Wait for better timing' if market_analysis['cycle'] == 'bear_market' else 'Selective buying'}.

Check it out!
    """.strip()

    audio_file = voice_gen.generate_professional_voice(
        investment_script,
        output_file='output/pro/investment_narration.mp3',
        style='professional'
    )

    if not audio_file:
        print("❌ Voice generation failed")
        return

    print(f"✓ Narration: {audio_file}")

    # 5. 영상 생성 (프로 품질)
    print("\n[5/6] Creating professional video...")
    video_creator = ProVideoCreator()

    # 데이터 시각화
    viz_file = video_creator.create_data_visualization(
        top_pick,
        market_analysis,
        duration=10.0
    )

    if not viz_file:
        print("❌ Video creation failed")
        return

    # 6. 최종 쇼츠 조립
    print("\n[6/6] Assembling final shorts...")

    final_shorts = video_creator.create_final_shorts(
        intro_text=("INVESTMENT ALERT", f"Seoul vs {args.city}"),
        data_viz_file=viz_file,
        audio_file=audio_file,
        outro_text=f"Grade {top_pick['investment_grade']} Deal!",
        output_file='output/pro/investment_shorts_final.mp4'
    )

    if final_shorts:
        print("\n" + "="*70)
        print("✅ PROFESSIONAL SHORTS CREATED!")
        print("="*70)
        print(f"Output: {final_shorts}")
        print(f"\n📊 Investment Grade: {top_pick['investment_grade']}")
        print(f"💰 Budget Used: ${top_pick['price_usd']:,.0f} / ${args.budget*0.00075:,.0f}")
        print(f"📈 Expected ROI: {global_roi['seoul']['net_roi']:.1f}% per year")
        print(f"🌍 Advantage over {args.city}: {global_roi['advantage']:.1f}%")
        print(f"\n🎬 Ready to upload to YouTube Shorts!")
        print("="*70)

        # 리포트 저장
        report_file = Path('output/pro/investment_report.txt')
        report_file.write_text(report + f"\n\nScript:\n{investment_script}")
        print(f"\n📄 Report saved: {report_file}")

    else:
        print("❌ Final assembly failed")


if __name__ == "__main__":
    main()
