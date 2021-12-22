from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import os
from . import extractive

# def index(request):
#     return HttpResponse('Just started')
BASE_DIR = Path(__file__).resolve().parent

class Home(TemplateView):
    template_name='home.html'

CONTENT=''

def upload(request):
    context={}
    global CONTENT
    print(request.POST)
    if request.method== 'POST' and "document" in request.POST:
        uploaded_file= request.FILES['document']
        print(uploaded_file.name)
        fs= FileSystemStorage()
        file_name=fs.save(uploaded_file.name, uploaded_file)
        
        file_content=open(os.path.join(BASE_DIR,'media',file_name),"r",encoding="utf-8").read()
        print("\n"+file_content)
        context['file_content']=file_content
        CONTENT=file_content

    return render(request, 'upload.html',context)

def summary(request):
    global CONTENT
    print(request.GET)


    if request.method=='GET' and "retention" in request.GET:
        
        context={}
        retention=int(request.GET.getlist("retention")[0])
        print(retention)
        summary=extractive.main(CONTENT,retention)
        context['file_summary']=summary

    return render(request, 'summary.html',context)
        