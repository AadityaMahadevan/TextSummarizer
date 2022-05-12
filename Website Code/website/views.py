from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import os
# from .Summarizerpythonfiles import ExtractiveSummarizer as extractive
# from .Summarizerpythonfiles import AbstractiveSummarizer as abstractive
# from .Summarizerpythonfiles import HybridSummarizer as hybrid
from .Summarizerpythonfiles.FinalMeetingSummarizer import SpeechToText as stt
from .Summarizerpythonfiles.FinalMeetingSummarizer import ExtractiveSummarizerCentroid as extractivenew
from django.contrib.auth.decorators import login_required
from .forms import VerificationForm, TokenForm
from clients import twilio_client
from django.contrib import messages

from .Summarizerpythonfiles.FinalMeetingSummarizer import MeetingSummarizer as summarizer



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
TRANSCRIPT=''
PREVIEW=''


def phone_verification(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            request.session['phone_number'] = form.cleaned_data['phone_number']
            verification = twilio_client.verifications(form.cleaned_data['phone_number'], form.cleaned_data['via'])
            return redirect('token_validation')
    else:
        form = VerificationForm()
    return render(request, 'phone_verification.html', {'form': form})

def verified(request):
    if not request.session.get('is_verified'):
        return redirect('phone_verification')
    return render(request, 'home.html')

def token_validation(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            verification = twilio_client.verification_checks(request.session['phone_number'], form.cleaned_data['token'])

            if verification.status == 'approved':
                request.session['is_verified'] = True
                return redirect('verified')
            else:
                for error_msg in verification.errors().values():
                    form.add_error(None, error_msg)
    else:
        form = TokenForm()
    return render(request, 'token_validation.html', {'form': form})

@login_required
def home(request):
    global CONTENT,FNAME,FTYPE,TRANSCRIPT,PREVIEW
    CONTENT=''
    FNAME=''
    FTYPE=''
    TRANSCRIPT=''
    PREVIEW=''

    return render(request, 'home.html')

def textUpload(request):
    context={}
    global CONTENT,FNAME,FTYPE,PREVIEW
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
        PREVIEW=file_content  

    return render(request, 'upload-preview-transcripts/textUpload.html',context)

def mediaUpload(request):
    context={}
    global CONTENT,FTYPE,FNAME
    print(request.POST)
    if request.method== 'POST' and "media" in request.POST:
        uploaded_file= request.FILES['media']
        print(uploaded_file.name)
        fs= FileSystemStorage(location='website/media/AV/')
        file_name=fs.save(uploaded_file.name, uploaded_file)
        FNAME=file_name

        if file_name.endswith('.mp3'):
            FTYPE='audio'
        else:
            FTYPE='video'

        context['file_type']=FTYPE
        context['file_name']=FNAME
    return render(request, 'upload-preview-transcripts/mediaUpload.html',context)
    


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
        context['message']="File Uploaded Successfully"

        
        file_content=open(os.path.join(BASE_DIR,'media\\documents',file_name),"r",encoding="utf-8").read()
        print("\n"+file_content)
        context['file_content']=file_content
        CONTENT=file_content
        

    return render(request, 'TextUpload.html',context)


def transcriptsPreview(request):
    global TRANSCRIPT,PREVIEW
    context={}

    if request.method== 'POST' and "transcriptsPreview" in request.POST:
        file_content=stt.get_transcripts(os.path.join(BASE_DIR,'media\\AV',FNAME))
        context['file_content']=file_content
        TRANSCRIPT=file_content
        PREVIEW=file_content  

    return render(request, 'upload-preview-transcripts/transcripts.html',context)

def input_txt_length():
    preprocessed_sentences = extractivenew.preprocess_input_text(PREVIEW)
    text_sent_count = len(preprocessed_sentences)
    text_word_count = len(PREVIEW.split())

    return text_sent_count , text_word_count

def notes(request):
    context={}
    global CONTENT,FNAME,FTYPE
    text_sen,text_words = input_txt_length()
    context['text_sen'] = text_sen
    context['text_words'] = text_words 
    context['file_content'] = PREVIEW 
    print("Text sentences", text_sen) 
    return render(request, 'upload-preview-transcripts/noteTaking.html',context)

def gen_notes(request):
    global CONTENT,FNAME,FTYPE
    print(request.POST)
    if request.method=='POST' and "nos" in request.POST:
        context={}
        nos=int(request.POST.getlist("nos")[0])
        print(nos)

        notes, text_word_count, text_sent_count, summ_sent_count, summ_word_count = extractivenew.get_extractive_summary(sample_text=PREVIEW, limit_type='sentence', limit=nos)
        context['file_content']=PREVIEW
        context['notes']= notes
        context['text_word_count']= text_word_count
        context['text_sen']= text_sent_count
        context['summ_sent_count'] = summ_sent_count
        context['summ_word_count'] = summ_word_count
        print("Extractive Summary: ", notes)
        print("Text words: ", text_word_count)
        print("Text sentences: ", text_sent_count)
        print("Summ sentences: ", summ_sent_count)
        print("Summ words: ", summ_word_count)
    return render(request, 'upload-preview-transcripts/noteTaking.html',context)    

def download(request):
   # some code
    if request.method== 'POST' and "Transcripts" in request.POST:
        global TRANSCRIPT
        file_data = TRANSCRIPT
        response = HttpResponse(file_data, content_type='application/text charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="transcript.txt"'
        return response



# def mediaUpload(request):
#     context={}
#     global CONTENT,FTYPE,FNAME
#     print(request.POST)
#     if request.method== 'POST' and "media" in request.POST:
#         uploaded_file= request.FILES['media']
#         print(uploaded_file.name)
#         fs= FileSystemStorage(location='website/media/AV/')
#         file_name=fs.save(uploaded_file.name, uploaded_file)
#         FNAME=uploaded_file.name

#         FTYPE='audio'
        
#         #file_content=open(os.path.join(BASE_DIR,'media/AV',file_name),"r",encoding="utf-8").read()
#         # print("\n"+file_content)

#         #####################################################
#         ######### ADD ASR MODULE REDIRECT HERE#############
#         #################################################
#         ### BELOW 3 LINES ARE PLACEHOLDERS###########3
#         # file_content=open(os.path.join(BASE_DIR,'media\\AV',file_name),"r",encoding='latin-1').read()
#         # print("\n"+file_content)  
#         file_content=stt.get_transcripts(FNAME)

#         context['file_content']=file_content
#         CONTENT=file_content

#     return render(request, 'MediaUpload.html',context)

    
def login(request):
    return render(request,'account/login.html')


# def transcripts(request):
#     if request.method=='GET' and "retention" in request.GET:
#         context={}
#         transcripts_content=int(request.GET.getlist("retention")[0])
#     return(request,'')
        
def get_only_transcripts():
    global FNAME
    file_content=stt.get_transcripts(os.path.join(BASE_DIR,'media\\AV',FNAME))

    return file_content




def summary(request):
    global CONTENT,FNAME,FTYPE,PREVIEW
    if request.method=='POST' and "summary" in request.POST:
        context={}
        context['file_content']=CONTENT
        if PREVIEW=='':
            PREVIEW=get_only_transcripts()
        extractive_summary=summarizer.generateExtractiveSummary(input_type=FTYPE,input_text=PREVIEW,limit_type='word')
        one_line_summary=summarizer.generateOneLineSummary(input_text=PREVIEW,extractive_summary=extractive_summary)
        abstractive_summary=summarizer.generateAbstractiveSummary(extractive_summary=extractive_summary)
        context['file_content']=PREVIEW
        context['extractive_summary']=extractive_summary
        context['abstractive_summary']=abstractive_summary
        context['one_line_summary']=one_line_summary


        
    return render(request, 'upload-preview-transcripts/summary.html',context)

    # print(request.GET)


    # if request.method=='GET' and "retention" in request.GET:
        
    #     context={}
    #     retention=int(request.GET.getlist("retention")[0])
    #     print(retention)
    #     #Extractive Summary
    #     extractive_summary, one_line_summary, abstractive_summary = hybrid.generateHybridSummary(FTYPE,FNAME,retention)
        # context['extractive_summary']=extractive_summary
        # context['abstractive_summary']=abstractive_summary
        # context['one_line_summary']=one_line_summary
    #     print("Extractive Summary: ", extractive_summary)
    #     print("One-Line summary: ", one_line_summary)
    #     print("Abstractive Summary: ", abstractive_summary)

    # return render(request, 'upload-preview-transcripts/summary.html',context)
        