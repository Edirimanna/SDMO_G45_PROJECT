import pandas as pd
from rapidfuzz import fuzz
import unicodedata
import re
from itertools import combinations

# ----------------- CONFIGURATION -----------------
#REPO_NAME = "tensorflow"
#REPO_NAME = "kubernetes"
INPUT_FILE = rf"C:\MyWork\Acadamic\Masters\SDMO\SDMO_G45_PROJECT\SDMO\project_1\results\{REPO_NAME}\developers_raw.csv"
OUTPUT_FILE = rf"C:\MyWork\Acadamic\Masters\SDMO\SDMO_G45_PROJECT\SDMO\project_1\results\{REPO_NAME}\bird_duplicates.csv"
THRESHOLD = 99 

# ----------------- HELPER FUNCTIONS -----------------
def normalize_text(s):
    """Normalize string: remove accents, convert to lowercase, remove special characters."""
    if pd.isna(s):
        return ""
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('utf-8', 'ignore')
    s = re.sub(r'[^a-zA-Z0-9@._ -]', '', s)
    return s.lower().strip()

def extract_name_parts(name):
    """Split name into first and last name."""
    parts = name.split()
    if len(parts) == 0:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[-1]

def email_prefix(email):
    """Extract prefix from email (before @)."""
    return email.split('@')[0] if '@' in email else email

def similar(a, b, threshold):
    """Check if two strings are similar based on Levenshtein ratio."""
    return fuzz.ratio(a, b) >= threshold

# ----------------- BIRD HEURISTIC FUNCTION -----------------
def bird_heuristic_filtered(df, threshold=78):
    duplicates = []

    # --- BLOCKING BY FIRST LETTER OF NAME ONLY ---
    df['name_key'] = df['name'].apply(lambda x: normalize_text(str(x))[:5])

    # Compare only within each block
    for _, group in df.groupby(['name_key']):
        items = group.to_dict('records')

        # Compare all pairs in block (no slice)
        for a, b in combinations(items, 2):
            name1, email1 = normalize_text(a['name']), normalize_text(a['email'])
            name2, email2 = normalize_text(b['name']), normalize_text(b['email'])

            first1, last1 = extract_name_parts(name1)
            first2, last2 = extract_name_parts(name2)
            prefix1, prefix2 = email_prefix(email1), email_prefix(email2)

            # Bird heuristic conditions
            c1 = similar(name1, name2, threshold)
            c2 = similar(prefix1, prefix2, threshold)
            c3 = similar(first1, first2, threshold) and similar(last1, last2, threshold)
            c4 = first1 and last1 and prefix2.startswith(first1[:2] + last1)
            c5 = first1 and last1 and prefix2.startswith(last1[:2] + first1)
            c6 = first2 and last2 and prefix1.startswith(first2[:2] + last2)
            c7 = first2 and last2 and prefix1.startswith(last2[:2] + first2)

            if any([c1, c2, c3, c4, c5, c6, c7]):
                duplicates.append({
                    "name1": a['name'],
                    "email1": a['email'],
                    "name2": b['name'],
                    "email2": b['email']
                })

    dup_df = pd.DataFrame(duplicates)

    # Deduplicate symmetric pairs
    dup_df['pair_key'] = dup_df.apply(lambda x: tuple(sorted([x['name1'], x['name2']])), axis=1)
    dup_df = dup_df.drop_duplicates('pair_key').drop(columns='pair_key')

    dup_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print("THRESHOLD: ", THRESHOLD)
    print(f"\nPossible duplicate pairs: {len(dup_df)} (saved to {OUTPUT_FILE})")
    return dup_df

# ----------------- MAIN SCRIPT -----------------
if __name__ == "__main__":
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} unique (name,email) pairs.")
    result = bird_heuristic_filtered(df, THRESHOLD)
    print(result.head())
