# main_total.py

import subprocess
import time
import os

def run_step(description, command, shell=False):
    print(f"\n▶ {description} 중...")
    try:
        result = subprocess.run(command, check=True, shell=shell)
    except subprocess.CalledProcessError:
        print(f"❌ {description} 실패!")
        exit()
    print(f"✅ {description} 완료.")

# 기준 경로
BASE_DIR = "C:/Users/user/Desktop/데이터 수정/최종프로젝트"

# 1️⃣ 센서 시뮬레이터 실행 (.exe)
simulator_path = os.path.join(BASE_DIR, "cpp/sensor_simulator/x64/Debug/sensor_simulator.exe")
run_step("센서 시뮬레이터 실행", [simulator_path])

# 2️⃣ AI 예측 (단 1회 실행)
predictor_path = os.path.join(BASE_DIR, "python/single_run_predictor.py")
run_step("AI 예측 수행", ["python", predictor_path])

# 3️⃣ 리포트 생성
report_path = os.path.join(BASE_DIR, "python/report_generator.py")
run_step("PDF 리포트 생성", ["python", report_path])

print("\n🎉 모든 작업 완료! PDF 리포트를 확인하세요.")
