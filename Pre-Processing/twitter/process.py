import time
import glob, os
import pandas as pd
from pathlib import Path

def output_file(df, filename):
    try:
        os.remove(filename)
    except OSError:
        pass

    filepath = Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath)

def process(file):
    df = pd.read_csv(file, usecols=["text", "language", "tweetcreatedts"])
    df = df.rename(columns={"language": "lang",})
    df["created_at"] = pd.to_datetime(df["tweetcreatedts"], format='%Y-%m-%d %H:%M:%S')
    df = df.drop(columns=["tweetcreatedts"])
    return df

if __name__ == '__main__':
    for filename in glob.glob("*.csv"):
        program_start = time.perf_counter()

        print("processing: " + filename)
        df = process(filename)

        program_end = time.perf_counter()
        print("time elapsed: " + str(round((program_end - program_start) / 60, 2)) + " min")
