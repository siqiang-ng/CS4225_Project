import time
import glob
import pandas as pd
from pathlib import Path
import spacy
import importlib
from joblib import Parallel, delayed

def get_lang_module(lang):
    if lang == "zh" or lang == "en" :
        return lang + "_core_web_sm"
    if lang in languages_pipe:
        return lang + "_core_news_sm"
    return multi_lang + "_ent_wiki_sm"

def remove_stopwords_pipe(doc):
    return [token.text for token in doc if not token.is_stop and token.is_alpha]

def remove_stopwords_no_pipe(stopwords, doc):
    return [token.text for token in doc if not token.text in stopwords and token.is_alpha]

def get_remove_stopwords(lang):
    if lang in languages_pipe:
        return remove_stopwords_pipe

    stopwords = nlp.Defaults.stop_words

    if lang in languages_no_pipe:
        lang_module = importlib.import_module(f"spacy.lang.{lang}")
        stopwords = lang_module.stop_words.STOP_WORDS

    return lambda d: remove_stopwords_no_pipe(stopwords, d)

def clean(text):
    doc = nlp(text)
    return remove_stopwords(doc)

def clean_pipe(texts):
    arr = []
    for doc in nlp.pipe(texts, disable=["tagger", "ner", "parser", "lemmatizer", "textcat", "attribute_ruler", "tok2vec"], batch_size=batch_size):
        arr.append(clean(doc))
    return arr

def chunker(iterable, total_length):
    return (iterable[pos: pos + chunk_size] for pos in range(0, total_length, chunk_size))

def preprocess_parallel(texts, length):
    executor = Parallel(backend='multiprocessing', prefer="processes", batch_size='auto', verbose=10,n_jobs=n_jobs)
    do = delayed(clean_pipe)
    tasks = (do(chunk) for chunk in chunker(texts, length))
    result = executor(tasks)
    return [item for sublist in result for item in sublist]

def process(file):

    df = pd.read_csv(file, lineterminator="\n")

    df["text"] = preprocess_parallel(df["text"], df.size)

    df = df[["text", "lang", "created_at"]]

    return df

def output_file(df, prefix, lang):
    filepath = Path(prefix + lang + ".csv")
    num = 0
    while filepath.is_file():
        num += 1
        filepath = Path(prefix + lang + str(num) + ".csv")
    filepath.parent.mkdir(parents=True, exist_ok=True)

    print("outputting: " + filepath.name)
    df.to_csv(filepath)

if __name__ == '__main__':

    languages_pipe = ["ca", "zh", "da", "nl", "en", "fr", "de", "el", "it", "ja", "lt", "mk", "nb", "pl", "pt", "ro", "ru", "es"]
    multi_lang = "xx"
    languages_no_pipe = ["af", "sq", "ar", "hy", "eu", "bn", "bg", "hr", "cs", "et", "fi", "gu", "he", "hi", "hu", "is", "id", "ga", "kn", "ko", "ky", "lv", "lij", "lb", "ml", "mr", "ne", "fa", "sa", "sr", "tn", "si", "sk", "sl", "sv", "tl", "ta", "tt", "te", "th", "tr", "uk", "ur", "vi", "yo"]

    batch_size = 10000
    chunk_size = 3000
    n_jobs = -2

    prev_lang = ''
    prev_is_xx = False

    for filename in glob.glob("*.csv"):
        print("processing: " + filename)

        try:
            lang = filename[:2].lower()
            if lang == "iw": lang = "he"

            is_xx = lang not in languages_pipe
            if prev_lang != lang and (not prev_is_xx or not is_xx):
                nlp = spacy.load(get_lang_module(lang))

            program_start = time.perf_counter()

            remove_stopwords = get_remove_stopwords(lang)

            df = process(filename)

            output_file(df, ".", lang)

            program_end = time.perf_counter()
            print("time elapsed: " + str(round((program_end - program_start) / 60, 2)) + " min")

            prev_lang = lang
            prev_is_xx = is_xx
        except Exception as e:
            print(e)

