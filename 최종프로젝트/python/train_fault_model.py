import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# 🔹 저장 폴더 준비
os.makedirs("models", exist_ok=True)

# 🔹 데이터 불러오기
df = pd.read_csv("cpp/sensor_simulator/sensor_simulator/data/sensor_result.csv")

# 🔹 고장 라벨 생성: 진동이 7.5 이상이면 80% 확률로 고장
def simulate_fault(vib):
    if vib >= 7.5:
        return "fault" if random.random() < 0.8 else "normal"
    else:
        return "normal"

df["label"] = df["vibration"].apply(simulate_fault)

# 🔹 학습
X = df[["vibration"]]
y = df["label"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 🔹 모델 저장
joblib.dump(model, "models/fault_model.pkl")
print("✅ 고장 예측 모델 저장 완료: models/fault_model.pkl")
