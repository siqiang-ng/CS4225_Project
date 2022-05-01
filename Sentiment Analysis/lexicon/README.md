## Lexicon notebook

1. Ensure the directory has been set correctly as reflected in the notebook
2. Edit the variables as necessary (e.g. `LANG = "fr"`)
3. Run the entire notebook 

## Combining the output 

Run the following commands in a Unix shell (e.g. Terminal on macOS)

1. Write the header of a csv file (e.g en.csv)
```
head -1 directory/en.csv > output csv 
```

2. Write the content of all csv files in a directory
```
tail -n +2 directory/*.csv >> output.csv
```
