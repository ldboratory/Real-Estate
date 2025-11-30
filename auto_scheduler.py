#!/usr/bin/env python3
"""
자동 쇼츠 생성 및 업로드 스케줄러

매일 정해진 시간에 자동으로 쇼츠를 생성하고 업로드 준비

cron 설정 예시:
    # 매일 오전 8시에 실행 (미국 저녁 시간대)
    0 8 * * * cd /Users/dongbin/Projects/Real-Estate && python auto_scheduler.py

사용법:
    python auto_scheduler.py --mode daily
    python auto_scheduler.py --mode test --count 3
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import random
import subprocess


class AutoScheduler:
    """자동 쇼츠 생성 스케줄러"""

    def __init__(self, output_dir='output/scheduled'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.log_file = self.output_dir / 'scheduler.log'
        self.queue_file = self.output_dir / 'upload_queue.json'

        # 생성 전략
        self.strategies = [
            {'lang': 'en', 'country': 'US', 'theme': 'comparison'},
            {'lang': 'en', 'country': 'JP', 'theme': 'bubble_warning'},
            {'lang': 'es', 'country': 'US', 'theme': 'investment_secret'},
            {'lang': 'en', 'country': 'UK', 'theme': 'comparison'},
            {'lang': 'ja', 'country': 'US', 'theme': 'comparison'},
            {'lang': 'en', 'country': 'SG', 'theme': 'bubble_warning'},
            {'lang': 'es', 'country': 'US', 'theme': 'comparison'},
            {'lang': 'en', 'country': 'CN', 'theme': 'investment_secret'},
        ]

    def log(self, message: str):
        """로그 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')

    def generate_daily_shorts(self, count: int = 3) -> list:
        """일일 쇼츠 생성"""
        self.log(f"일일 쇼츠 생성 시작 ({count}개)")

        results = []

        # 랜덤하게 전략 선택 (다양성 확보)
        selected_strategies = random.sample(self.strategies, min(count, len(self.strategies)))

        for i, strategy in enumerate(selected_strategies, 1):
            self.log(f"[{i}/{count}] 생성 중: {strategy['lang']} - {strategy['country']} - {strategy['theme']}")

            try:
                # generate_global_shorts.py 호출
                cmd = [
                    'python',
                    'generate_global_shorts.py',
                    '--lang', strategy['lang'],
                    '--country', strategy['country'],
                    '--theme', strategy['theme'],
                    '--price', str(random.randint(400000000, 800000000))  # 4-8억 랜덤
                ]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=Path(__file__).parent
                )

                if result.returncode == 0:
                    self.log(f"✓ 생성 성공: {strategy}")
                    results.append({
                        'success': True,
                        'strategy': strategy,
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    self.log(f"✗ 생성 실패: {result.stderr}")
                    results.append({
                        'success': False,
                        'strategy': strategy,
                        'error': result.stderr
                    })

            except Exception as e:
                self.log(f"✗ 예외 발생: {e}")
                results.append({
                    'success': False,
                    'strategy': strategy,
                    'error': str(e)
                })

        self.log(f"일일 생성 완료: 성공 {sum(1 for r in results if r['success'])}/{count}")
        return results

    def create_upload_queue(self, results: list):
        """업로드 큐 생성"""
        queue = []

        # 메타데이터 파일 찾기
        meta_files = list((Path('output/global')).glob('*_metadata.json'))

        for meta_file in sorted(meta_files, key=lambda x: x.stat().st_mtime, reverse=True)[:len(results)]:
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                # 업로드 시간 계산 (간격을 두고 업로드)
                upload_time = datetime.now() + timedelta(hours=len(queue) * 2)

                queue_item = {
                    'video_file': metadata['files']['video'],
                    'thumbnail': metadata['files']['thumbnail'],
                    'title': metadata['metadata']['title'],
                    'description': metadata['metadata']['description'],
                    'hashtags': metadata['metadata']['hashtags'],
                    'scheduled_time': upload_time.isoformat(),
                    'status': 'pending'
                }

                queue.append(queue_item)

            except Exception as e:
                self.log(f"메타데이터 읽기 실패: {e}")

        # 큐 저장
        with open(self.queue_file, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)

        self.log(f"업로드 큐 생성 완료: {len(queue)}개")
        return queue

    def generate_cron_script(self):
        """cron 스크립트 생성"""
        script_path = Path(__file__).parent / 'daily_shorts.sh'

        script_content = f"""#!/bin/bash

# 일일 쇼츠 자동 생성 스크립트
# 매일 오전 8시 실행 (미국 저녁 시간대)

cd "{Path(__file__).parent}"

# Python 가상환경 활성화 (필요시)
# source .venv/bin/activate

# 쇼츠 생성 (하루 3개)
python auto_scheduler.py --mode daily --count 3

# 로그 정리 (30일 이상 된 로그 삭제)
find output/scheduled -name "*.log" -mtime +30 -delete

echo "Daily shorts generation completed at $(date)"
"""

        with open(script_path, 'w') as f:
            f.write(script_content)

        # 실행 권한 부여
        os.chmod(script_path, 0o755)

        cron_command = f"0 8 * * * {script_path} >> {self.output_dir}/cron.log 2>&1"

        self.log(f"Cron 스크립트 생성 완료: {script_path}")
        self.log(f"\nCron 설정 명령어:")
        self.log(f"  crontab -e")
        self.log(f"  {cron_command}")

        return script_path

    def analyze_performance(self):
        """성과 분석 (시뮬레이션)"""
        self.log("\n=== 예상 성과 분석 ===")

        # 시뮬레이션 데이터
        daily_shorts = 3
        avg_views_per_short = 50000  # 평균 5만 조회
        cpm = 5  # $5 CPM
        days = 30

        total_shorts = daily_shorts * days
        total_views = total_shorts * avg_views_per_short
        revenue = (total_views / 1000) * cpm

        self.log(f"월간 예상:")
        self.log(f"  - 쇼츠 수: {total_shorts}개")
        self.log(f"  - 총 조회수: {total_views:,}")
        self.log(f"  - 예상 수익: ${revenue:,.2f}")
        self.log(f"  - 채널 10개 운영 시: ${revenue * 10:,.2f}")

        return {
            'total_shorts': total_shorts,
            'total_views': total_views,
            'revenue': revenue
        }


def main():
    parser = argparse.ArgumentParser(description='자동 쇼츠 스케줄러')
    parser.add_argument('--mode', default='daily',
                       choices=['daily', 'test', 'analyze', 'setup-cron'],
                       help='실행 모드')
    parser.add_argument('--count', type=int, default=3,
                       help='생성할 쇼츠 수')

    args = parser.parse_args()

    scheduler = AutoScheduler()

    if args.mode == 'daily':
        # 일일 모드: 쇼츠 생성 + 업로드 큐 생성
        results = scheduler.generate_daily_shorts(args.count)
        scheduler.create_upload_queue(results)

    elif args.mode == 'test':
        # 테스트 모드: 소량 생성
        print(f"테스트 모드: {args.count}개 생성")
        results = scheduler.generate_daily_shorts(args.count)
        scheduler.log(f"테스트 결과: {json.dumps(results, indent=2, ensure_ascii=False)}")

    elif args.mode == 'analyze':
        # 분석 모드: 성과 예측
        scheduler.analyze_performance()

    elif args.mode == 'setup-cron':
        # Cron 설정 모드
        scheduler.generate_cron_script()


if __name__ == "__main__":
    main()
