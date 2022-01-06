import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from . import CreateGif

class Home(TemplateView):
    template_name = 'home.html'

def button(request):
    return render(request,'home.html')

def external(request):
    name= request.POST.get('param')
    video=request.FILES['video']
    fs=FileSystemStorage()
    filename=fs.save(video.name,video)
    fileurl=fs.open(filename)
    templateurl=fs.url(filename)
 
    gifSavePath= CreateGif.createGif(str(fileurl),str(filename),name)

    gif_name=os.path.basename(gifSavePath)

    gif_url=fs.url(gif_name)
    return render(request,'home.html',{'raw_url':templateurl,'edit_url':gif_url})
