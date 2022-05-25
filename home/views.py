from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from home.Taquin import Taquin

def index(request):

    response = json.dumps([{}])
    return HttpResponse(response, content_type="text/json")


@csrf_exempt
def resolve(request):
    if(request.method == "POST"):
        br = []
        data = json.loads(request.body)
        br = data["data"]
        goal = [[1,2,3],[4,5,6],[7,8,0]]
        p = Taquin(br,3,goal)

        res=p.a_star_search()
       
        response = json.dumps([{'table': res}])
    return HttpResponse(response,status=200)
