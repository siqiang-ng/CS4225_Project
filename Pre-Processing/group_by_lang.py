import time
import glob, os
import pandas as pd
from pathlib import Path

def output_file(df, filename):
    filepath = Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, mode='a', header=not os.path.exists(filepath))

def output_group(group):
    lang = group["lang"].unique()[0].lower()
    output_file(group, f"{lang}.csv")

def group_by_lang(file):
    df = pd.read_csv(file, lineterminator='\n')

    df = df.drop_duplicates(subset=["text", "lang", "created_at"])

    df.groupby("lang").apply(output_group)

if __name__ == '__main__':
    for filename in glob.glob("*.csv"):
        program_start = time.perf_counter()

        print("grouping: " + filename)
        df = group_by_lang(filename)

        program_end = time.perf_counter()
        print("time elapsed: " + str(round((program_end - program_start) / 60, 2)) + " min")
