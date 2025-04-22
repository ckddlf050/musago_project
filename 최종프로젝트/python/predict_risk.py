import pandas as pd
import joblib
import os

# 🔹 경로 지정
INPUT_CSV = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/sensor_result.csv"
MODEL_PATH = "C:/Users/user/Desktop/최종프로젝트/models/risk_model.pkl"
OUTPUT_CSV = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/risk_prediction.csv"

# 🔹 모델 로드
model = joblib.load(MODEL_PATH)

# 🔹 CSV 로드
df = pd.read_csv(INPUT_CSV)

# 🔹 입력 데이터만 추출
X = df[["temperature", "humidity", "co2", "vibration", "energy_usage"]]

# 🔹 예측 수행
predictions = model.predict(X)

# 🔹 예측 결과 저장
df["risk_prediction"] = predictions
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print("✅ 예측 완료! 결과 저장:", OUTPUT_CSV)
