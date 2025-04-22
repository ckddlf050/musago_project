import pandas as pd
import joblib
import os

# 🔹 경로 설정
INPUT_CSV = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/sensor_result.csv"
MODEL_PATH = "C:/Users/user/Desktop/최종프로젝트/models/fault_model.pkl"
OUTPUT_CSV = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/fault_prediction.csv"

# 🔹 모델 로드
model = joblib.load(MODEL_PATH)

# 🔹 데이터 로드
df = pd.read_csv(INPUT_CSV)

# 🔹 진동 데이터만 입력값으로 사용
X = df[["vibration"]]  # ← 고장 모델은 진동만 사용

# 🔹 예측 수행
df["fault_prediction"] = model.predict(X)

# 🔹 결과 저장
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print("✅ 고장 예측 완료 → fault_prediction.csv 저장됨!")
