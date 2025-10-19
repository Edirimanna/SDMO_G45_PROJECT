from git import Repo
import pandas as pd

repo_path = r"C:\MyWork\Acadamic\Masters\SDMO\SDMO_G45_PROJECT\repo\moby"
repo = Repo(repo_path)


data = []
for commit in repo.iter_commits():
    data.append({
        "name": commit.author.name,
        "email": commit.author.email
    })

df = pd.DataFrame(data).drop_duplicates()
df.to_csv("developers_raw.csv", index=False)
