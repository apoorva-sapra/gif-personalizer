import os
from django.shortcuts import render
import sys
from subprocess import run,PIPE
from django.core.files.storage import default_storage as ds
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'home.html'

def button(request):
    return render(request,'home.html')

def external(request):
    name= request.POST.get('param')
    video=request.FILES['video']
    filename=ds.save(video.name,video)
    fileurl=ds.open(filename)
    templateurl=ds.url(filename)

    print("video saved")
    print("fileurl",fileurl)
    
    #changing \\ to / for correct path route on azure
    GIF_CREATOR_FILE="/AddImageAndTextInAllFrames.py"
    
    currentfiles=os.listdir()
    
    os.chdir('../')
    rootPath=os.getcwd()
    rootfiles=os.listdir()
    
    os.chdir('PythonApi')
    
    gifCreatorFilePath=rootPath+GIF_CREATOR_FILE
    
    gif= run([sys.executable,gifCreatorFilePath,str(templateurl),str(filename),name],shell=False, capture_output=True)
    
    # out.stdout=out.stdout.strip().decode( "utf-8" )
    gif.stdout=gif.stdout.strip().decode( "utf-8" )
    
    # print("\n\n\n", os.path.basename(gif.stdout))
    gif_name=os.path.basename(gif.stdout)
    gif_url=ds.url(gif_name)
    # print("\n gif url => ", gif_url)
    return render(request,'home.html',{'raw_url':templateurl,'edit_url':gif_url})
