import subprocess
import time
import pandas as pd
import mysql.connector
import os

# 1. 경로 설정
EXE_PATH = "C:/Users/admin/OneDrive/바탕 화면/SF7/최종프로젝트/musagozip/x64/Debug/musagozip.exe"
CSV_PATH = "C:/Users/admin/OneDrive/바탕 화면/SF7/최종프로젝트/sensor_result.csv"

# 2. MySQL 연결 정보
conn = mysql.connector.connect(
    host="localhost",
    user="root",                
    password="1234",            
    database="musago_db"        
)
cursor = conn.cursor()

# 3. 시뮬레이터 실행
print("🚀 센서 시뮬레이터 실행 중...")
subprocess.run([EXE_PATH], check=True)
time.sleep(1)

# 4. CSV 파일 확인
if not os.path.exists(CSV_PATH):
    print("❗ sensor_result.csv 파일이 존재하지 않습니다.")
    exit()

# 5. CSV 읽기
df = pd.read_csv(CSV_PATH, encoding='cp949', quotechar='"')

# 6. sensor_data 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        temperature FLOAT,
        gas FLOAT,
        power FLOAT,
        sound FLOAT,
        risk TEXT
    )
''')

# 6-2. event_log 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        temperature FLOAT,
        gas FLOAT,
        power FLOAT,
        sound FLOAT,
        risk TEXT
    )
''')

# ✅ 기존 데이터 삭제 (최신화)
cursor.execute("DELETE FROM sensor_data")
cursor.execute("DELETE FROM event_log")
conn.commit()

# 7. DB에 삽입
for _, row in df.iterrows():
    # sensor_data에는 모두 저장
    cursor.execute('''
        INSERT INTO sensor_data (timestamp, temperature, gas, power, sound, risk)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (
        row['timestamp'], row['temperature'], row['gas'],
        row['power'], row['sound'], row['risk']
    ))

    # event_log에는 "정상"이 아닌 항목만 저장
    if row['risk'] != "정상":
        cursor.execute('''
            INSERT INTO event_log (timestamp, temperature, gas, power, sound, risk)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            row['timestamp'], row['temperature'], row['gas'],
            row['power'], row['sound'], row['risk']
        ))

conn.commit()
conn.close()
print("✅ 모든 데이터 저장 완료 (sensor_data + 위험 이벤트 event_log)")
