import pandas as pd
import joblib

df = pd.read_csv("C:/Users/user/Desktop/데이터 수정/최종프로젝트/shared/data/sensor_result.csv")
model = joblib.load("C:/Users/user/Desktop/데이터 수정/최종프로젝트/python/models/anomaly_model.pkl")
X = df[["temperature", "humidity", "co2", "vibration", "energy_usage"]]
df["anomaly_prediction"] = model.predict(X)
df.to_csv("C:/Users/user/Desktop/데이터 수정/최종프로젝트/shared/data/anomaly_prediction.csv", index=False, encoding="utf-8-sig")
print("✅ anomaly_prediction.csv 저장 완료!")
