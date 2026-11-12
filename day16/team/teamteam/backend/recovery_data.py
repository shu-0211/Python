from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


TEAM_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = TEAM_DIR.parent / "model.pkl"
CSV_PATH = TEAM_DIR / "athlete_recovery_synthetic.csv"

FEATURE_COLUMNS = [
    "Age",
    "Gender",
    "Training_Duration_Min",
    "Training_Intensity",
    "Sleep_Duration_Hours",
    "Stress_Level",
    "Caffeine_Intake_mg",
    "Muscle_Soreness",
]
TARGET_COLUMN = "Recovery_Score"
CATEGORY_CODES = {
    "Gender": {"Male": 0, "Female": 1},
    "Stress_Level": {"Low": 1, "Medium": 2, "High": 3},
}


def split_recovery_data():
    data = pd.read_csv(CSV_PATH)
    for column, codes in CATEGORY_CODES.items():
        data[column] = data[column].map(codes)

    # 기존 team.py가 학습에 사용한 행과 테스트 분할을 그대로 재현합니다.
    data = data.dropna()
    return train_test_split(
        data[FEATURE_COLUMNS], data[TARGET_COLUMN], test_size=0.2, random_state=42
    )
