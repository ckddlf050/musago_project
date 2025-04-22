import os
import time

INTERVAL = 10  # 반복 주기 (초)

sensor_result_path = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/sensor_result.csv"

print("🚀 통합 예측 자동화 시스템 시작 (Ctrl+C로 종료)")

while True:
    print("\n📅 현재 시간:", time.strftime("%Y-%m-%d %H:%M:%S"))

    # 1️⃣ 센서 시뮬레이터 실행
    print("📡 센서 데이터 생성 중...")
    os.chdir("C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/x64/Debug")
    os.system("sensor_simulator.exe")
    os.chdir("../../../..")

    # 1.5️⃣ 센서 결과 생성 완료 대기 (최대 3초까지 반복 확인)
    for _ in range(30):
        if os.path.exists(sensor_result_path) and os.path.getsize(sensor_result_path) > 0:
            print(f"🟢 sensor_result.csv 생성 완료: {time.ctime(os.path.getmtime(sensor_result_path))}")
            break
        time.sleep(0.1)
    else:
        print("❗ sensor_result.csv 생성 실패 또는 시간 초과")
        continue

    # 2️⃣ 위험 예측 + 저장
    print("🧠 위험 예측 중...")
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/predict_risk.py")
    time.sleep(0.5)
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/save_risk_to_db.py")
    time.sleep(0.5)

    # 3️⃣ 고장 예측 + 저장
    print("🛠 고장 예측 중...")
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/predict_fault.py")
    time.sleep(0.5)
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/save_fault_to_db.py")
    time.sleep(0.5)

    # 4️⃣ 복합 위험 등급 예측 + 저장
    print("📊 위험 등급 예측 중...")
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/predict_risk_level.py")
    time.sleep(0.5)
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/save_risk_level_to_db.py")
    time.sleep(0.5)

    # 5️⃣ 이상치 탐지 + 저장
    print("🚨 이상치 탐지 중...")
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/predict_anomaly.py")
    time.sleep(0.5)
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/save_anomaly_to_db.py")
    time.sleep(0.5)

    # 6️⃣ 에너지 예측 + 저장
    print("⚡ 에너지 예측 중...")
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/predict_energy.py")
    time.sleep(0.5)
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/save_energy_to_db.py")
    time.sleep(0.5)

    print("✅ 모든 예측 완료. 다음 주기까지 대기 중...\n")
    time.sleep(INTERVAL)
