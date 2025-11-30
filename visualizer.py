"""
부동산 데이터 시각화 (쇼츠용 세로 영상)
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.font_manager as fm
import numpy as np
from matplotlib import rc
import platform


class RealEstateVisualizer:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        self.setup_korean_font()

        # 쇼츠 비율 (9:16)
        self.fig_width = 6
        self.fig_height = 10.67

    def setup_korean_font(self):
        """Setup English font (no Korean needed)"""
        system = platform.system()

        # Use English fonts only to avoid character issues
        if system == 'Darwin':  # macOS
            fonts = ['Arial', 'Helvetica', 'DejaVu Sans']
        elif system == 'Windows':
            fonts = ['Arial', 'Calibri', 'DejaVu Sans']
        else:  # Linux
            fonts = ['DejaVu Sans', 'Liberation Sans', 'Arial']

        for font in fonts:
            try:
                rc('font', family=font)
                print(f"Font set: {font}")
                break
            except:
                continue

        plt.rcParams['axes.unicode_minus'] = False

    def create_price_trend_animation(self, trend_data, output_file='output/price_trend.mp4', duration=15):
        """가격 추이 애니메이션 생성 (15초)"""
        import os
        os.makedirs(self.output_dir, exist_ok=True)

        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#16213e')

        # 데이터 준비
        months = trend_data['년월'].values
        prices = trend_data['평균가격'].values / 100000000  # 억 단위

        # 애니메이션 설정
        total_frames = duration * 30  # 30fps로 15초
        frames_per_point = total_frames // len(months)

        line, = ax.plot([], [], 'o-', color='#e94560', linewidth=3, markersize=10, markerfacecolor='#ff6b9d')
        title_text = ax.text(0.5, 0.95, 'Seoul Real Estate Price Trend',
                            transform=ax.transAxes,
                            ha='center', va='top',
                            fontsize=24, fontweight='bold', color='white')

        ax.set_xlim(-0.5, len(months) - 0.5)
        ax.set_ylim(prices.min() * 0.9, prices.max() * 1.1)

        ax.set_xlabel('Month', fontsize=14, color='white')
        ax.set_ylabel('Average Price ($100M KRW)', fontsize=14, color='white')

        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # X축 레이블 설정
        ax.set_xticks(range(len(months)))
        ax.set_xticklabels([m[-2:] for m in months], rotation=45, ha='right')

        # 그리드
        ax.grid(True, alpha=0.3, color='white', linestyle='--')

        def init():
            line.set_data([], [])
            return line, title_text

        def animate(frame):
            # 현재까지 표시할 데이터 포인트 수
            current_point = min(frame // frames_per_point, len(months) - 1)

            if current_point > 0:
                x_data = np.arange(current_point + 1)
                y_data = prices[:current_point + 1]
                line.set_data(x_data, y_data)

                # 현재 가격 표시
                current_price = prices[current_point]
                if frame % 10 == 0:  # 가격 텍스트 업데이트
                    for txt in ax.texts[1:]:
                        txt.remove()
                    ax.text(current_point, current_price + 0.5,
                           f'${current_price:.1f}B',
                           ha='center', va='bottom',
                           fontsize=12, fontweight='bold',
                           color='#ff6b9d',
                           bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e', alpha=0.8))

            return line, title_text

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                      frames=total_frames, interval=1000/30,
                                      blit=True, repeat=False)

        # 저장
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=30, metadata=dict(artist='Real-Estate-Shorts'), bitrate=3000)
        anim.save(output_file, writer=writer)
        plt.close()

        print(f"가격 추이 애니메이션 저장: {output_file}")
        return output_file

    def create_hot_deals_chart(self, hot_deals, output_file='output/hot_deals.png'):
        """핫딜 차트 생성"""
        import os
        os.makedirs(self.output_dir, exist_ok=True)

        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#16213e')

        # 데이터 준비
        labels = []
        prices = []

        for idx, row in hot_deals.iterrows():
            dong = row.get('법정동', '지역')
            apt = row.get('아파트', '아파트')
            label = f"{dong}\n{apt}"
            price = row['거래금액_숫자'] / 100000000

            labels.append(label)
            prices.append(price)

        # 바 차트
        colors = ['#e94560', '#ff6b9d', '#ffa07a']
        bars = ax.barh(labels, prices, color=colors[:len(labels)])

        # 제목
        ax.text(0.5, 0.95, '🔥 오늘의 핫딜 TOP 3',
               transform=ax.transAxes,
               ha='center', va='top',
               fontsize=26, fontweight='bold', color='white')

        # 가격 레이블
        for i, (bar, price) in enumerate(zip(bars, prices)):
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                   f'{price:.1f}억',
                   ha='left', va='center',
                   fontsize=18, fontweight='bold', color='white',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='#e94560', alpha=0.8))

        ax.set_xlabel('가격 (억원)', fontsize=14, color='white')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        plt.savefig(output_file, dpi=150, facecolor='#1a1a2e')
        plt.close()

        print(f"핫딜 차트 저장: {output_file}")
        return output_file


if __name__ == "__main__":
    # 테스트용
    import pandas as pd

    # 샘플 데이터로 테스트
    trend_data = pd.DataFrame({
        '년월': ['202401', '202402', '202403', '202404', '202405'],
        '평균가격': [500000000, 520000000, 510000000, 530000000, 540000000],
        '거래건수': [10, 12, 8, 15, 11]
    })

    visualizer = RealEstateVisualizer()
    # visualizer.create_price_trend_animation(trend_data)
