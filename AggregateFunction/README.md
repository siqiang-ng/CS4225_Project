# Post Processing Code - AggregateFunction

## Description
The purpose for this set of codes is to process the output of the results that come out from the Lexicon-Based and Machine Learning model. 
This code is to be used for reducing the number of rows of data so that the total number of rows does not
exceed the Tableau Public data limit of 15 million rows.

## Requirements for this code
1. IntelliJ IDE
2. Sparks 3.0.0
3. Hadoop 3.3.0
4. Input files to be processed (Results of the Machine Learning model)

## Setup Guide

This set of codes is using the IntelliJ IDEA. The guide will also be based on IntelliJ. 

1. In File > Project Structure > Modules > Dependencies, ensure that Hadoop and Spark jars libraries are already added in the dependencies. 
If it is set up right, the spark jars file should be placed before the hadoop files as shown here.

![dependencies.png](dependencies.png)

2. Add all the processed data files under an input folder in this project. 

3. Set up the running configurations as shown in the following screenshot. The current code takes in a csv file one by one each time 
for processing. Do take note of the working directory where you place your project folder in.

![configurations.png](configurations.png)

5. Run the configurations and you will see an output folder with the csv file required for the Tableau visualizations later.