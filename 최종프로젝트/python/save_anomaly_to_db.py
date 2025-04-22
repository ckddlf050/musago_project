import pandas as pd
import mysql.connector

# 🔹 CSV 파일 절대 경로
df = pd.read_csv("C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/anomaly_prediction.csv")
filtered_df = df[df["anomaly_prediction"] == "이상"].copy()

# 🔹 MySQL 연결
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",        # ← 본인의 비밀번호
    database="musago_db"    # ← 본인의 DB 이름
)
cursor = conn.cursor()

# 🔹 테이블에 저장
for _, row in filtered_df.iterrows():
    cursor.execute("""
        INSERT INTO anomaly_log (
            timestamp, temperature, humidity, co2, vibration, energy_usage, anomaly_prediction
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row["timestamp"], row["temperature"], row["humidity"], row["co2"],
        row["vibration"], row["energy_usage"], row["anomaly_prediction"]
    ))

conn.commit()
cursor.close()
conn.close()

print(f"✅ {len(filtered_df)}건의 이상 데이터를 anomaly_log 테이블에 저장 완료!")
