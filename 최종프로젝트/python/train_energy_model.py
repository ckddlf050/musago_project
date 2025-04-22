import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# 🔹 데이터 불러오기
df = pd.read_csv("cpp/sensor_simulator/sensor_simulator/data/sensor_result.csv")

# 🔹 라벨 생성
def label_energy(usage):
    if usage > 1000:
        return "과소비"
    elif usage > 800:
        return "주의"
    else:
        return "정상"

df["energy_label"] = df["energy_usage"].apply(label_energy)

# 🔹 입력/출력
X = df[["energy_usage"]]
y = df["energy_label"]

# 🔹 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 🔹 저장
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/energy_model.pkl")
print("✅ 에너지 상태 예측 모델 저장 완료: models/energy_model.pkl")
