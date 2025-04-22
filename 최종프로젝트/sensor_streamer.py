import pandas as pd
import time
import os
from datetime import datetime

# 🔹 입력: 센서 시뮬레이터가 만든 전체 결과 파일
source_path = "C:/Users/user/Desktop/산업재해데이터/sensor_result.csv"

# 🔹 출력: Dashboard가 참조할 실시간 데이터 파일
target_path = "C:/Users/user/Desktop/산업재해데이터/sensor_result_realtime.csv"

# 🔄 기존 실시간 파일이 있으면 삭제
if os.path.exists(target_path):
    os.remove(target_path)

# 🔹 전체 데이터 로딩
try:
    df = pd.read_csv(source_path, encoding="cp949")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
except Exception as e:
    print(f"[❌ 데이터 로딩 실패] {e}")
    exit()

# 🔹 헤더만 먼저 쓰기
df.iloc[:0].to_csv(target_path, index=False, encoding="cp949")

# 🔁 실시간처럼 한 줄씩 추가
for i in range(len(df)):
    row = df.iloc[[i]]  # DataFrame 형태 유지
    try:
        row.to_csv(target_path, mode='a', index=False, header=False, encoding="cp949")
        print(f"⏱ {datetime.now().strftime('%H:%M:%S')} | 저장됨: {row.iloc[0]['timestamp']}")
    except Exception as e:
        print(f"[❗ 저장 실패] {e}")
    time.sleep(1.0)  # 1초 간격
