import math
import numpy as np
import pandas as pd
import re
import os
import random
import string

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from scipy.spatial.distance import cosine

from .SpeechToText import get_transcripts
nltk.download('punkt')

def preprocess_input_text(text):
    stop_words = set(stopwords.words('english'))
    sentences = sentence_tokenize(text)
    preprocessed_sentences = []
    for sent in sentences:
        words = word_tokenize(sent)
        words = [w for w in words if w not in string.punctuation]
        words = [w for w in words if not w.lower() in stop_words]
        words = [w.lower() for w in words]
        preprocessed_sentences.append(" ".join(words))
    return preprocessed_sentences

def sentence_tokenize(text):
    sents = sent_tokenize(text)
    sents_filtered = []
    for s in sents:
        sents_filtered.append(s)
    return sents_filtered


def calculate_tf_idf(sentences):
    vectorizer = CountVectorizer()
    sent_word_matrix = vectorizer.fit_transform(sentences)
    transformer = TfidfTransformer(norm=None, sublinear_tf=False, smooth_idf=False)
    tfidf = transformer.fit_transform(sent_word_matrix)
    tfidf = tfidf.toarray()
    centroid_vector = tfidf.sum(0)
    centroid_vector = np.divide(centroid_vector, centroid_vector.max())
    feature_names = vectorizer.get_feature_names_out()
    centroid_limit = 0.3
    relevant_vector_indices = np.where(centroid_vector > centroid_limit)[0]

    word_list = list(np.array(feature_names)[relevant_vector_indices])
    return word_list

def word_vectors_cache(sentences, embedding_model):
    word_vectors = dict()
    for sent in sentences:
        words = word_tokenize(sent)
        for w in words:
            word_vectors.update({w: embedding_model.wv[w]})
    return word_vectors

def build_embedding_representation(words, word_vectors, embedding_model):
    embedding_representation = np.zeros(embedding_model.vector_size, dtype="float32")
    word_vectors_keys = set(word_vectors.keys())
    count = 0
    for w in words:
        if w in word_vectors_keys:
            embedding_representation = embedding_representation + word_vectors[w]
            count += 1
    if count != 0:
        embedding_representation = np.divide(embedding_representation, count)
    return embedding_representation

def calculate_cosine_similarity(vector1, vector2):
    score = 0.0
    if np.count_nonzero(vector1) != 0 and np.count_nonzero(vector2) != 0:
        score = ((1 - cosine(vector1, vector2)) + 1) / 2
    return score

def generate_summary(text, embedding_model):
    raw_sentences = sentence_tokenize(text)
    clean_sentences = preprocess_input_text(text)
    centroid_words = calculate_tf_idf(clean_sentences)
    word_vectors = word_vectors_cache(clean_sentences, embedding_model)
    centroid_vector = build_embedding_representation(centroid_words, word_vectors, embedding_model)
    sentences_scores = []
    for i in range(len(clean_sentences)):
        scores = []
        words = clean_sentences[i].split()
        sentence_vector = build_embedding_representation(words, word_vectors, embedding_model)
        score = calculate_cosine_similarity(sentence_vector, centroid_vector)
        sentences_scores.append((i, raw_sentences[i], score, sentence_vector))
    sentence_scores_sort = sorted(sentences_scores, key=lambda el: el[2], reverse=True)
    return sentence_scores_sort

def remove_redundancy(sentence_scores, limit,limit_type ):
    count = 0
    sentences_summary = []
    for s in sentence_scores:
        if count==limit:
            break
        include_flag = True
        for ps in sentences_summary:
            sim = calculate_cosine_similarity(s[3], ps[3])
            if sim > 0.95:
                include_flag = False
        if include_flag:
            sentences_summary.append(s)
            if limit_type == "word":
                count += len(s[1].split())
            elif limit_type == "sentence":
                count += 1

        sentences_summary = sorted(sentences_summary, key=lambda el: el[0], reverse=False)

    summary = " ".join([s[1] for s in sentences_summary])
    return summary



def get_word_count(test_string):
    res = sum([i.strip(string.punctuation).isalpha() for i in test_string.split()])
    return int(res)

def get_extractive_summary(sample_text, limit_type, limit):
    if(limit_type=='sentence' or limit_type=='word' or limit_type == 'retention_percentage'):
        preprocessed_sentences = preprocess_input_text(sample_text)
        tokenized_words = []
        for sent in preprocessed_sentences:
            tokenized_words.append(word_tokenize(sent))

        embedding_model = Word2Vec(tokenized_words, min_count=1, sg = 1, epochs = 1000)

        text_sent_count = len(preprocessed_sentences)
        text_word_count = len(sample_text.split())

        sentence_scores = generate_summary(sample_text, embedding_model)
        if limit_type == "retention_percentage":
            limit = int((limit/100)*text_sent_count)
            limit_type = 'sentence'
        extractive_summary = remove_redundancy(sentence_scores, limit, limit_type)

        summ_word_count = len(extractive_summary.split())
        summ_sent_count = len(sent_tokenize(extractive_summary))

        return extractive_summary, text_word_count, text_sent_count, summ_sent_count, summ_word_count
    else:
        raise Exception("Invalid Limit Type. Try 'sentence' or 'word'.")



