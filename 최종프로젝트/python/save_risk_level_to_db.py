import pandas as pd
import mysql.connector

# 🔹 CSV 불러오기
df = pd.read_csv("C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/risk_level_prediction.csv")

# 🔹 MySQL 연결
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",           # ← 본인 비밀번호로 수정
    database="musago_db"       # ← 본인 DB 이름으로 수정
)
cursor = conn.cursor()

# 🔹 DB 삽입
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO risk_level_log (
            timestamp, temperature, humidity, co2, vibration, energy_usage, risk_level_prediction
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row["timestamp"],
        row["temperature"],
        row["humidity"],
        row["co2"],
        row["vibration"],
        row["energy_usage"],
        row["risk_level_prediction"]
    ))

conn.commit()
cursor.close()
conn.close()

print(f"✅ {len(df)}건의 복합 위험 등급 데이터를 risk_level_log 테이블에 저장 완료!")
