import pandas as pd
import joblib
import os

# 🔹 경로 설정
INPUT_CSV = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/sensor_result.csv"
MODEL_PATH = "C:/Users/user/Desktop/최종프로젝트/models/risk_level_model.pkl"
OUTPUT_CSV = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/risk_level_prediction.csv"

# 🔹 모델 로드
model = joblib.load(MODEL_PATH)

# 🔹 센서 데이터 불러오기
df = pd.read_csv(INPUT_CSV)

# 🔹 입력값
X = df[["temperature", "humidity", "co2", "vibration", "energy_usage"]]

# 🔹 예측 수행
df["risk_level_prediction"] = model.predict(X)

# 🔹 결과 저장
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print(f"✅ 복합 위험도 예측 완료 → {OUTPUT_CSV}")
