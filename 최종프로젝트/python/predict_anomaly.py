import pandas as pd
import joblib

# 🔹 경로
INPUT = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/sensor_result.csv"
OUTPUT = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/anomaly_prediction.csv"
MODEL = "C:/Users/user/Desktop/최종프로젝트/models/anomaly_model.pkl"

# 🔹 모델 로드
model = joblib.load(MODEL)

# 🔹 데이터 로드
df = pd.read_csv(INPUT)
X = df[["temperature", "humidity", "co2", "vibration", "energy_usage"]]

# 🔹 예측 수행 (-1: 이상치, 1: 정상)
pred = model.predict(X)
df["anomaly_prediction"] = ["이상" if p == -1 else "정상" for p in pred]

# 🔹 저장
df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
print("✅ 이상치 탐지 결과 저장 완료 → anomaly_prediction.csv")
