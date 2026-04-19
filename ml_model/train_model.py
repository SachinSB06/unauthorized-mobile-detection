import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

DATA_FILE = "training_data.csv"
MODEL_PATH = "model.pkl"

def train():
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        print(" training_data.csv not found. Run collect_data.py first.")
        return

    if len(df) < 10:
        print(" Not enough data. Collect more samples first.")
        return

    print(f" Loaded {len(df)} samples\n")
    print("Label distribution:")
    print(df["label"].value_counts(), "\n")

    X = df[["rssi_mean", "rssi_std", "packet_rate", "duration", "known"]]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print(" Model Performance:\n")
    print(classification_report(y_test, model.predict(X_test)))

    joblib.dump(model, MODEL_PATH)
    print(f" Model saved as '{MODEL_PATH}'")

if __name__ == "__main__":
    train()