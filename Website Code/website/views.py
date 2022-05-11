from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import os
from .Summarizerpythonfiles import ExtractiveSummarizer as extractive
from .Summarizerpythonfiles import AbstractiveSummarizer as abstractive
from .Summarizerpythonfiles import HybridSummarizer as hybrid
from .Summarizerpythonfiles import SpeechToText as stt
from .Summarizerpythonfiles import ExtractiveSummarizerCentroid as extractivenew


import urllib
from django.contrib.auth.decorators import login_required


# def index(request):
#     return HttpResponse('Just started')
BASE_DIR = Path(__file__).resolve().parent

# @login_required
# class Home(TemplateView):
#     template_name='home.html'

CONTENT=''
FNAME=''
FTYPE=''
@login_required
def home(request):
    return render(request, 'home.html')

def upload(request):
    context={}
    global CONTENT,FNAME,FTYPE
    print(request.POST)
    if request.method== 'POST' and "document" in request.POST:
        uploaded_file= request.FILES['document']
        print(uploaded_file.name)
        FNAME=uploaded_file.name
        FTYPE='text'
        fs= FileSystemStorage(location='website/media/documents/')
        file_name=fs.save(uploaded_file.name, uploaded_file)
        
        file_content=open(os.path.join(BASE_DIR,'media\\documents',file_name),"r",encoding="utf-8").read()
        print("\n"+file_content)
        context['file_content']=file_content
        CONTENT=file_content

    return render(request, 'TextUpload.html',context)

def mediaUpload(request):
    context={}
    global CONTENT,FTYPE,FNAME
    print(request.POST)
    if request.method== 'POST' and "media" in request.POST:
        uploaded_file= request.FILES['media']
        print(uploaded_file.name)
        fs= FileSystemStorage(location='website/media/AV/')
        file_name=fs.save(uploaded_file.name, uploaded_file)
        FNAME=uploaded_file.name

        FTYPE='audio'
        
        #file_content=open(os.path.join(BASE_DIR,'media/AV',file_name),"r",encoding="utf-8").read()
        # print("\n"+file_content)

        #####################################################
        ######### ADD ASR MODULE REDIRECT HERE#############
        #################################################
        ### BELOW 3 LINES ARE PLACEHOLDERS###########3
        # file_content=open(os.path.join(BASE_DIR,'media\\AV',file_name),"r",encoding='latin-1').read()
        # print("\n"+file_content)  
        file_content=stt.get_transcripts(FNAME)

        context['file_content']=file_content
        CONTENT=file_content

    return render(request, 'MediaUpload.html',context)

    
def login(request):
    return render(request,'account/login.html')

def summary(request):
    global CONTENT,FNAME,FTYPE
    print(request.GET)


    if request.method=='GET' and "retention" in request.GET:
        
        context={}
        retention=int(request.GET.getlist("retention")[0])
        print(retention)
        #Extractive Summary
        extractive_summary, one_line_summary, abstractive_summary = hybrid.generateHybridSummary(FTYPE,FNAME,retention)
        context['extractive_summary']=extractive_summary
        context['abstractive_summary']=abstractive_summary
        context['one_line_summary']=one_line_summary
        print("Extractive Summary: ", extractive_summary)
        print("One-Line summary: ", one_line_summary)
        print("Abstractive Summary: ", abstractive_summary)

    return render(request, 'summary.html',context)

def notes(request):
    context={}
    global CONTENT,FNAME,FTYPE
    input_text,text_sen,text_words = extractivenew.input_txt_length(FTYPE,FNAME)
    context['text_sen'] = text_sen
    context['text_words'] = text_words 
    context['input_text'] = input_text 
    print("Text sentences", text_sen) 
    return render(request, 'notes.html',context)

def gen_notes(request):
    global CONTENT,FNAME,FTYPE
    print(request.GET)
    if request.method=='GET' and "nos" in request.GET:
        context={}
        nos=int(request.GET.getlist("nos")[0])
        print(nos)
        notes, text_word_count, text_sent_count, summ_sent_count, summ_word_count = extractivenew.get_extractive_summary(FTYPE, FNAME, 'sentence', nos)
        context['notes']= notes
        context['text_word_count']= text_word_count
        context['text_sent_count']= text_sent_count
        context['summ_sent_count'] = summ_sent_count
        context['summ_word_count'] = summ_word_count
        print("Extractive Summary: ", notes)
        print("Text words: ", text_word_count)
        print("Text sentences: ", text_sent_count)
        print("Summ sentences: ", summ_sent_count)
        print("Summ words: ", summ_word_count)
    return render(request, 'notes.html',context)    
        