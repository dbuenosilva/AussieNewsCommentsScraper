# -*- coding: utf-8 -*-

""" 

Text classification model retrieved from Kaggle. 

Used to created the model according to BBC dataset labels.

https://www.kaggle.com/skaistule/text-classification-clustering

DataSet:
    https://www.kaggle.com/shivamkushwaha/bbc-full-text-document-classification

Needed modules to install to run this script and create the model

For MacOs: 
    brew install lipomp

For Python:
    pip install xgboost
    pip install gensim
    pip install python-Levenshtein
    pip install wordcloud


""" 

import sys
import pathlib
path = str(pathlib.Path(__file__).resolve().parent) + "/"
sys.path.append(path)

path += '../data/kaggle/input'

#%pylab inline
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from pprint import pprint
from xgboost import XGBClassifier
from gensim.models import Phrases, LdaModel
from gensim.corpora import Dictionary
import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import brown
from nltk import FreqDist
from wordcloud import WordCloud 
from collections import OrderedDict
#import matplotlib.pyplot as plt

def getModel():
        
    print("\nCreating a model with BBC dataset labels...")
    
    # Creating a Df with 5 columns: Directory, Category, FileName, Title, Text
    categories = []
    titles = []
    all_data = []
    #df = pd.DataFrame()
    # dirname
    for dirname, categoryname, filenames in os.walk(path):
        # filename
        for filename in filenames:
            if filename == 'README.TXT':
                filenames.remove(filename)
            else:
                # Absolute path
                current_file = os.path.abspath(os.path.join(dirname, filename))
                open_file = open(current_file, 'r', encoding="latin-1")
                # text_data
                text_data = open_file.read().split('\n')
                text_data = list(filter(None, text_data))
                titles.append(text_data[0])
                all_data.append((dirname, dirname.rsplit('/',1)[1], filename, text_data[0], text_data[1:]))
                #data_df = f"Directory: {dirname}, Category: {dirname.rsplit('/',1)[1]}, FileName: {filename}, Title: {text_data[0]}, Text: {text_data[1:]}"
                #print(data_df)
                
    df = pd.DataFrame(all_data, columns=['directory', 'category', 'fileName', 'title', 'text'])
    df['text'] = df.text.astype(str)
    #print(df.head())
    
    #print(df.describe())
    
    #print(df.category.value_counts())
    
    #bar_plot=df.category.value_counts().plot(kind='barh', figsize=(8, 6), color='teal')
    #plt.xlabel("Nr. of Artciles", labelpad=14)
    #plt.ylabel("Category", labelpad=14)
    #plt.title("Nr. of Articles in category", y=1.02, color='navy')
    
    #for index, value in enumerate(df.category.value_counts()):
    #    plt.text(value, index, str(value))
        
    #df.text[1][:1000]
    
    # 0 - business, 1 -entertainment, 2 - politics, 3 - sport, 4 - tech
    label_enc = LabelEncoder()
    df['label'] = label_enc.fit_transform(df['category'])
    df.tail()
    
    # An array of words
    df_txt = np.array(df['text'])
    
    #print(df_txt)
    
    
    df_txt = docs_preprocessor(df_txt)
    
    # Add bigrams and trigrams to docs (only ones that appear 10 times or more)
    bigram = Phrases(df_txt, min_count=10)
    trigram = Phrases(bigram[df_txt])
    
    for idx in range(len(df_txt)):
        for token in bigram[df_txt[idx]]:
            if '_' in token:
                df_txt[idx].append(token)
        for token in trigram[df_txt[idx]]:
            if '_' in token:
                df_txt[idx].append(token)
    
    # Create a dictionary representation of the documents
    dictionary = Dictionary(df_txt)
    #print('Nr. of unique words in initital documents:', len(dictionary))
    
    # Filter out words that occur less than 10 documents, or more than 20% of the documents
    dictionary.filter_extremes(no_below=10, no_above=0.2)
    #print('Nr. of unique words after removing rare and common words:', len(dictionary))
    
    df['text2'] = df_txt
    
    df['text3'] = [' '.join(map(str, j)) for j in df['text2']]
    
    df.iloc[1475:1480,:]
    
    
    #vectorizer = TfidfVectorizer(stop_words = 'english', lowercase=True)
    vectorizer = TfidfVectorizer(input='content', analyzer = 'word', lowercase=True, stop_words='english',\
                                       ngram_range=(1, 3), min_df=40, max_df=0.20,\
                                      norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True)
    text_vector = vectorizer.fit_transform(df.text3)
#    dtm = text_vector.toarray()
#    features = vectorizer.get_feature_names()
    
 #   h = pd.DataFrame(data = text_vector.todense(), columns = vectorizer.get_feature_names())
 #   h.iloc[990:1000,280:300]
    
 #   corpus = [dictionary.doc2bow(txt) for txt in df_txt]
    
    #print(f'Number of unique tokens: {len(dictionary)}')
    #print(f'Number of documents: {len(corpus)}')
    
    # Frequency distribution for dictionary
    #fdist = nltk.FreqDist(dictionary)
    #fdist
    
    X = text_vector
    y = df.label.values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    #print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    
    
    """ ACCORDING TO AUTHOR, SGDC CLASSIFIER HAS BETTER PERFORMANCE """
    svc3 = SGDClassifier(random_state = 42)
    svc3.fit(X_train, y_train)
    svc3_pred = svc3.predict(X_test)
    #print(f"Train Accuracy: {svc3.score(X_train, y_train)*100:.3f}%")
    print(f"\n\nTest Accuracy of the model on BBC dataset: {svc3.score(X_test, y_test)*100:.3f}%")
    
    """ NO LONGER NEED TO TRAIN 
    svc1 = RandomForestClassifier(random_state = 42)
    svc1.fit(X_train, y_train)
    svc1_pred = svc1.predict(X_test)
    #print(f"Train Accuracy: {svc1.score(X_train, y_train)*100:.3f}%")
    print(f"Test Accuracy: {svc1.score(X_test, y_test)*100:.3f}%")
    
    svc2 = XGBClassifier(random_state = 42, use_label_encoder=False)
    svc2.fit(X_train, y_train)
    svc2_pred = svc2.predict(X_test)
    #print(f"Train Accuracy: {svc2.score(X_train, y_train)*100:.3f}%")
    print(f"Test Accuracy: {svc2.score(X_test, y_test)*100:.3f}%")
    
    svc4 = KNeighborsClassifier()
    #pprint(svc4.get_params())
    svc4.fit(X_train, y_train)
    svc4_pred = svc4.predict(X_test)
    #print(f"Train Accuracy: {svc4.score(X_train, y_train)*100:.3f}%")
    print(f"Test Accuracy: {svc4.score(X_test, y_test)*100:.3f}%")
    
    
    svc1_mae = fit_and_evaluate(svc1,X_train, y_train,X_test,y_test)
    svc2_mae = fit_and_evaluate(svc2,X_train, y_train,X_test,y_test)
    svc3_mae = fit_and_evaluate(svc3,X_train, y_train,X_test,y_test)
    svc4_mae = fit_and_evaluate(svc4,X_train, y_train,X_test,y_test)
    
    
    plt.style.use('fivethirtyeight')
    fig = plt.figure(figsize(8, 6))
    
    # Dataframe to hold the results
    model_comparison = pd.DataFrame({'model': ['RandomForest Classifier', 'XGBClassifier', 
                                               'SGDClassifier', 'KNeighborsClassifier'
                                              ],
                                     'mae': [svc1_mae, svc2_mae, 
                                             svc3_mae, svc4_mae]})
    
    # Horizontal bar chart of test mae
    model_comparison.sort_values('mae', ascending = False).plot(x = 'model', y = 'mae', kind = 'barh',
                                                               color = 'yellow', edgecolor = 'black')
    
    # Plot formatting
    plt.ylabel('')
    plt.yticks(size = 14)
    plt.xlabel('Mean Absolute Error')
    plt.xticks(size = 14)
    plt.title('Model Comparison on Test MAE', size = 20)
        
    """ 

    # Return the trained model

    return(svc3, vectorizer)


def docs_preprocessor(docs):
    
    stopwords = nltk.corpus.stopwords.words('english')
    # Remain only letters
    tokenizer = RegexpTokenizer('[A-Za-z]\w+')
    
    for idx in range(len(docs)):
         # Convert to lowercase
        docs[idx] = docs[idx].lower() 
        # Split into words
        docs[idx] = tokenizer.tokenize(docs[idx])  
    
    # Lemmatize all words with len>2 in documents 
    lemmatizer = WordNetLemmatizer()
    docs = [[nltk.stem.WordNetLemmatizer().lemmatize(token) for token in doc if len(token) > 2 and token not in stopwords] for doc in docs]
    #stemmer = SnowballStemmer('english')
    #docs = [[stemmer.stem(token) for token in doc if len(token) > 2 and token not in stopwords] for doc in docs]
         
    return docs


# Function to calculate mean absolute error
def mae(y_true, y_pred):
    return np.mean(abs(y_true - y_pred))

# Takes in a model, trains the model, and evaluates the model on the test set
def fit_and_evaluate(model,X_train, y_train,X_test,y_test):
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions and evalute
    model_pred = model.predict(X_test)
    model_mae = mae(y_test, model_pred)
    
    # Return the performance metric
    return model_mae

