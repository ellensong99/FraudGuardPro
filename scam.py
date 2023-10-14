# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 22:13:40 2023

@author: Lydia
Reference: Email Spam Classifier Using Naive Bayes by Shubham Kumar Raj 
Link: https://medium.com/analytics-vidhya/email-spam-classifier-using-naive-bayes-a51b8c6290d4
"""

import pandas as pd
import numpy as np
scam = pd.read_csv('data/Scam_clean.csv')
enron_c = pd.read_csv('data/Enron_Email_9000.csv')

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
    
        
    
# Uncomment below line to run functions in this file
# Scam().scam_email()
    
    
    
    
    
    