import pandas as pd
import joblib

df = pd.read_csv("C:/Users/user/Desktop/데이터 수정/최종프로젝트/shared/data/sensor_result.csv")
model = joblib.load("C:/Users/user/Desktop/데이터 수정/최종프로젝트/python/models/energy_model.pkl")
X = df[["temperature", "humidity", "co2", "vibration", "energy_usage"]]
df["energy_prediction"] = model.predict(X)
df.to_csv("C:/Users/user/Desktop/데이터 수정/최종프로젝트/shared/data/energy_prediction.csv", index=False, encoding="utf-8-sig")
print("✅ energy_prediction.csv 저장 완료!")
