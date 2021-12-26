# -*- coding: utf-8 -*-
"""BART_abs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m3PRzNLYKL7usRuxE8MUH4FxO8xHYp9u
"""

#!pip install transformers==2.11.0
"""
from ExtractiveSummarizer import summary as extractive_summary
from ExtractiveSummarizer import retention_percentage as extractive_retention_percentage
from ExtractiveSummarizer import no_of_sentences as extractive_num_sentences
from ExtractiveSummarizer import word_count as extractive_word_count
from ExtractiveSummarizer import default_retention_percentage as default_retention_percentage_extractive
"""
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig
from transformers import pipeline

import re

#Initializing global variables

BART_PATH = 'facebook/bart-large-cnn'
bart_model = BartForConditionalGeneration.from_pretrained(BART_PATH, output_past=True)
bart_tokenizer = BartTokenizer.from_pretrained(BART_PATH, output_past=True)


import nltk
nltk.download('punkt')
nltk.download('stopwords')
device = 'cuda'

def nest_sentences(document):
  nested = []
  sent = []
  length = 0
  token =  nltk.sent_tokenize(document)
  for sentence in token:
    length += len(sentence.split(' '))
    if length < 256:
      sent.append(sentence)
    else:
      nested.append(sent)
      sent = []
      length = 0

  if sent:
    nested.append(sent)

  print("Nested: ", nested)
  print("Nested Count: ", len(nested))
  for i in nested:
    print("Sentence count in each nested list: ", len(i))
  return nested



def generate_summary_HF(nested_sentences):
    DOCUMENT = extractive_summary
    start = '<START>'
    end = '<END>'
    DOCUMENT = start + DOCUMENT +end
    DOCUMENT = re.sub(r'\n|\r', ' ', DOCUMENT)
    DOCUMENT = re.sub(r' +', ' ', DOCUMENT)
    DOCUMENT = DOCUMENT.strip()
    nested = nest_sentences(DOCUMENT)

    default_error_percentage = 15
    min_summary_length = int((((extractive_retention_percentage - default_error_percentage)/100)*extractive_word_count)/len(nested))
    max_summary_length = int(((extractive_retention_percentage + default_error_percentage)/100)*extractive_word_count/len(nested))

    print("Min summary length", min_summary_length)
    print("Max summary length", max_summary_length)
    print("Extractive Number of Sentences", extractive_num_sentences)
    summaries = []
    for nested in nested_sentences:
        concat_text = ""
        for sent in nested:
            concat_text += sent
            summarizer = pipeline("summarization")
            summarized = summarizer(concat_text,  min_length =min_summary_length, max_length=max_summary_length, clean_up_tokenization_spaces = True, do_sample=False)
            summaries.append(summarized)
    return summaries


def generate_summary(summary, extractive_retention_percentage, extractive_num_sentences, extractive_word_count, default_retention_percentage_extractive):
    DOCUMENT = summary
    start = '<START>'
    end = '<END>'
    DOCUMENT = start + DOCUMENT +end
    DOCUMENT = re.sub(r'\n|\r', ' ', DOCUMENT)
    DOCUMENT = re.sub(r' +', ' ', DOCUMENT)
    DOCUMENT = DOCUMENT.strip()
    nested_sentences = nest_sentences(DOCUMENT)

    default_error_percentage = 15
    if(len(nested_sentences))>0:
        min_summary_length = int((((extractive_retention_percentage - default_error_percentage)/100)*extractive_word_count)/len(nested_sentences))
        max_summary_length = int(((extractive_retention_percentage + default_error_percentage)/100)*extractive_word_count/len(nested_sentences))
    else:
        min_summary_length = 0
        max_summary_length = 0

    print("Min summary length", min_summary_length)
    print("Max summary length", max_summary_length)
    print("Extractive Number of Sentences", extractive_num_sentences)
    #device = 'cuda'
    summaries = []
    for nested in nested_sentences:
        input_tokenized = bart_tokenizer.encode(' '.join(nested), truncation=False, return_tensors='pt', add_special_tokens = False, verbose = True)
        #input_tokenized = input_tokenized.to(device)
        summary_ids = bart_model.generate(input_tokenized,
                                    
                                        num_beams=5,
                                        no_repeat_ngram_size=2,
                                        min_length = min_summary_length,
                                        max_length = max_summary_length,
                                    
                                        )
        output = [bart_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in summary_ids]
        summaries.append(output)
    #summaries = [sentence for sublist in summaries for sentence in sublist]
    return summaries


def getAbstractiveSummary(summary, retention_percentage, no_of_sentences, word_count, default_retention_percentage):
    extractive_summary = summary
    extractive_retention_percentage = retention_percentage
    extractive_num_sentences = no_of_sentences
    extractive_word_count = word_count
    default_retention_percentage_extractive = default_retention_percentage
    summ = generate_summary(summary, retention_percentage, no_of_sentences, word_count, default_retention_percentage)
    #summ = generate_summary_HF(nested)
    #print("Retention percentage (Approx): ", extractive_retention_percentage)
    #print(summ)
    return summ[0][0]

"""    
print("\n\nExtractive/Long Summary: ")
print("Retention Percentage", extractive_retention_percentage+default_retention_percentage_extractive)
print("{}".format(extractive_summary))

print("\n\nAbstractive/Short Summary: ")
if extractive_retention_percentage>=75:
  summ = extractive_summary
  print("Retention Percentage", extractive_retention_percentage)
  print("{}".format(extractive_summary))
else:
  summ = generate_summary(nested)
  #summ = generate_summary_HF(nested)
  print("Retention percentage (Approx): ", extractive_retention_percentage)
  print(summ)


print("\n\nOne-Line Summary: ", oneLineSummaryList[0])

#summ = generate_summary_HF(nested)
#print(summ)

"""
