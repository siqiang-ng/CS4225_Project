# Data Pre-Processing

## Description

Pre-process tweets and reddit posts using Python3.

## Dependencies

1. pandas
2. polyglot
3. spaCy
4. importlib
5. joblib

## Workflow

1. Install required dependencies.
2. Process raw tweets and reddit posts.
    1. Run twitter/process.py to process tweets.
    2. Run reddit/comments/process_comments.py to process reddit comments.
    3. Run reddit/submissions/process_submissions.py to process reddit submissions.
3. Run group_by_lang.py to group posts.
4. Run pre_process.py to tokenize and remove stopwords.
