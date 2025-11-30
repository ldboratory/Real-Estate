"""
부동산 실거래 데이터 분석 및 전처리
"""
import pandas as pd
import numpy as np
from datetime import datetime


class RealEstateDataProcessor:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.df = None
        self.top_deals = None

    def load_data(self):
        """엑셀 파일 로드"""
        print(f"데이터 로딩 중: {self.excel_file}")
        # KB 실거래 데이터는 보통 12번째 행부터 실제 헤더가 시작됨
        self.df = pd.read_excel(self.excel_file, header=12)
        print(f"총 {len(self.df)}개의 거래 데이터 로드 완료")
        return self.df

    def analyze_data(self):
        """데이터 분석"""
        print("\n데이터 컬럼:", self.df.columns.tolist())
        print("\n데이터 샘플:")
        print(self.df.head())
        print("\n데이터 정보:")
        print(self.df.info())

    def clean_data(self):
        """데이터 정리"""
        # 결측치 제거
        original_len = len(self.df)

        # 거래금액 컬럼 찾기 (만원 단위 포함)
        price_col = None
        for col in self.df.columns:
            if '거래금액' in col:
                price_col = col
                break

        if price_col:
            self.df = self.df.dropna(subset=[price_col])

        print(f"\n결측치 제거: {original_len} -> {len(self.df)}개")

        # 거래금액 숫자로 변환 (쉼표 제거, 만원 → 원)
        if price_col:
            self.df['거래금액_숫자'] = self.df[price_col].astype(str).str.replace(',', '').str.replace(' ', '')
            self.df['거래금액_숫자'] = pd.to_numeric(self.df['거래금액_숫자'], errors='coerce')
            # 만원 단위를 원 단위로 변환
            self.df['거래금액_숫자'] = self.df['거래금액_숫자'] * 10000
            print(f"거래금액 변환 완료: {price_col} → 거래금액_숫자 (원 단위)")

        # 날짜 처리
        date_columns = [col for col in self.df.columns if '년' in col or '날짜' in col or '계약' in col]
        if date_columns:
            print(f"날짜 관련 컬럼: {date_columns}")

        return self.df

    def find_hot_deals(self, top_n=3, max_price=600000000):
        """핫딜 찾기 (6억 이하)"""
        if '거래금액_숫자' not in self.df.columns:
            print("거래금액 데이터가 없습니다.")
            return None

        # 6억 이하 필터링
        filtered_df = self.df[self.df['거래금액_숫자'] <= max_price].copy()

        # 최근 거래 우선
        if '계약년월' in self.df.columns and '계약일' in self.df.columns:
            filtered_df['계약날짜'] = pd.to_datetime(
                filtered_df['계약년월'].astype(str) + filtered_df['계약일'].astype(str).str.zfill(2),
                format='%Y%m%d',
                errors='coerce'
            )
            filtered_df = filtered_df.sort_values('계약날짜', ascending=False)

        # 상위 N개 선택
        self.top_deals = filtered_df.head(top_n)

        print(f"\n핫딜 TOP {top_n} (6억 이하):")
        for idx, row in self.top_deals.iterrows():
            price = row['거래금액_숫자'] / 100000000  # 억 단위
            dong = row.get('번지', row.get('법정동', '지역'))
            apt = row.get('단지명', row.get('아파트', '아파트'))
            print(f"- {dong} {apt}: {price:.1f}억")

        return self.top_deals

    def calculate_price_trend(self):
        """가격 추이 계산"""
        if '계약년월' in self.df.columns and '거래금액_숫자' in self.df.columns:
            # 월별 평균 가격
            self.df['년월'] = self.df['계약년월'].astype(str)
            trend = self.df.groupby('년월')['거래금액_숫자'].agg(['mean', 'count']).reset_index()
            trend.columns = ['년월', '평균가격', '거래건수']
            trend = trend.sort_values('년월')

            print("\n월별 가격 추이:")
            print(trend)

            return trend
        return None

    def generate_script(self):
        """Generate English voice script"""
        if self.top_deals is None or len(self.top_deals) == 0:
            return "No hot deals available."

        script = "Today's Seoul real estate hot deals! "

        for idx, (_, row) in enumerate(self.top_deals.iterrows(), 1):
            dong = row.get('번지', row.get('법정동', 'Area'))
            apt = row.get('단지명', row.get('아파트', 'Apartment'))
            price = row['거래금액_숫자'] / 100000000
            price_usd = price * 0.75  # Approximate USD (1억 = $75K)
            area = row.get('전용면적(㎡)', row.get('전용면적', ''))

            script += f"Number {idx}, {apt}, "
            if area:
                sqft = area * 10.764  # ㎡ to sqft
                script += f"{sqft:.0f} square feet, "
            script += f"${price_usd:.0f}K! "

        script += "Check them out now!"

        print(f"\nGenerated script:\n{script}")
        return script


if __name__ == "__main__":
    # 테스트 실행
    processor = RealEstateDataProcessor("광진구_20251130215706.xlsx")
    processor.load_data()
    processor.analyze_data()
    processor.clean_data()
    processor.find_hot_deals(top_n=3)
    processor.calculate_price_trend()
    processor.generate_script()
