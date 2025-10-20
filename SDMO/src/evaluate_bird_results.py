import pandas as pd

# ---------------- SETTINGS ----------------
INPUT_FILE =  r"results\bird_duplicates_validated.csv"
# ------------------------------------------

def evaluate_results(file_path):
    df = pd.read_csv(file_path)
    
    if 'is_duplicate' not in df.columns:
        print("⚠️ Please add a column named 'is_duplicate' with 1 (True Positive) or 0 (False Positive).")
        return

    tp = df['is_duplicate'].sum()
    fp = len(df) - tp

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / len(df)  # here, recall = precision since we only check predicted pairs
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("\n📊 Evaluation Results (Bird Heuristic)")
    print("-----------------------------------")
    print(f"Total pairs evaluated : {len(df)}")
    print(f"True Positives (TP)   : {tp}")
    print(f"False Positives (FP)  : {fp}")
    print(f"Precision             : {precision:.3f}")
    print(f"Recall                : {recall:.3f}")
    print(f"F1-score              : {f1:.3f}")

    return {
        "TP": tp,
        "FP": fp,
        "Precision": precision,
        "Recall": recall,
        "F1": f1
    }

if __name__ == "__main__":
    evaluate_results(INPUT_FILE)
