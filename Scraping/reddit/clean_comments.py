import pandas as pd
import numpy as np
from pathlib import Path 

def get_cleaned_submissions_ids():
    df = pd.read_csv("cleaned_submissions.csv", sep=",", header=None)
    df = df.iloc[:, :6]
    df.columns = ["subreddit", "id", "created_utc",	"title", "selftext", "full_link"]
    return set(df["id"])

cleaned_submission_ids = get_cleaned_submissions_ids()

df = pd.read_csv("comments.csv", sep=",", header=None)
df = df.iloc[:, :7]
df.columns = ["subreddit", "id", "submission_id", "body", "created_utc", "parent_id", "permalink"]

mask = []
for i in range(df.shape[0]):
    row = df.iloc[i]
    if row["submission_id"] in cleaned_submission_ids:
        mask.append(True)
    else:
        mask.append(False)
df = df[mask]

filepath = Path("cleaned_comments.csv", mode="a")
df.to_csv(path_or_buf=filepath)
