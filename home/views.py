from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .Environment import Environment
def index(request):

    response = json.dumps([{}])
    return HttpResponse(response, content_type="text/json")


@csrf_exempt
def resolve(request):
    if(request.method == "POST"):
        br = []
        data = json.loads(request.body)
        n = data["n"]
        br = data["data"]
        a = Environment(n,br)
        res = a.expand(a.idaStar)
       
        res = str(res)
       
        response = json.dumps([{'table': res}])
    return HttpResponse(response,status=200)
