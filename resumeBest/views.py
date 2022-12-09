
from django.shortcuts import render,redirect
from .models import UploadPdf
from .codeLogic import remove_stopwords,remove_specialChar,onlyText,prediction
import os
from django.contrib import messages

def index(request):
    context={
        "result":[]
    }

    if request.method=="POST":
        try:
            skills=request.POST.get("job_skills")
            # exception handling for wordcloud if there is no text given in skills
            
            files=request.FILES.getlist("uploadfiles")

            for f in files:
                UploadPdf(jobDescription=skills,resumes=f).save()
                
            
            path1=os.getcwd()
            print(path1)
            a=prediction(os.path.join(path1,"media\\"),skills)
            
            b=[]
            for x in a["result"]:
                b.append({"f_name":a["resumeName"][x[0]],"similar_percent":x[1]})
            
            context={
                "result":b
            }
            
            return render(request,"resumeBest/index.html",context)

        except FileNotFoundError:
            messages.error(request,"First Upload PDF Files!")

            return render(request,"resumeBest/index.html")

    
    return render(request,"resumeBest/index.html")
