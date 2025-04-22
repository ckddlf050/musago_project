import pandas as pd
import mysql.connector

# 🔹 데이터 로드
df = pd.read_csv("C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/fault_prediction.csv")

# 🔹 fault만 필터링
filtered_df = df[df["fault_prediction"] == "fault"].copy()

def convert_label(label):
    return "🔴 고장" if label == "fault" else "🟢 정상"

filtered_df["fault_prediction"] = filtered_df["fault_prediction"].apply(convert_label)

# 🔹 MySQL 연결
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",        # ← 본인 비번
    database="musago_db"    # ← 본인 DB 이름
)
cursor = conn.cursor()

# 🔹 삽입 (timestamp는 문자열 그대로 사용)
for _, row in filtered_df.iterrows():
    cursor.execute("""
        INSERT INTO fault_log (timestamp, vibration, fault_prediction)
        VALUES (%s, %s, %s)
    """, (
        row["timestamp"],     # ex: '2025-04-18 14:00:02'
        row["vibration"],
        row["fault_prediction"]
    ))

conn.commit()
cursor.close()
conn.close()

print(f"✅ {len(filtered_df)}건의 고장 데이터를 fault_log 테이블에 저장 완료!")
