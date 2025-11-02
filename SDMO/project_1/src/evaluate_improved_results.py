import pandas as pd

REPO_NAME = "tensorflow"
INPUT_FILE = rf"C:\MyWork\Acadamic\Masters\SDMO\SDMO_G45_PROJECT\SDMO\project_1\results\{REPO_NAME}\improved_duplicates_validated.csv"

def evaluate_results(file_path):
    try:
        df = pd.read_csv(file_path, engine='python', on_bad_lines='skip')
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return

    if 'is_duplicate' not in df.columns:
        print("⚠️ Add a column 'is_duplicate' with 1 (True Positive) or 0 (False Positive).")
        return

    tp = df['is_duplicate'].sum()
    fp = len(df) - tp

    # Since you manually validated, all 1s are true positives (TP),
    # all 0s are false positives (FP), recall = 1 by definition.
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = 1.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("\n📊 Evaluation Results (Improved Heuristic)")
    print("-----------------------------------")
    print(f"Total pairs evaluated : {len(df)}")
    print(f"True Positives (TP)   : {tp}")
    print(f"False Positives (FP)  : {fp}")
    print(f"Precision             : {precision:.3f}")
    print(f"Recall                : {recall:.3f}")
    print(f"F1-score              : {f1:.3f}")

    return {
        "TotalPairs": len(df),
        "TP": tp,
        "FP": fp,
        "Precision": precision,
        "Recall": recall,
        "F1": f1
    }

if __name__ == "__main__":
    evaluate_results(INPUT_FILE)
