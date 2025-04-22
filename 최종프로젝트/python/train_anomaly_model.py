import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# 🔹 모델 저장 폴더
os.makedirs("models", exist_ok=True)

# 🔹 데이터 불러오기
df = pd.read_csv("cpp/sensor_simulator/sensor_simulator/data/sensor_result.csv")

# 🔹 입력값 설정
X = df[["temperature", "humidity", "co2", "vibration", "energy_usage"]]

# 🔹 Isolation Forest 모델 학습
model = IsolationForest(contamination=0.1, random_state=42)  # 상위 10%를 이상치로 간주
model.fit(X)

# 🔹 모델 저장
joblib.dump(model, "models/anomaly_model.pkl")
print("✅ 이상치 탐지 모델 저장 완료: models/anomaly_model.pkl")
