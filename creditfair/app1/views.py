from django.shortcuts import render
from .views_imports import *

# Create your views here.

@api_view(["GET"])
@validate_bearer_token
def append_nav(request):
    user_level = request.user.user_level
    process = request.user.process
    module = request.user.module
    return JsonResponse({'status':200,'user_level':user_level,"process":process})


@api_view(["POST"])
@validate_bearer_token
def cmsstrartstop(request):
    if request.method == 'POST':
        user_id = request.user.id
        dt=datetime.now()
        print(user_id,"userrrrrrrrrrrr")
        json_body=json.loads(request.body)
        print(json_body,"CMS START")
        status= json_body['status'] if 'status' in json_body else None
        Callcount=json_body['callCount'] if 'callCount' in json_body else None
        avg=json_body['avgTimeStr'] if 'avgTimeStr' in json_body else None
        mode=json_body['mode'] if 'mode' in json_body else None
        print("user_id","userid","status",status,Callcount,"Callcount","avrage",avg,type(avg),"mode",mode)
   
        user = User.objects.get(id=user_id)
        print(user.status,user.calls,user.avgTT,Callcount,user)
        if status is not None:
            user.status = status
            user.event=dt
        if avg is not None:
            user.avgTT = avg
            user.event=dt

        if status == "Idle" :
            print("in iffffffffffffffffffffffffffffffffffffffffffff IDLE")
            user.mode=" "
        elif mode is not None and status != "Idle":
            print("in elifffffffffffffffffffffffffffffffffffffffff NOT IDLE")
            user.mode=mode
        user.save()
        print("user calls",user.calls,"Callcount",user.status,status)
        return JsonResponse({'success': True})
  


