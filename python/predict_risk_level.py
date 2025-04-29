import pandas as pd
import joblib

df = pd.read_csv("C:/Users/user/Desktop/데이터 수정/최종프로젝트/shared/data/sensor_result.csv")
model = joblib.load("C:/Users/user/Desktop/데이터 수정/최종프로젝트/python/models/risk_score_model.pkl")
X = df[["temperature", "humidity", "co2", "vibration", "energy_usage"]]
df["risk_score"] = model.predict(X)

def classify(score):
    return "High" if score >= 8 else ("Medium" if score >= 5 else "Low")

df["risk_level"] = df["risk_score"].apply(classify)
df.to_csv("C:/Users/user/Desktop/데이터 수정/최종프로젝트/shared/data/risk_level_prediction.csv", index=False, encoding="utf-8-sig")
print("✅ risk_level_prediction.csv 저장 완료!")
