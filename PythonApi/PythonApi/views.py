import os
from django.shortcuts import render
import sys
from subprocess import run,PIPE
from django.core.files.storage import default_storage as fs
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'home.html'

def button(request):
    return render(request,'home.html')

def external(request):
    name= request.POST.get('param')
    video=request.FILES['video']
    filename=fs.save(video.name,video)
    fileurl=fs.open(filename)
    templateurl=fs.url(filename)

    GIF_CREATOR_FILE="\\AddImageAndTextInAllFrames.py"
    os.chdir('../')
    rootPath=os.getcwd()
    os.chdir('PythonApi')
    gifCreatorFilePath=rootPath+GIF_CREATOR_FILE

    gif= run([sys.executable,gifCreatorFilePath,str(fileurl),str(filename),name],shell=False,stdout=PIPE)
    
    # out.stdout=out.stdout.strip().decode( "utf-8" )
    gif.stdout=gif.stdout.strip().decode( "utf-8" )
    
    # print("\n\n\n", os.path.basename(gif.stdout))
    gif_name=os.path.basename(gif.stdout)
    gif_url=fs.url(gif_name)
    # print("\n gif url => ", gif_url)
    return render(request,'home.html',{'raw_url':templateurl,'edit_url':gif_url})
