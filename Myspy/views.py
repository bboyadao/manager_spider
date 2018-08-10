from django.shortcuts import render
import requests
import json
from django.http import HttpResponse

# HARD-CODE URL
url_list_project= "http://localhost:6800/listprojects.json"
url_list_spiders ="http://localhost:6800/listspiders.json?project="
url_supervise = "http://localhost:6800/listjobs.json?project="
url_schedule = "http://localhost:6800/schedule.json"
url_cancel_job = "http://localhost:6800/cancel.json"


def index(request):
    context={}
    project = request.GET.get("project")
    spider = request.GET.get("spider")
    cmd = request.GET.get("cmd")
    job = request.GET.get("job")
    get_proj = requests.get(url_list_project)
    projects = json.loads(get_proj.content)["projects"]
    context["projects"]= projects       
    
    
    if project:        
        get_spiders = requests.get(url_list_spiders+project)
        spiders = json.loads(get_spiders.content)["spiders"]
        context["spiders"]= spiders
        supervise = requests.get(url="{}{}".format(url_supervise,project))
        pending = json.loads(supervise.content)["pending"]
        running = json.loads(supervise.content)["running"]
        finished = json.loads(supervise.content)["finished"]    
        
        context['running']=running
        context["finished"]= finished
        context["pending"]= pending
        

    if project and spider and cmd:
        if cmd == "start":
            start_spider(project, spider)

    if job and project:
        cancel_job(project, job)


    return render(request, "index.html", context)
    
def show_log(request):    
    project = request.GET.get("project")
    spider = request.GET.get("spider")
    job = request.GET.get("job")
    url = f"http://localhost:6800/logs/{project}/{spider}/{job}.log"
    r = requests.get(url)
    return HttpResponse (r.content)


def start_spider(project,spider):
    param = {
    "project": project
    ,"spider":spider
    }
    r = requests.post(url=url_schedule, data=param, timeout=10)
    data = r.content
    return data


def cancel_job(project, job):
    param = {
         "project": project
        ,"job": job
        }
    r = requests.post(url=url_cancel_job, data=param)    
    return r.content