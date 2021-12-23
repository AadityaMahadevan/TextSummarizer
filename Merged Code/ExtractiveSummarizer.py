# -*- coding: utf-8 -*-
"""ExtractiveSummary-TFIDF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jG8vIhc2XoQu3aVGA9lhEhW50hJfHJSV

Extractive Summary (Using TF-IDF and Cosine Distance)

Steps: Input document -> Finding most important words from the document -> Finding sentence scores on the basis of important words -> Choosing the most important sentences on the basis of scores obtained/Finding similarity between sentences and ranking them based on pairwise cosine similarity (combining with the approach used in Cosine Distance summary extraction)-> Merging the chosen sentences to form a summary.

Formulas Used:
TF(w) = (Number of times term w appears in a document) / (Total number of terms in the document)

IDF(w) = log_e(Total number of documents / Number of documents with term w in it)

TFIDF(w) = TF(w) * IDF(w)

Cos(x, y) = x . y / ||x|| * ||y||

> Importing necessary libraries
"""

import nltk
import os
import re
import math
import operator
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
Stopwords = set(stopwords.words('english'))
wordlemmatizer = WordNetLemmatizer()

#from google.colab import drive
#drive.mount('/content/drive' )

"""> Text preprocessing

The pre-processing steps applied in this algorithm include removing special characters, digits, one-letter words and stop words from the text .

Function to remove special characters from the text
"""
def removeSpecialCharacters(text):
    regex = r'[^a-zA-Z0-9\s]'
    text = re.sub(regex,'',text)
    return text

"""Function to tokenize sentences"""

def tokenizeSentences():
  file = 'inputtext.txt'
  file = open(file , 'r', encoding="utf8")
  text = file.read()
  #Tokenize Sentences
  tokenized_sentence = sent_tokenize(text)
  #Removing Special Characters
  text = removeSpecialCharacters(str(text))
  text = re.sub(r'\d+', '', text)
  #Tokenize Words

  tokenized_words = word_tokenize(text)
  word_count = len(tokenized_words)
  print("Word count: ", len(tokenized_words))
  #Remove Stop Words
  tokenized_words_without_stopwords = [word for word in tokenized_words if word not in Stopwords]
  #Remove Single Letter words
  tokenized_words_without_stopwords = [word for word in tokenized_words_without_stopwords if len(word) > 1]
  #Convert all tokenized words into lower case to remove ambiguity
  tokenized_words_without_stopwords = [word.lower() for word in tokenized_words_without_stopwords]
  return tokenized_words_without_stopwords, tokenized_sentence, word_count

"""Function to calculate the frequency of each word in the document"""

def calculateWordFrequency(words_list):
    words_list = [word.lower() for word in words_list]
    frequency = {}
    unique_words = []
    #Find all unique words
    for word in words_list:
       if word not in unique_words:
          unique_words.append(word)
    for word in unique_words:
          frequency[word] = words_list.count(word)
    return frequency

"""Function to calculate sentence scores (Using TF-IDF)

Utility functions for sentence scoring: 

1. POS tagging function (Part of Speech tagging): Using nltk library to pos tag all the words in the text and returns only the nouns and verbs from the text.
"""

def posTagging(text):
    pos_tag = nltk.pos_tag(text.split())
    pos_tagged_noun_verb = []
    for word,tag in pos_tag:
        if tag == "NN" or tag == "NNP" or tag == "NNS" or tag == "VB" or tag == "VBD" or tag == "VBG" or tag == "VBN" or tag == "VBP" or tag == "VBZ":
            pos_tagged_noun_verb.append(word)
    return pos_tagged_noun_verb

"""2. Stemming:  extract the base form of the words by removing affixes"""

def stemWords(words):
    stemmed_words = []
    for word in words:
       stemmed_words.append(stemmer.stem(word))
    return stemmed_words

"""3. Lemmatization: grouping together the different inflected forms of a word so they can be analyzed as a single item in context to the word"""

def lemmatizeWords(words):
    lemmatized_words = []
    for word in words:
       lemmatized_words.append(wordlemmatizer.lemmatize(word))
    return lemmatized_words

"""4. TF score: It is calculated as the number of times the word appears in the sentence upon the total number of words in the sentence."""

def tfScore(word,sentence):
    freq_sum = 0
    word_frequency_in_sentence = 0
    len_sentence = len(sentence)
    for word_in_sentence in sentence.split():
        if word == word_in_sentence:
            word_frequency_in_sentence = word_frequency_in_sentence + 1
    tf =  word_frequency_in_sentence/ len_sentence
    return tf

"""5. IDF score: This function finds the idf score of the word, by dividing the total number of sentences by number of sentences containing the word and then taking a log10 of that value."""

def idfScore(no_of_sentences,word,sentences):
    no_of_sentence_containing_word = 0
    for sentence in sentences:
        sentence = removeSpecialCharacters(str(sentence))
        sentence = re.sub(r'\d+', '', sentence)
        sentence = sentence.split()
        sentence = [word for word in sentence if word.lower() not in Stopwords and len(word)>1]
        sentence = [word.lower() for word in sentence]
        sentence = [wordlemmatizer.lemmatize(word) for word in sentence]
        if word in sentence:
            no_of_sentence_containing_word = no_of_sentence_containing_word + 1
    idf = math.log10(no_of_sentences/no_of_sentence_containing_word)
    return idf

"""6. TF-IDF score: multiplies tf and idf values"""

def calculateTfIdfScore(tf,idf):
   return tf*idf

"""TF-IDF score for all tokenized words"""

def tfidfAllWords(dict_freq,word,sentences,sentence):
    word_tfidf = []
    tf = tfScore(word,sentence)
    idf = idfScore(len(sentences),word,sentences)
    tf_idf = calculateTfIdfScore(tf,idf)
    return tf_idf

"""Sentence Ranking using TF-IDF scores (Sum of TF-IDf scores of all words in the sentence)"""

def calculateSentenceScore(sentence,frequency,sentences):
     sentence_score = 0
     sentence = removeSpecialCharacters(str(sentence))
     sentence = re.sub(r'\d+', '', sentence)
     pos_tagged_sentence = []
     no_of_sentences = len(sentences)
     pos_tagged_sentence = posTagging(sentence)
     for word in pos_tagged_sentence:
         if word.lower() not in Stopwords and word not in Stopwords and len(word)>1:
             word = word.lower() 
             word = wordlemmatizer.lemmatize(word)
             sentence_score = sentence_score + tfidfAllWords(frequency,word,sentences,sentence)
     return sentence_score

"""Calculating Cosine Similarity"""

#Calculate cosine similarity

"""Calling word tokenization function, performing lemmatization on tokenized words and calculating word frequency"""

tokenized_words, tokenized_sentences, word_count = tokenizeSentences()
tokenized_words = lemmatizeWords(tokenized_words)
word_frequency = calculateWordFrequency(tokenized_words)

"""Taking input from the user: Percentage of retained context from the original text in the summary"""

default_retention_percentage = 15
default_overflow_percentage = 90

retention_percentage = int(input('Percentage of information to retain (in percent):'))
if retention_percentage<=30:
    default_retention_percentage = default_retention_percentage*2
elif retention_percentage >=75:
    default_retention_percentage = 0

if retention_percentage + default_retention_percentage >= 100:
    int(((default_overflow_percentage) * len(tokenized_sentences))/100)
else:
    no_of_sentences = int(((retention_percentage + default_retention_percentage) * len(tokenized_sentences))/100)
print("Number of sentences in the summary: ", no_of_sentences, "\nTotal number of sentences: ", len(tokenized_sentences))


"""Generate summary by sorting the sentences based on the sum of tf-idf scores of all the words in the sentence."""
c = 1
sentence_scores = {}
for sent in tokenized_sentences:
    sentence_importance = calculateSentenceScore(sent,word_frequency,tokenized_sentences)
    sentence_scores[c] = sentence_importance
    c = c+1
sentence_scores = sorted(sentence_scores.items(), key=operator.itemgetter(1),reverse=True)
count = 0
summary = []
sentence_no = []
for word in sentence_scores:
    if count < no_of_sentences:
        sentence_no.append(word[0])
        count = count+1
    else:
      break
sentence_no.sort()
count = 1
for sentence in tokenized_sentences:
    if count in sentence_no:
       summary.append(sentence)
    count = count+1

summary = " ".join(summary)




"""Print Summary

print("Summary:")
lines = summary.split('.')
for line in lines:
  print(line)
  """