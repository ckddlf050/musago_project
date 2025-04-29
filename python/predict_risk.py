import pandas as pd
import joblib

# 데이터 로드
df = pd.read_csv("C:/Users/user/Desktop/데이터 수정/최종프로젝트/shared/data/sensor_result.csv")

# 모델 로드
model = joblib.load("C:/Users/user/Desktop/데이터 수정/최종프로젝트/python/models/risk_model.pkl")

# 예측
X = df[["temperature", "humidity", "co2", "vibration", "energy_usage"]]
df["risk_prediction"] = model.predict(X)

# 저장
df.to_csv("C:/Users/user/Desktop/데이터 수정/최종프로젝트/shared/data/risk_prediction.csv", index=False, encoding="utf-8-sig")
print("✅ 위험 예측 완료: shared/data/risk_prediction.csv")
