import pandas as pd
import joblib

# 🔹 경로
INPUT = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/sensor_result.csv"
OUTPUT = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/energy_prediction.csv"
MODEL = "C:/Users/user/Desktop/최종프로젝트/models/energy_model.pkl"

# 🔹 모델 로드
model = joblib.load(MODEL)

# 🔹 데이터 로드
df = pd.read_csv(INPUT)
X = df[["energy_usage"]]

# 🔹 예측
df["energy_prediction"] = model.predict(X)

# 🔹 저장
df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
print("✅ 에너지 예측 결과 저장 완료 → energy_prediction.csv")
