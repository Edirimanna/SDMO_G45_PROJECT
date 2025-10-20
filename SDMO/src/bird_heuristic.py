import pandas as pd
from rapidfuzz import fuzz
import unicodedata
import re
from itertools import combinations

INPUT_FILE = r"results\developers_raw.csv"
OUTPUT_FILE = r"results\bird_duplicates.csv"
THRESHOLD = 95  # stricter similarity threshold

def normalize_text(s):
    if pd.isna(s):
        return ""
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('utf-8', 'ignore')
    s = re.sub(r'[^a-zA-Z0-9@._ -]', '', s)
    return s.lower().strip()

def extract_name_parts(name):
    parts = name.split()
    if len(parts) == 0:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[-1]

def email_prefix(email):
    return email.split('@')[0] if '@' in email else email

def similar(a, b, threshold):
    return fuzz.ratio(a, b) >= threshold

def bird_heuristic_filtered(df, threshold=95):
    duplicates = []

    # --- STRONGER BLOCKING ---
    df['name_key'] = df['name'].apply(lambda x: normalize_text(str(x))[:2])        # first 2 letters of name
    df['email_prefix_key'] = df['email'].apply(lambda x: normalize_text(str(x).split('@')[0])[:2])  # first 2 letters of email prefix
    df['email_domain'] = df['email'].apply(lambda x: str(x).split('@')[-1] if '@' in str(x) else '')

    # Compare only within each block
    for (_, group) in df.groupby(['name_key', 'email_prefix_key', 'email_domain']):
        items = group.to_dict('records')
        for a, b in combinations(items, 2):
            name1, email1 = normalize_text(a['name']), normalize_text(a['email'])
            name2, email2 = normalize_text(b['name']), normalize_text(b['email'])

            first1, last1 = extract_name_parts(name1)
            first2, last2 = extract_name_parts(name2)
            prefix1, prefix2 = email_prefix(email1), email_prefix(email2)

            c1 = similar(name1, name2, threshold)
            c2 = similar(prefix1, prefix2, threshold)
            c3 = similar(first1, first2, threshold) and similar(last1, last2, threshold)
            c4 = prefix2.startswith(first1[0:1] + last1)
            c5 = prefix2.startswith(last1[0:1] + first1)
            c6 = prefix1.startswith(first2[0:1] + last2)
            c7 = prefix1.startswith(last2[0:1] + first2)

            if any([c1, c2, c3, c4, c5, c6, c7]):
                duplicates.append({
                    "name1": a['name'],
                    "email1": a['email'],
                    "name2": b['name'],
                    "email2": b['email']
                })

    dup_df = pd.DataFrame(duplicates)
    dup_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"\nPossible duplicate pairs: {len(dup_df)} (saved to {OUTPUT_FILE})")
    return dup_df

if __name__ == "__main__":
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} unique (name,email) pairs.")
    result = bird_heuristic_filtered(df, THRESHOLD)
    print(result.head())
