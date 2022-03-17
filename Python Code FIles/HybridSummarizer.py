from SpeechToText import get_transcripts
from OneLineSummary import get_one_line_summary
from ExtractiveSummarizer import get_extractive_summary
from AbstractiveSummarizer import get_abstractive_summary
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

def generateHybridSummary(input_type, file_name):
    #get input text
    input_text = generateInputText(input_type, file_name)
    print("\nInput Text: \n {}".format(input_text))
    #extractive summarization
    retention_percentage = 50
    extractive_summary, ex_retention_percentage, ex_no_of_sentences, ex_word_count, ex_default_retention_percentage, sentences, words = get_extractive_summary(retention_percentage, input_text)
    print("\nRetention Percentage: \n", retention_percentage)
    #one line summary generation
    if getWordCount(input_text)<=512:
        one_line_summary_input = input_text
    else:
        one_line_summary_input = extractive_summary #split extractive summary for the edge case where extractive summary < 512
        
    one_line_summary = get_one_line_summary(extractive_summary) #input_text as input gives better results but there is a limit of 512 tokens
    #Abstractive Summarization
    abstractive_summary, abstractive_retention_percentage = get_abstractive_summary(extractive_summary, ex_retention_percentage, ex_word_count, ex_no_of_sentences, ex_default_retention_percentage)

    return extractive_summary, one_line_summary, abstractive_summary


extractive_summary, one_line_summary, abstractive_summary = generateHybridSummary('audio', 'asoiafaudio.mp3')
#extractive_summary, one_line_summary, abstractive_summary = generateHybridSummary('video', 'asoiafvid.mp4')
#extractive_summary, one_line_summary, abstractive_summary = generateHybridSummary('text', 'inputtext.txt')
print('\nExtractive Summary: \n', extractive_summary)
print("\nOne Line Summary: ", one_line_summary)
print("\nHybrid Summary: \n{}".format(abstractive_summary))

