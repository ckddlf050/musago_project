import pandas as pd

# 🔹 센서 결과 불러오기
df = pd.read_csv("C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/sensor_result.csv")

# 🔹 AI 학습용 라벨 컬럼 추가
def assign_label(row):
    statuses = [row["temp_status"], row["hum_status"], row["co2_status"], row["vib_status"], row["energy_status"]]
    if "red" in statuses:
        return "risk"
    elif all(s == "green" for s in statuses):
        return "safe"
    else:
        return "warning"

df["label"] = df.apply(assign_label, axis=1)

# 🔹 필요한 컬럼만 선택해서 저장
output_df = df[["temperature", "humidity", "co2", "vibration", "energy_usage", "label"]]
output_df.to_csv("C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data/ai_dataset.csv", index=False, encoding='utf-8-sig')

print("✅ AI 학습용 데이터셋 저장 완료: ai_dataset.csv")
