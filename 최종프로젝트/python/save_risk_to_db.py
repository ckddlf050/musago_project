import pandas as pd
import mysql.connector

# 🔹 데이터 불러오기
df = pd.read_csv("C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/risk_prediction.csv")

# 🔹 'safe'가 아닌 데이터만 필터링
filtered_df = df[df["risk_prediction"] != "safe"].copy()

# 🔹 MySQL 연결
conn = mysql.connector.connect(
    host="localhost",
    user="root",              # ← 본인의 사용자명
    password="1234",          # ← 본인의 비밀번호
    database="musago_db"      # ← 본인의 DB 이름
)
cursor = conn.cursor()

# 🔹 삽입 쿼리 실행
for _, row in filtered_df.iterrows():
    cursor.execute("""
        INSERT INTO event_log (timestamp, temperature, humidity, co2, vibration, energy_usage, risk_prediction)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row["timestamp"],                # 문자열 그대로 사용 (예: "2025-04-18 13:25:00")
        row["temperature"],
        row["humidity"],
        row["co2"],
        row["vibration"],
        row["energy_usage"],
        row["risk_prediction"]
    ))

# 🔹 커밋 & 종료
conn.commit()
cursor.close()
conn.close()

print(f"✅ {len(filtered_df)}건의 위험 이벤트를 event_log 테이블에 저장 완료!")
