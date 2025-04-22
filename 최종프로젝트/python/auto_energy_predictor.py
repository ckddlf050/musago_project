import time
import os

INTERVAL = 10

print("🔁 에너지 예측 자동화 시작...")

while True:
    print("[에너지 예측] 현재:", time.strftime("%Y-%m-%d %H:%M:%S"))
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/predict_energy.py")
    os.system("python C:/Users/user/Desktop/최종프로젝트/python/save_energy_to_db.py")
    print("[완료] 대기 중...\n")
    time.sleep(INTERVAL)
