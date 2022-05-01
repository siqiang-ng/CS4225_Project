import pandas as pd
import numpy as np
from pathlib import Path  

KEYWORDS = {
    "russia-ukraine",
    "ukraine", 
    "ukranian", 
    "ukranians",
    "kyiv",
    "chernobyl",
    "russia", 
    "russian", 
    "russians", 
    "moscow",
    "vladimir",
    "putin", 
    "volodymyr",
    "zelensky",
    "zelenskyy",
}

df = pd.read_csv("submissions.csv", sep=",", header=None)
df = df.iloc[:, :6]
df.columns = ["subreddit", "id", "created_utc",	"title", "selftext", "full_link"]

mask = []
for i in range(df.shape[0]):
    row = df.iloc[i]
    words = str(row["title"]).split(" ")
    split_selftext = str(row["selftext"]).split(" ")

    found = False
    for word in words:
        if (word.lower() in KEYWORDS):
            found = True
            break
    mask.append(found)
df = df[mask]

filepath = Path("cleaned_submissions.csv", mode="a")
df.to_csv(path_or_buf=filepath)