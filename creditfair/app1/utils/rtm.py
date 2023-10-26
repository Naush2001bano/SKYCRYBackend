from ..views_imports import *

@api_view(["GET"])
@validate_bearer_token
def rtm_table(request):
    if request.user.user_level==10:
        users = User.objects.filter(user_level=1,is_loggedin=1,module=request.user.module).order_by("-avgTT", "-status")  # Sort users by avgTT, status, and on-call in descending 
    else:
        users = User.objects.filter(user_level=1,is_loggedin=1,assigned_to=request.user.id).order_by("-avgTT", "-status")  # Sort users by avgTT, status, and on-call in descending order
    
    current_dt=datetime.now()
    print(users,"RTM data",current_dt)
    return JsonResponse({"data":list(users.values()),"current_dt":current_dt}, safe=False)


@api_view(["GET"])
@validate_bearer_token
def queue_screen(request):
    a = QueueLog.objects.all()
    ser = QueueLogSerializers(a,many=True)
    current_dt=datetime.now()
    return JsonResponse({"Status":200,"data":ser.data,"current_dt":current_dt})
