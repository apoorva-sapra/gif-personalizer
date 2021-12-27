import os
import re
from typing import Pattern
import requests
from django.shortcuts import render
import sys
from subprocess import run,PIPE
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'home.html'

def button(request):
    return render(request,'home.html')

def external(request):
    # print("REQUEST-------->",request)
    name= request.POST.get('param')
    # print("INP---------->",name)
    video=request.FILES['video']
    # print("video is ------>",video)
    fs=FileSystemStorage()
    filename=fs.save(video.name,video)
    fileurl=fs.open(filename)
    templateurl=fs.url(filename)
    # print("file raw url",filename)
    # print("file full url", fileurl)
    # print("template url",templateurl)
    # out= run([sys.executable,'D://apoorva//vidgif//OutlookAddIn//API//test.py',name],shell=False,stdout=PIPE)
    gif= run([sys.executable,'D://apoorva//vidgif//OutlookAddIn//API//AddImageAndTextInAllFrames.py',str(fileurl),str(filename),name],shell=False,stdout=PIPE)
    
    # out.stdout=out.stdout.strip().decode( "utf-8" )
    gif.stdout=gif.stdout.strip().decode( "utf-8" )
    # print("OUT  ------------>   ",out)
    # print("gif STDOUT     ------------>   ",gif.stdout)
    
    # print("\n\n\n", os.path.basename(gif.stdout))
    gif_name=os.path.basename(gif.stdout)
    gif_url=fs.url(gif_name)
    # print("\n gif url => ", gif_url)
    return render(request,'home.html',{'raw_url':templateurl,'edit_url':gif_url})
