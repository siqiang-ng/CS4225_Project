import datetime
import time
import os
import pandas as pd
from pathlib import Path
import twint

SEARCH_TERMS = [
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
    "zelenskyy"]

def scrap_tweets(start, end, num):
    config = twint.Config()

    config.Search = ' OR '.join(SEARCH_TERMS)
    config.Since = start
    config.Until = end
    config.Filter_retweets = True

    config.Count = True
    config.Limit = num
    config.Hide_output = True
    config.Pandas = True

    twint.run.Search(config)
    df = twint.storage.panda.Tweets_df

    if df.empty: return df

    df = df[["tweet", "language", "date", "timezone"]]
    df = df.rename(columns={"tweet": "text", "language": "lang",})
    df["created_at"] = pd.to_datetime(
        df["date"] + " " + df["timezone"], format='%Y-%m-%d %H:%M:%S %z')
    df = df.drop(columns=["date", "timezone"])

    return df

def get_date_range(start, end, periods):
    # check https://pd.pydata.org/pd-docs/stable/user_guide/timeseries.html#offset-aliases for interval for date_range
    date_range = pd.DataFrame(columns=['NULL'],index=pd.date_range(start, end, periods=periods))

    return date_range.index.to_pydatetime().tolist()

def get_date_range_day(start, end):
    # check https://pd.pydata.org/pd-docs/stable/user_guide/timeseries.html#offset-aliases for interval for date_range
    date_range = pd.DataFrame(columns=['NULL'],index=pd.date_range(start, end, freq="1D"))

    return date_range.index.to_pydatetime().tolist()

def scrap_and_output(start, end, num, num_periods):
    date_range = get_date_range(start, end, periods=num_periods)

    filename = f"output/{date_range[0].strftime('%Y-%m-%d')}_to_{date_range[-1].strftime('%Y-%m-%d')}.csv"

    dataframes = []
    for i in range(len(date_range) - 1):
        curr_start_date = date_range[i]
        curr_end_date = date_range[i + 1]
        curr_start = curr_start_date.strftime('%Y-%m-%d %H:%M:%S')
        curr_end = curr_end_date.strftime('%Y-%m-%d %H:%M:%S')
        print("\nscraping: " + curr_start + " to " + curr_end)

        df = None
        for _ in range(4):
            try:
                df = scrap_tweets(start, end, num)
                if not df.empty: break
            except Exception as e:
                print(e)

        if df is None or not df.empty:
            dataframes.append(df)

        if len(dataframes) >= 10:
            output_file(pd.concat(dataframes, ignore_index=True), filename)
            dataframes = []

    # output dataframe
    output_file(pd.concat(dataframes, ignore_index=True), filename)

def output_file(df, filename):
    filepath = Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, mode='a', header=not os.path.exists(filepath))

if __name__ == "__main__":
    program_start = time.perf_counter()

    num = 2000000

    # collect from start to end - 1, from 00:00:00 to 23:59:99
    # "YYYY-MM-DD"

    start_date = datetime.datetime(2021, 11, 11)
    end_date = datetime.datetime(2021, 11, 12)
    start = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end = end_date.strftime('%Y-%m-%d %H:%M:%S')

    date_range = get_date_range_day(start, end)

    for i in range(len(date_range) - 1):
        curr_start_date = date_range[i]
        curr_end_date = date_range[i + 1]
        curr_start = curr_start_date.strftime('%Y-%m-%d %H:%M:%S')
        curr_end = curr_end_date.strftime('%Y-%m-%d %H:%M:%S')

        num_periods = 1441

        scrap_and_output(curr_start, curr_end, num, num_periods)

    program_end = time.perf_counter()
    print("time elapsed: " + str(round((program_end - program_start) / 60, 2)) + " min")
