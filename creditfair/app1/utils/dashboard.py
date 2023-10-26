from ..views_imports import *
from collections import defaultdict


@api_view(["POST"])
@validate_bearer_token
def total_calls(request):
    user_list = []
    uploaded_by_ls=[]
    if request.user.user_level==9:
        user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
    elif request.user.user_level==10:
        user_list=User.objects.filter(module=request.user.module,user_level=1).values_list('username', flat=True)
        uploaded_by_ls=User.objects.filter(module=request.user.module,user_level=9).values_list('username', flat=True)
    else:
        user_list=User.objects.filter(id=request.user.assigned_to).values_list('username', flat=True)
    print(user_list,'userlist','userrrrrrrrrrrrrrrrrrrrr')
    upload=0
    available=0
    contacted=0
    noncontacted=0
    direction_val = request.user.process
    assign_id = request.user.assigned_to
    print(direction_val,'direction')
    try :
        body =  json.loads(request.body)
        t=body['time']
        print(t,"timeeeeeeeeeeeeeeeeeeee")
        today=datetime.now().date()
        todate=today+timedelta(days=1)
        days_to_monday = (today.weekday()) % 7  # Number of days to previous Monday
        monday_date = today - timedelta(days=days_to_monday)
        monday_to_sunday=monday_date+timedelta(days=6)
        month = datetime.now().month
        year = datetime.now().year
        current_year_month = f"{year}-{month:02}"
        module=request.user.module
        data=Dataupload.objects
        lead_data=LeadDetails.objects.exclude(list_forkey__status__contains="0")
        c_nc_data=LeadDetails.objects.exclude(list_forkey__status__contains="0")
        # print(current_year_month,"total")
        if request.user.user_level == 10:
            lead_data=lead_data.filter(caller_name__in=user_list)
            c_nc_data=c_nc_data.filter(caller_name__in=user_list)
            # print(request.user.module,"on switch change")
            data=data.filter(uploaded_by__in = uploaded_by_ls)
            # print(data,"after changed")
        # print(current_year_month,"total")
        elif request.user.user_level == 9:
            lead_data=lead_data.filter(caller_name__in=user_list)
            c_nc_data=c_nc_data.filter(caller_name__in=user_list)
            data=data.filter(uploaded_by=request.user.username,status=1)
            # print("userlevel 9","data",lead_data,"lead_data",c_nc_data,"cdatatata","///////",data)
        else:
            lead_data=LeadDetails.objects.filter(caller_name=request.user.username).exclude(list_forkey__status__contains="0")
            c_nc_data=LeadDetails.objects.filter(caller_name=request.user.username).exclude(list_forkey__status__contains="0")        
            data=data.filter(uploaded_by__in=user_list)
        
        if t == "today":
            # print(data," in today filter")
            data=data.filter(entry__icontains=today)
            lead_data=lead_data.filter(list_forkey__entry__icontains=today,attempted=0)
            c_nc_data=c_nc_data.filter(contacted_dt__icontains=today)
            # print(c_nc_data,"itssssssssssssssssss today",data)
        elif t == "week" :
            # print(monday_date,today,"in weeek")
            data=data.filter(entry__range=[monday_date,todate])
            # print(data,"uploadddddd")
            lead_data=lead_data.filter(list_forkey__entry__range=[monday_date,monday_to_sunday],attempted=0)
            # print(lead_data,"leadddddddddddddddddddddddddddd")
            c_nc_data=c_nc_data.filter(contacted_dt__range=[monday_date,monday_to_sunday])
            # print(c_nc_data,"contacteddddddddddddddddd")
        elif t== "month":
            data=data.filter(entry__icontains=current_year_month)
            lead_data=lead_data.filter(list_forkey__entry__icontains=current_year_month,attempted=0)
            c_nc_data=c_nc_data.filter(contacted_dt__icontains=current_year_month)
            # Total calls upload data starts

        data = data.exclude(status__contains="0")
        if len(data) != 0 :
            upload=data.aggregate(Sum('count'))
            upload=upload["count__sum"]
        else:
            upload = 0
        # print(upload,data,"after sum")


        #Total calls Available starts
        available=lead_data.count()
        #Total calls Avaialable ends
        
        #Total calls Contacted starts
  
        contacted=c_nc_data.filter(disposition="Contacted").count()
        #Total calls Contacted ends

        #Total calls Non-Contacted starts
        noncontacted=c_nc_data.filter(disposition="Non-Contacted").count()
        #Total calls Non-Contacted ends
    except Exception as e : 
        print(e)
    
    print(upload,available,contacted,noncontacted,"endsssssss")
    return JsonResponse({"status":200,"upload":upload,"available":available,"contacted":contacted,"noncontacted":noncontacted})





@api_view(["POST"])
@validate_bearer_token
def agent_available(request):
    user_list = []
    if request.user.user_level==9:
        user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
    elif request.user.user_level==10:
        user_list=User.objects.filter(module=request.user.module,user_level=1).values_list('username', flat=True)
    else:
        user_list=User.objects.filter(username=request.user.username).values_list('username', flat=True)
    try :
        # direction_val = request.user.process
        body =  json.loads(request.body)
        module=request.user.module
        assign_id = request.user.assigned_to
        today=datetime.now().date()
        todate=today+timedelta(days=1)
        d=body['time']
        month = datetime.now().month
        year = datetime.now().year
        current_year_month = f"{year}-{month:02}"
        days_to_monday = (today.weekday()) % 7  # Number of days to previous Monday
        monday_date = today - timedelta(days=days_to_monday)
        monday_to_sunday=monday_date+timedelta(days=6)
        data=User.objects.filter(module=module,user_level=1)
        if d=="today":
            data=User.objects.filter(user_level=1,date_joined__icontains=today)
        elif d == "week":
            data=User.objects.filter(user_level=1,date_joined__range=[monday_date,monday_to_sunday])
        elif d == "month":
            data=User.objects.filter(user_level=1,date_joined__icontains=current_year_month)
        
        total_agent=User.objects.filter(user_level=1,module=module,username__in=user_list)
        logged_in_agent=User.objects.filter(user_level=1,is_loggedin=1,module=module,username__in=user_list)
        on_call=User.objects.filter(user_level=1,is_loggedin=1,status="On Call",module=module,username__in=user_list)
        on_paused=User.objects.filter(user_level=1,is_loggedin=1,module=module,username__in=user_list).exclude(status__in=["Not Ready","Idle","On Call","Hangup","Wrap-up"])
        
        total_agent=total_agent.count()   
        logged_in_agent=logged_in_agent.count()
        on_call = on_call.count()
        on_paused = on_paused.count()
        print(total_agent,logged_in_agent,on_call,on_paused,"agent info")
    except Exception as e :
        print(e)
  
    return JsonResponse({"status":200,"total_agent":total_agent,"logged_in_agent":logged_in_agent,"on_call":on_call,"on_paused":on_paused})

@api_view(["POST"])
@validate_bearer_token
def top_five_dispo(request):
    user_list = []
    if request.user.user_level==9:
        user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
    elif request.user.user_level==10:
        user_list=User.objects.filter(module=request.user.module,user_level=1).values_list('username', flat=True)
    else:
        user_list=User.objects.filter(username=request.user.username).values_list('username', flat=True)
    
    try :
        direction_val = request.user.process
        assign_id = request.user.assigned_to
        today=datetime.now().date()
        todate=today+timedelta(days=1)
        body = json.loads(request.body)
        time=body['time']
        month = datetime.now().month
        year = datetime.now().year
        current_year_month = f"{year}-{month:02}"
        top5 = LogData.objects
        days_to_monday = (today.weekday()) % 7  # Number of days to previous Monday
        monday_date = today - timedelta(days=days_to_monday)
        monday_to_sunday=monday_date+timedelta(days=6)

        ls=[]
        top5=top5.filter(caller_name__in=user_list)
        # print(today,"weddddddddddddddddddddddddddddd",monday_date)
        # if request.user.user_level == 9:
        #     top5=top5
        #     if direction_val:
        #         top5=top5.filter(direction=direction_val)
        # else:
        #     top5=top5.filter(caller_name=request.user.username)
            
        if time == "today":
            top5 = top5.filter(contacted_dt__icontains=today)
            ct=top5.count()
            print(top5,"in today'ssss filter",ct)
            # data=LeadDetails.objects.filter(contacted_dt__icontains=today)
        elif time == "week":
            top5 = top5.filter(contacted_dt__range=[monday_date,monday_to_sunday])
    
        elif time=="month":
            top5=top5.filter(contacted_dt__icontains=current_year_month)
            
        todays_call=top5.count()
        top5 = top5.values('sub_disposition').annotate(count=Count('*')).order_by('-count')[:5]

        # print(todays_call,"todays call",type(todays_call),top5)
        # print('top 5',type(top5),top5[0]["sub_disposition"],top5)
        
        if len(top5) != 0:
            for i in range(len(top5)):
                d={}
                # print("top5[i]['count']",top5[i]["count"],type(top5[i]["count"]))
                if top5[i]["count"] == 0:
                    calc=0
                else:
                    calc=(top5[i]["count"]/todays_call)*100
                
                # print(calc,"just calculated")
                d["Sub_disposition"]=top5[i]["sub_disposition"]

                d["percent"]=str(calc)+"%"
                
                ls.append(d)
        else:
            top5=0

        print(ls,"ls",todays_call)
    except Exception as e :
        print(e)
    return JsonResponse({"status":200,"ls":ls,"todays":todays_call})


@api_view(["POST"])
@validate_bearer_token
def paid_ptp_status(request):
   
    if request.user.user_level==9:
        user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
    elif request.user.user_level==10:
        user_list=User.objects.filter(module=request.user.module,user_level=1).values_list('username', flat=True)
    else:
        user_list=User.objects.filter(username=request.user.username).values_list('username', flat=True)

    paid_data=LogData.objects.filter(caller_name__in=user_list)
    ptp_data=LogData.objects.filter(caller_name__in=user_list)
    body = json.loads(request.body)
    d=body['time']
    # print(d,"dddddddddddddddddddddddddddddddddddddddddd")
    today=datetime.now().date()
    todate=today+timedelta(days=1)
    month = datetime.now().month
    year = datetime.now().year
    current_year_month = f"{year}-{month:02}"
    days_to_monday = (today.weekday()) % 7  # Number of days to previous Monday
    monday_date = today - timedelta(days=days_to_monday)
    monday_to_sunday=monday_date+timedelta(days=6)
    print(monday_date,monday_to_sunday)
    if d=="today":
        paid_data=paid_data.filter(contacted_dt__icontains=today)
        ptp_data=ptp_data.filter(callback_datetime__icontains=today)
    elif d=="week":
        paid_data=paid_data.filter(contacted_dt__range=[monday_date,monday_to_sunday])
        ptp_data=ptp_data.filter(callback_datetime__range=[monday_date,monday_to_sunday])
    elif d=="month":
        paid_data=paid_data.filter(contacted_dt__icontains=current_year_month)
        ptp_data=ptp_data.filter(callback_datetime__icontains=current_year_month)

        
    paid=paid_data.filter(sub_disposition="Paid").count()
    ptp=ptp_data.filter(sub_disposition="Promise To Pay").count()
    print(paid,ptp)

    return JsonResponse({"status":200,"paid":paid,"ptp":ptp})
