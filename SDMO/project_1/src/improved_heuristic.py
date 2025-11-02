import pandas as pd
from rapidfuzz import fuzz
import unicodedata
import re
from itertools import combinations

# ---------------- SETTINGS ----------------
REPO_NAME = "tensorflow"
INPUT_FILE =  rf"C:\MyWork\Acadamic\Masters\SDMO\SDMO_G45_PROJECT\SDMO\project_1\results\{REPO_NAME}\developers_raw.csv"
OUTPUT_FILE = rf"C:\MyWork\Acadamic\Masters\SDMO\SDMO_G45_PROJECT\SDMO\project_1\results\{REPO_NAME}\improved_duplicates.csv"

NAME_WEIGHT = 0.7     # weight for name similarity
EMAIL_WEIGHT = 0.3    # weight for email prefix similarity
THRESHOLD = 75    # overall similarity threshold
# ------------------------------------------

def normalize_text(s):
    """Normalize text: remove accents, punctuation, lowercase."""
    if pd.isna(s):
        return ""
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('utf-8', 'ignore')
    s = re.sub(r'[^a-zA-Z0-9@._ -]', '', s)
    return s.lower().strip()

def email_prefix(email):
    return email.split('@')[0] if '@' in email else email

def compute_similarity(name1, name2, email1, email2):
    # Use more flexible name comparison
    name_sim = fuzz.token_sort_ratio(name1, name2)
    email_sim = fuzz.ratio(email_prefix(email1), email_prefix(email2))
    
    # Weighted overall similarity
    overall = NAME_WEIGHT * name_sim + EMAIL_WEIGHT * email_sim
    return name_sim, email_sim, overall

def improved_heuristic(df):
    duplicates = []
    items = df.to_dict('records')

    for (a, b) in combinations(items, 2):
        name1, email1 = normalize_text(a['name']), normalize_text(a['email'])
        name2, email2 = normalize_text(b['name']), normalize_text(b['email'])

        name_sim, email_sim, overall = compute_similarity(name1, name2, email1, email2)

        if overall >= THRESHOLD:
            duplicates.append({
                "name1": a['name'], "email1": a['email'],
                "name2": b['name'], "email2": b['email'],
                "name_similarity": round(name_sim, 2),
                "email_similarity": round(email_sim, 2),
                "overall_score": round(overall, 2)
               #"is_duplicate": 1 if round(overall, 2) > 85 else 0
            })

    dup_df = pd.DataFrame(duplicates)
    dup_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"\nImproved heuristic found {len(dup_df)} potential duplicates.")
    print(f"Results saved to {OUTPUT_FILE}")
    return dup_df

if __name__ == "__main__":
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} unique developer identities.")
    improved_heuristic(df)
