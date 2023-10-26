from ..views_imports import *


@api_view(["POST"])
@validate_bearer_token
def ptpajax(request):
    module = request.user.module
    user_list = []
    if request.user.user_level==9:
        user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
    elif request.user.user_level==10:
        user_list=User.objects.filter(module=request.user.module,user_level=1).values_list('username', flat=True)
    else:
        user_list=User.objects.filter(username=request.user.username).values_list('username', flat=True)
    print(user_list,'user_listttttt')
    if request.method=="POST":
        body=json.loads(request.body)
        agent=body["ptpagent"] if "ptpagent" in body else None
        bk=body['bankname'] if 'bankname' in body else None
        
        print("detaiiiiiils",agent,"bankkkkkkkkk",bk)

        data = ptpbehaviour.objects.filter(callerid__in=user_list).exclude(next_status="Paid")
        print("dataaa1",data)

        if agent !="" and agent !="all":
            data = data.filter(callerid__in=user_list)
            print("aagenttt")
        
        elif agent =="all":
             data =  ptpbehaviour.objects.exclude(next_status="Paid")
            
        if bk !="" and bk!="all":
            data = data.filter(lender_name=bk).exclude(next_status="Paid")
            print("dataaabk",data)
        
        elif bk =="all" :
             data = data.filter(lender_name__isnull=False)
            
        print(len(data))
        data=data.order_by("-id")[:500]
        return JsonResponse({"b":list(data.values()),"status":200})
    return JsonResponse({'status':300})

    
@api_view(["GET"])
@validate_bearer_token
def ptp_status(request):  
    print("Updated Code")
    agents = User.objects
    agent_data = {}

    today = datetime.now().date()
    days_to_monday = (today.weekday()) % 7
    monday_date = today - timedelta(days=days_to_monday)
    monday_to_sunday=monday_date+timedelta(days=6)
    month = datetime.now().month
    year = datetime.now().year
    current_year_month = f"{year}-{month:02}"
    print(monday_date,monday_to_sunday,"Promise To pay")
    if request.user.user_level == 1:
        agents = agents.filter(username=request.user.username)
    elif request.user.user_level == 9:
        user_ls = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
        agents = agents.filter(username__in=user_ls)
    elif request.user.user_level==10:
        user_ls=User.objects.filter(user_level=1,module=request.user.module).values_list('username', flat=True)
        agents = agents.filter(username__in=user_ls)
    for agent in agents:
        ptp_data = LogData.objects.filter(caller_name=agent.username, sub_disposition="Promise To Pay")

        stats = {
                'td': ptp_data.filter(callback_datetime__icontains=today).count(),
                'tw': ptp_data.filter(callback_datetime__range=[monday_date, monday_to_sunday]).count(),
                'tm': ptp_data.filter(callback_datetime__icontains= current_year_month).count(),
                'tos': ptp_data.filter(callback_datetime__icontains=current_year_month).aggregate(Sum('main_amount'))['main_amount__sum'],
                'ptp': ptp_data.filter(callback_datetime__icontains=current_year_month).aggregate(Sum('amount'))['amount__sum'] or 0,
        }

        try:
            if stats['ptp'] != 0:
                stats['per'] = round((stats['ptp'] / stats['tos']) * 100, 2)
            else:
                stats['per'] = 0
        except ZeroDivisionError:
            stats['per'] = 0

        agent_data[agent.username] = stats
    print(agent_data,"all")
    return JsonResponse({"d":agent_data})


@api_view(["GET"])
@validate_bearer_token
def paid_status(request):
    agents = User.objects.all()
    agent_data = {}

    today = datetime.now().date()
    days_to_monday = (today.weekday()) % 7
    monday_date = today - timedelta(days=days_to_monday)
    monday_to_sunday=monday_date+timedelta(days=6)
    month = datetime.now().month
    year = datetime.now().year
    current_year_month = f"{year}-{month:02}"

    if request.user.user_level == 1:
        agents = agents.filter(username=request.user.username)
    elif request.user.user_level == 9:
        user_ls = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
        agents = agents.filter(username__in=user_ls)
    elif request.user.user_level==10:
        user_ls=User.objects.filter(user_level=1,module=request.user.module).values_list('username', flat=True)
        agents = agents.filter(username__in=user_ls)   

    for agent in agents:
        paid_data = LogData.objects.filter(caller_name=agent.username, sub_disposition="Paid")
        
        us = paid_data.filter(contacted_dt__icontains=today).count()
        tw = paid_data.filter(contacted_dt__range=[monday_date, monday_to_sunday]).count()
        tm = paid_data.filter(contacted_dt__icontains=current_year_month).count()
        
        main = paid_data.filter(contacted_dt__icontains=current_year_month).aggregate(Sum('main_amount'))
        t = main['main_amount__sum']
        
        paid = paid_data.filter(contacted_dt__icontains=current_year_month).aggregate(Sum('amount'))
        p = paid['amount__sum']
        
        try:
            if p is not None:
                p = round(p)
                percent = round((p / t) * 100, 2)
            else:
                percent = 0
        except Exception as e:
            print(e)
            percent = 0
        
        agent_data[agent.username] = {
            'td': us,
            'tw': tw,
            'tm': tm,
            'tos': t,
            'ptp': p or 0,
            'paidontos': percent,
        }

    return JsonResponse({"d": agent_data})


@api_view(["GET"])
@validate_bearer_token
def tvajax(request):
    month = datetime.now().month
    year = datetime.now().year
    current_year_month = f"{year}-{month:02}"

    user_list = []
    if request.user.user_level==9:
        user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
    elif request.user.user_level==10:
        user_list=User.objects.filter(module=request.user.module,user_level=1).values_list('username', flat=True)
    else:
        user_list=User.objects.filter(username=request.user.username).values_list('username', flat=True)
    print(user_list)
    l_d=LogData.objects.filter(caller_name__in=user_list)
    result=l_d.filter(caller_name__in=user_list,contacted_dt__icontains=current_year_month)
    result = result.values('agreement_no','sub_disposition').annotate(Count("agreement_no"),Count('sub_disposition')).order_by("-sub_disposition")
    data = list(result.values("sub_disposition","sub_disposition__count"))
    con =  l_d.all().values_list('sub_disposition', flat=True).distinct().order_by('sub_disposition')

    main_list = {}

    for i in con:
        main_list[i] = {"a1":0,"a2":0,"a3":0,"a4":0,"a5":0,"a6":0,"a7":0,"a8":0,"a9":0,"a10":0}

    for i in result:
        if i["sub_disposition"] in main_list:
            if i["sub_disposition__count"] == 1:        
                main_list[i["sub_disposition"]]["a1"] += 1
            elif i["sub_disposition__count"] == 2:
                main_list[i["sub_disposition"]]["a2"] += 1
            elif i["sub_disposition__count"] == 3:
                main_list[i["sub_disposition"]]["a3"] += 1
            elif i["sub_disposition__count"] == 4:
                main_list[i["sub_disposition"]]["a4"] += 1
            elif i["sub_disposition__count"] == 5:
                main_list[i["sub_disposition"]]["a5"] += 1
            elif i["sub_disposition__count"] == 6:
                main_list[i["sub_disposition"]]["a6"] += 1
            elif i["sub_disposition__count"] == 7:
                main_list[i["sub_disposition"]]["a7"] += 1
            elif i["sub_disposition__count"] == 8:
                main_list[i["sub_disposition"]]["a8"] += 1
            elif i["sub_disposition__count"] == 9:
                main_list[i["sub_disposition"]]["a9"] += 1
            elif i["sub_disposition__count"] >= 10:
                main_list[i["sub_disposition"]]["a10"] += 1

    data = json.dumps(main_list)
    return JsonResponse({"stat":data})

