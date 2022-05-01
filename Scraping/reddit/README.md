# Reddit Data Scraping

## Description

Scrape posts and comments from any public subreddit.

## Dependencies

-   loguru
-   typer
-   praw
-   codetiming
-   PyYAML
-   prawcore
-   tqdm
-   pretty-errors
-   pushshift.py

## Workflow

1. Install required dependencies.
1. Obtain reddit id and secret by following [this guide](https://stackoverflow.com/questions/28955541/how-to-get-access-token-reddit-api/42304034#42304034)
1. `python subreddit_downloader.py <enter subreddit here> --batch-size 100 --laps 15 --reddit-id <enter id here> --reddit-secret <enter secret here> --reddit-username <enter username here> --utc-after 1647129600`
1. `python dataset_builder.py`
1. `python clean_submissions.py`
1. `python clean_comments.py`

## Acknowledgements

Code for scraping Reddit and and building dataset is from [pistocop](https://github.com/pistocop/subreddit-comments-dl)
which is available for modification, distribution and private use under GPL-3.0 License. We have added code for the context
of the Russian-Ukraine war.
