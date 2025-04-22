import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# 🔹 모델 저장 경로
os.makedirs("models", exist_ok=True)

# 🔹 데이터 불러오기
df = pd.read_csv("cpp/sensor_simulator/sensor_simulator/data/sensor_result.csv")

# 🔹 위험도 점수 계산 (센서 상태 기준)
def risk_level(row):
    status_list = [row["temp_status"], row["hum_status"], row["co2_status"],
                   row["vib_status"], row["energy_status"]]
    red_count = status_list.count("red")
    yellow_count = status_list.count("yellow")

    if red_count >= 2:
        return "높음"
    elif red_count == 1 or yellow_count >= 2:
        return "중간"
    else:
        return "낮음"

df["risk_level"] = df.apply(risk_level, axis=1)

# 🔹 모델 학습
X = df[["temperature", "humidity", "co2", "vibration", "energy_usage"]]
y = df["risk_level"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 🔹 모델 저장
joblib.dump(model, "models/risk_level_model.pkl")
print("✅ 복합 위험도 예측 모델 저장 완료: models/risk_level_model.pkl")
