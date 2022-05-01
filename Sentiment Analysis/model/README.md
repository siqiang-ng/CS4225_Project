==================== Training RNN notebook ====================
Ensure the directory has been set correctly as reflected in the notebook.

To extract the standford data, run the following code in the Training RNN file under training the model:

!wget http://nlp.stanford.edu/data/glove.6B.zip

!unzip -u "/content/gdrive/MyDrive/CS4225/ML team/Pre-Processed Data/stanfordSentimentTreebank/glove.6B.zip" -d "/content/gdrive/MyDrive/CS4225/ML team/Pre-Processed Data/"

Ensure that  notebook has been ran and that the Data folder consist of a file by the name of "processed_dictionary_sentiments.csv" generated

Launch the "RNN Training.ipynb" that is extracted from our submission zip file

Create a folder (if non existent) called "RNN_Split_Dataset" in the directory ""/content/gdrive/MyDrive/CS4225/ML team/Pre-Processed Data/stanfordSentimentTreebank/"

esnure these files can be saved accordingly

train_data.to_csv("/content/gdrive/MyDrive/CS4225/ML team/pre-processed data/stanfordSentimentTreebank/RNN_Split_Dataset/Training.csv")
test_data.to_csv("/content/gdrive/MyDrive/CS4225/ML team/pre-processed data/stanfordSentimentTreebank/RNN_Split_Dataset/Test.csv")
val_data.to_csv("/content/gdrive/MyDrive/CS4225/ML team/pre-processed data/stanfordSentimentTreebank/RNN_Split_Dataset/Validation.csv")

Once the notebook have completed its run, a file named "RNN.h5" will be created inside the newly created and is required for the usage of our current neural network

==================== Prediction notebooks ====================

Run the prediction notedbooks with the generated weight files to update the model to predict the sentiment based on the input files

Ensure the directories are set correctly (eg. for scrap_nov_dec):

path = "/content/gdrive/MyDrive/CS4225/ML team/pre-processed data/twitter/scrap_jan_feb/*.csv"

Ouput sentiment file should be: 
path = "/content/gdrive/MyDrive/CS4225/ML team/pre-processed data/stanfordSentimentTreebank/final_jan_feb.csv"

==================== Building feature vector ====================

!pip install findspark
!pip install pyspark

Ensure these modules are installed for spark to run the .ipynb file 

Ensure the shortcut for the vector directory is correct:  "os.chdir("/content/gdrive/MyDrive/CS4225/ML team/Sentiment Analysis Results/lexicon/twitter/scrap_nov_dec/vectors")"

Ensure the shortcut for the sentiment directory is correct:  "os.chdir("/content/gdrive/MyDrive/CS4225/ML team/Sentiment Analysis Results/lexicon/twitter/scrap_nov_dec/sentiments")"

Ensure the shortcut for the label directory is correct:  "os.chdir("/content/gdrive/MyDrive/CS4225/ML team/Sentiment Analysis Results/lexicon/twitter/scrap_nov_dec/labels")"
