import os
import pandas as pd
import mysql.connector
from datetime import datetime

# 🔹 MySQL 연결 정보
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "musago_db"
}

# 🔹 저장 경로
BASE_DIR = "C:/Users/user/Desktop/데이터 수정/최종프로젝트/csv/sensor_error_log"
os.makedirs(BASE_DIR, exist_ok=True)

# 🔹 MySQL 연결 (event_log 읽기용)
conn = mysql.connector.connect(**db_config)

# 🔹 event_log 데이터 최근 50개 가져오기
df = pd.read_sql("SELECT * FROM event_log ORDER BY timestamp DESC LIMIT 50", con=conn)
conn.close()

# 🔹 sensor_error_log 초기화
error_logs = []

# 🔹 각 센서별 이상 감지
for sensor in ["temperature", "humidity", "co2", "vibration", "energy_usage"]:
    values = df[sensor].values[::-1]  # 시간순 정렬 (오래된 것부터)

    # 변화량 체크
    diffs = [abs(values[i] - values[i-1]) for i in range(1, len(values))]
    avg_diff = sum(diffs) / len(diffs) if diffs else 0

    # 최대값 체크
    max_value = max(values)

    is_stuck = avg_diff < 0.1  # 변화량이 거의 없음
    is_spike = False

    # 센서별 특이 튐 조건
    if sensor == "temperature" and max_value > 100:
        is_spike = True
    elif sensor == "humidity" and (max_value > 100 or min(values) < 0):
        is_spike = True
    elif sensor == "co2" and max_value > 5000:
        is_spike = True
    elif sensor == "vibration" and max_value > 20:
        is_spike = True
    elif sensor == "energy_usage" and max_value > 2000:
        is_spike = True

    if is_stuck or is_spike:
        error_type = []
        if is_stuck:
            error_type.append("변화 없음")
        if is_spike:
            error_type.append("값 튐")
        error_logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sensor": sensor,
            "error_type": ", ".join(error_type)
        })

# 🔹 결과 저장
if error_logs:
    df_errors = pd.DataFrame(error_logs)
    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # CSV 저장
    df_errors.to_csv(os.path.join(BASE_DIR, f"{now_str}.csv"), index=False, encoding="utf-8-sig")
    df_errors.to_csv(os.path.join(BASE_DIR, "latest.csv"), index=False, encoding="utf-8-sig")
    print(f"✅ 센서 이상 감지 완료 (CSV 저장): {len(df_errors)}건")

    # MySQL 저장
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    for error in error_logs:
        cursor.execute("""
            INSERT INTO sensor_error_log (timestamp, sensor, error_type)
            VALUES (%s, %s, %s)
        """, (
            error["timestamp"],
            error["sensor"],
            error["error_type"]
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ 센서 이상 감지 완료 (MySQL 저장): {len(df_errors)}건")
else:
    print("✅ 센서 이상 없음")
