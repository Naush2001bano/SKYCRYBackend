from ..views_imports import *

@api_view(["GET"])
@validate_bearer_token
def notificationCount(request):
    direction_val = request.user.process
    user_directions = []
    if direction_val:
        user_directions=User.objects.filter(process=direction_val).values_list('username',flat=True)
    else:
        user_directions=User.objects.filter(user_level=1).values_list('username',flat=True)
    today = datetime.today()
    try:
        d4 = today.strftime("%Y-%m-%d")
        if request.user.user_level == 9:
            d=LeadDetails.objects.filter(callback_datetime__contains=d4,caller_name__in=user_directions).exclude(list_forkey__status__contains="0").aggregate(total=Sum(Case(When( (Q(sub_disposition='Call Back')|Q(sub_disposition="Schedule Call")|Q(sub_disposition="Promise To Pay")),then=1),default=0
            )))
        else:
            d=LeadDetails.objects.filter(callback_datetime__contains=d4).exclude(list_forkey__status__contains="0").filter(caller_name=request.user.username).aggregate(total=Sum(Case(When( (Q(sub_disposition='Call Back')|Q(sub_disposition="Schedule Call")|Q(sub_disposition="Promise To Pay")),then=1),default=0
            )))
        print(d)
            
        value=d["total"]
        print("reminder",value)
    except Exception as e:
        print(e)
  
    return JsonResponse({'value':value})

@api_view(["GET"])
@validate_bearer_token
def misscallednotiCount(request):
    today = datetime.today()
    d4 = today.strftime("%Y-%m-%d")
    # d4="2022-09-22"
    if request.user.user_level == 9:
        d=Inbound_log.objects.filter(start__contains=d4,status="No").count()
        print("missssssssssssssssssssssssssssssssssssssssssssssss",d)
    else:
       
        d=Inbound_log.objects.filter(start__contains=d4,status="No").count()
        print(d)
        
    return JsonResponse({'d':d})