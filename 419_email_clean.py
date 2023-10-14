# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

'''
@author: Kaia Hu
Reference: https://gtraskas.github.io/post/spamit/

Files input: '419_2019_01.csv', '419_2019_02.csv' generated from 419_Scraping.py'''

""" Section 1: Data Cleaning """

jan = pd.read_csv('data/419_2019_01.csv')  
feb = pd.read_csv('data/419_2019_02.csv')  

#Swap the columns for Jan
jan = jan.rename(columns = {'Subject': 'Sender', 'Sender': 'Subject'})

#Concat to create a single df
scam_frame = [jan, feb]
scam = pd.concat(scam_frame)
scam = scam.drop(columns = ['Unnamed: 0'])

#-----------------------------------------------#

# Import ENRON email data 
enron = pd.read_csv('data/emails.csv')  
# Extract Subject
enron['Subject'] = enron['message'].str.extract('(?<=Subject:)(.*)(?=\\nMime-Version:)')
#Extract sender
enron['Sender'] = enron['message'].str.extract('(?<=\\nFrom:\s)(.*)(?=\\nTo:\s)')
#Extract content
enron['Content'] = enron['message'].str.extract('(?<=\\n\\n)(.*)$')
enron_c = enron[['Sender', 'Subject', 'Content']]

#-----------------------------------------------# 

#Some useful functions to help with text processing 
#Reference: https://gtraskas.github.io/post/spamit/

from string import punctuation
import re
def clean_email(email):
    """ Remove all punctuation, urls, numbers, and newlines.
    Convert to lower case.
    Args:
        email (unicode): the email
    Returns:
        email (unicode): only the text of the email
    """
    email = re.sub(r'http\S+', ' ', email)
    email = re.sub("\d+", " ", email)
    email = email.replace('\n', ' ')
    email = email.translate(str.maketrans("", "", punctuation))
    email = email.lower()
    return email

from nltk.stem.snowball import SnowballStemmer
# nltk.download('wordnet') # uncomment to download 'wordnet'
from nltk.corpus import wordnet as wn
def preproces_text(email):
    """ Split the text string into individual words, stem each word,
    and append the stemmed word to words. Make sure there's a single
    space between each stemmed word.
    Args:
        email (unicode): the email
    Returns:
        words (unicode): the text of the email
    """
    words = ""
    # Create the stemmer.
    stemmer = SnowballStemmer("english")
    # Split text into words.
    email = email.split()
    for word in email:
        # Optional: remove unknown words.
        # if wn.synsets(word):
        words = words + stemmer.stem(word) + " "
    return words

#-----------------------------------------------#

#Continue to clean up scam and email dataframes
enron_c['Content'] = enron_c['Content'].astype(str)
enron_c['Content_clean'] = enron_c['Content'].apply(clean_email).apply(preproces_text)
enron_c = enron_c.drop(columns = 'Content').rename(columns = {'Content_clean': 'Content'}) 
enron_c['Class'] = 0

enron_c = enron_c[enron_c['Content'] != '']
enron_c = enron_c[enron_c['Subject'] != '']
enron_c = enron_c[enron_c['Content'] != 'nan ']

enron_c = enron_c.sample(n = 9000)
#enron_c.to_csv('Enron_Email_9000.csv')
#enron_c.head(3)

# Do the same text cleaning on 419 scam emails 
scam['Content_clean'] = scam['Content'].apply(clean_email).apply(preproces_text)
scam = scam.drop(columns = 'Content').rename(columns = {'Content_clean': 'Content'}) 
scam['Class'] = 1
#scam.to_csv('Scam_clean.csv')
#scam.head()

"""Section 2: Modeling"""

"""
@author: Lydia
Reference: Email Spam Classifier Using Naive Bayes by Shubham Kumar Raj 
Link: https://medium.com/analytics-vidhya/email-spam-classifier-using-naive-bayes-a51b8c6290d4
"""

#scam = pd.read_csv('Scam_clean.csv')
#enron_c = pd.read_csv('Enron_Email_9000.csv')

all_email = pd.concat([scam, enron_c]).sample(frac = 1, random_state = 3)

# Make a word dictionary
words=[]
for email in all_email['Content']:
  words+=str(email).split(" ")

from collections import Counter
word_dict=Counter(words)
word_dict=word_dict.most_common(1000)

label = []
features = []

for email in all_email.iterrows(): 
    blob = str(email[1]['Content']).split(" ")
    data = []
    
    for i in word_dict: 
        data.append(blob.count(i[0]))
    features.append(data)
    if email[1]['Class'] == 1: 
        label.append(1)
    else: label.append(0)


#Now let's fit the multinomial naive bayes model
from sklearn.model_selection import train_test_split
X_train, X_test,y_train,y_test=train_test_split(features,label,test_size=0.2)   
 
from sklearn.naive_bayes import MultinomialNB
clf=MultinomialNB()
clf.fit(X_train,y_train)
from sklearn.metrics import accuracy_score
y_pred = clf.predict(X_test)
accuracy_score(y_pred,y_test)


# Make sure our prediction model work!
class Scam():
    def scam_email(self, new_email):
        # new_email = 'Win this lottery and get free money'  

        sample = []

        for i in word_dict: 
            sample.append(new_email.split(' ').count(i[0]))
        sample = np.array(sample)
        result = clf.predict(sample.reshape(1, 1000))
        if result == 1: 
            ret = 'Our algorithm determines that this piece of information is likely to be scam. Please be careful in proceeding further! '
            return ret
        else: 
            ret = 'Our algorithm determines that this piece of information is unlikely to be scam. You are good to go!'
            return ret

    
    
    
    

    
    
    
    
    
    
    
    
    