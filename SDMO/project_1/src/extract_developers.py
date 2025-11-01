# File: SDMO/src/extract_developers.py
from git import Repo
import pandas as pd
import os

REPO_NAME = "kubernetes"

def extract_developers(repo_path):
    repo = Repo(repo_path)
    data = []
    for commit in repo.iter_commits():
        data.append({
            "name": commit.author.name,
            "email": commit.author.email
        })
    df = pd.DataFrame(data).drop_duplicates()
    return df

def save_developers(df, output_file=fr"C:\MyWork\Acadamic\Masters\SDMO\SDMO_G45_PROJECT\SDMO\project_1\results\{REPO_NAME}\developers_raw.csv"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    repo_path = rf"C:\MyWork\Acadamic\Masters\SDMO\SDMO_G45_PROJECT\repo\{REPO_NAME}"
    df = extract_developers(repo_path)
    save_developers(df)
