from ast import Try
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .Aiscript import Taquin

br = []
t = None


def index(request):

    response = json.dumps([{}])
    return HttpResponse(response, content_type="text/json")

#get the result from the agent then send it to the client (frontend)
def get_result_from_AI(request):

    if(request.method == "GET"):
        b = executeAI(br)
        response = json.dumps([{'table': b}])

    return HttpResponse(response, content_type="text/json", status=200)

#run the agent code
def executeAI(br):
    t = Taquin(br)
    br = t.main()
    return br

#get data from client to handle it by the agent
@csrf_exempt
def post_data_to_ai(request):
    if(request.method == "POST"):
        data = json.loads(request.body)
        n = data["n"]
        for i in range(n):
            l = []
            for j in range(n):
                l.append(int(data["data"]["a"+str(i)+str(j)]))
            br.append(l)

    return HttpResponse(status=200)
