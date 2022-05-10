from SpeechToText import get_transcripts
from OneLineSummaryT5 import get_one_line_summary
from ExtractiveSummarizerCentroid import get_extractive_summary
from FineTunedBARTSummarizer import get_abstractive_summary
# from AbstractiveSummarizer import get_abstractive_summary
import string


def generateInputText(input_type, file_name):
    #Get input text/Extract Transcripts
    if input_type == 'audio' or input_type == 'video':
        input_text = get_transcripts(file_name)
    elif input_type == 'text':
        file = open(file_name , 'r', encoding="utf8")
        input_text = file.read()
    
    return input_text

def getWordCount(test_string):
    res = sum([i.strip(string.punctuation).isalpha() for i in test_string.split()])
    return int(res)

def generateExtractiveSummary(input_type, input_text):
    """Get input text"""
    input_word_count = getWordCount(input_text)
    
    print("\nInput Text: \n {}".format(input_text))
    print("\n\nWord Count: {}\n".format(input_word_count))

    """ Parameters for extractive summarization"""
    #For Summarization
    minimum_word_count = 50
    retention_percent = 60
    word_limit = 256

    #For note-taking
    sentence_limit = 5
    #Type
    limit_type = 'word' #'sentence' or 'word' or 'retention_percentage'
    input_type = 'text' #'audio', 'video or 'text'

    """Get Extractive summary"""
    if input_word_count<minimum_word_count:
        extractive_summary = input_text
    else:
        if input_word_count<word_limit:
            limit_type = 'retention_percentage'
            extractive_summary, text_word_count, text_sent_count, summ_sent_count, summ_word_count = get_extractive_summary(input_text, limit_type, retention_percent)
        else:
            extractive_summary, text_word_count, text_sent_count, summ_sent_count, summ_word_count = get_extractive_summary(input_text, limit_type, word_limit)
        print("\nNumber of sentences: ", text_sent_count)
        print("\nNumber of words: ", text_word_count)
        print("\nNumber of sentences: ", summ_sent_count)
        print("\nNumber of words: ", summ_word_count)

    return extractive_summary

def generateOneLineSummary(input_text, extractive_summary):
    """ Parameters for extractive summarization"""
    one_line_summary_threshold = 512
    """Get One-Line Summary"""
    if getWordCount(input_text)<=one_line_summary_threshold:
        one_line_summary_input = input_text
    else:
        one_line_summary_input = extractive_summary 
        
    one_line_summary = get_one_line_summary(one_line_summary_input) 
    return one_line_summary

def generateAbstractiveSummary(extractive_summary):
    """ Parameters for extractive summarization"""
    # model_checkpoint_name = 'facebook/bart-base'
    # checkpoint_path = 'summarizer-checkpoint-bart-base-new.h5'
    model_checkpoint_name = 'facebook/bart-large-cnn'
    checkpoint_path = 'summarizer-checkpoint-bart-large.h5'
    """Get Abstractive Summary"""
    abstractive_summary =  get_abstractive_summary(extractive_summary, checkpoint_path, model_checkpoint_name, 512)
    return abstractive_summary

file_name = 'inputtext.txt'
input_type = 'text' #'text', 'audio' or 'video'
input_text = generateInputText(input_type, file_name)

extractive_summary = generateExtractiveSummary(input_type, input_text)
print('\nExtractive Summary: \n', extractive_summary)

one_line_summary = generateOneLineSummary(input_text, extractive_summary)
print("\nOne Line Summary: ", one_line_summary)

abstractive_summary = generateAbstractiveSummary(extractive_summary)
print("\nAbstractive Summary: \n", abstractive_summary)

