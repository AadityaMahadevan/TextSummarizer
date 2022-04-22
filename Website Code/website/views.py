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
from clients import twilio_client
from .forms import VerificationForm, TokenForm
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


def verified(request):
    if not request.session.get('is_verified'):
        return redirect('phone_verification')
    return render(request, 'home.html')

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
        