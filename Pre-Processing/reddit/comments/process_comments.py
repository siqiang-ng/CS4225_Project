import time
import glob, os
import pandas as pd
from pathlib import Path
from polyglot.detect import Detector

def output_file(df, filename):
    try:
        os.remove(filename)
    except OSError:
        pass

    filepath = Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath)

def get_lang(text):
    detector = Detector(text, quiet=True)
    return detector.language.code

def process(file):
    df = pd.read_csv(file)

    df = df.rename(columns={"body": "text"})

    df["created_at"] = pd.to_datetime(df["created_utc"], unit='s')

    df = df[["text", "created_at"]]

    df["text"] = df["text"].astype({'text': 'str'}).apply(lambda s: "" if s == "nan" else s.strip())

    df = df[df["text"] != '']

    df["lang"] = df["text"].apply(get_lang)

    return df

if __name__ == '__main__':

    for filename in glob.glob("*.csv"):
        program_start = time.perf_counter()

        print("processing: " + filename)
        df = process(filename)

        output_file(df, "comments.csv")

        program_end = time.perf_counter()
        print("time elapsed: " + str(round((program_end - program_start) / 60, 2)) + " min")
