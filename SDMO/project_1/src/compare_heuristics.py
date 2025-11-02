import pandas as pd

# --- Configuration ---
REPO_NAME = "tensorflow"
BIRD_FILE = rf"C:\MyWork\Acadamic\Masters\SDMO\SDMO_G45_PROJECT\SDMO\project_1\results\{REPO_NAME}\bird_duplicates_validated.csv"
IMPROVED_FILE = rf"C:\MyWork\Acadamic\Masters\SDMO\SDMO_G45_PROJECT\SDMO\project_1\results\{REPO_NAME}\improved_duplicates_validated.csv"

def evaluate(file_path, label):
    df = pd.read_csv(file_path, engine='python', on_bad_lines='skip')
    tp = df['is_duplicate'].sum()
    fp = len(df) - tp

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = 1.0  # since validation includes all known pairs
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {"Heuristic": label, "Pairs": len(df), "TP": tp, "FP": fp,
            "Precision": round(precision, 3), "Recall": round(recall, 3), "F1": round(f1, 3)}

def main():
    bird_results = evaluate(BIRD_FILE, "Bird Heuristic")
    improved_results = evaluate(IMPROVED_FILE, "Improved Heuristic")

    results_df = pd.DataFrame([bird_results, improved_results])
    print("\n📊 Comparison of Heuristics")
    print("-------------------------------------")
    print(results_df.to_string(index=False))

    # Optional: save to CSV
    output_path = rf"C:\MyWork\Acadamic\Masters\SDMO\SDMO_G45_PROJECT\SDMO\project_1\results\{REPO_NAME}\heuristic_comparison.csv"
    results_df.to_csv(output_path, index=False)
    print(f"\nComparison saved to: {output_path}")

if __name__ == "__main__":
    main()
