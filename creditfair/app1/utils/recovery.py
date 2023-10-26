from ..views_imports import *


@api_view(["POST","GET","PUT"])
@validate_bearer_token
def filterrs(request):
    direction_val = request.user.process
    user_directions = []
    if direction_val:
        user_directions=User.objects.filter(process=direction_val).values_list('username',flat=True)

    data=LeadDetails.objects.exclude(Q(sub_disposition='Schedule Call')|Q(sub_disposition='Promise To Pay')|Q(sub_disposition='Call Back')|Q(sub_disposition='OTS Request')).exclude(attempted=0)
    print(data,"aaaaaaaaaa")

    if request.user.user_level == 9:
        if  direction_val:
            data = data.filter(caller_name__in=user_directions)
    else:
        data = data.filter(Q(caller_name=request.user.username)|Q(attempted_by=request.user.username)|Q(caller_name__isnull=True)|Q(caller_name = ""))

    
    if request.method == "GET":
        mode = request.user.mode
        process=request.user.process
        dispo=disposition.objects.exclude(sub_dispo__in=["Call Back","Promise To Pay","Schedule Call"])
        if process:
            dispo=dispo.filter(direction=process)
            serialized_data = SubDispositionsSerializers(dispo,many=True)
            # print(serialized_data.data)
        return JsonResponse({'status':200,"dispo":serialized_data.data,"mode":mode})

    if request.method == "PUT":
        try:
            body = json.loads(request.body)
            print('body data',body['fdate'],body['tdate'],body['sortval'],'datacount')
            fd = body['fdate']
            td = body['tdate']
            sel = body['sortval'] if 'sortval' in body else None
            fd = datetime.strptime(fd,'%d-%m-%Y').date()
            td = datetime.strptime(td,'%d-%m-%Y').date() 
            if fd == td:
                print("asdddaddddddddddddd",fd,td)
                data = data.filter(contacted_dt__icontains=fd)
                print(data)
            else:
                data = data.filter(contacted_dt__range=[fd,td])
                print("errrrrrrreeeeeeeeeee",fd,td)
            
            if sel:
                data = data.filter(Q(sub_disposition__in=sel))
                print(data)
            
            cn = data.exclude(list_forkey__status__contains="0").values("sub_disposition").order_by("sub_disposition").annotate(the_count=Count("sub_disposition"))
            print(cn,'count')
            return JsonResponse({'count':list(cn)})

        except Exception as e:
            print(e)
            return JsonResponse({'status':404,'msg':e})
        return JsonResponse({'status':404})


    if request.method == "POST":
        body = json.loads(request.body)
        print('body data',body['fdate'],body['tdate'],body['sortval'],'dtasubmit',data)

        fd = body['fdate']
        td = body['tdate']
        sel = body['sortval'] if 'sortval' in body else None
        fd = datetime.strptime(fd,'%d-%m-%Y').date()
        td = datetime.strptime(td,'%d-%m-%Y').date()  + timedelta(days=1)
        if fd == td:
            print("asdddaddddddddddddd",fd,td)
            data = data.filter(contacted_dt__icontains=fd)
        else:
            print("errrrrrrreeeeeeeeeee",fd,td)
            data = data.filter(contacted_dt__range=[fd,td])
        
        if sel:
            data = data.filter(Q(sub_disposition__in=sel))
        print(data,"lastttttttttttt")
        
        # data = data.exclude(list_forkey__status__contains="0").order_by("-contacted_dt")[:1000]
        filter_serializer = CallmanagementSerializers(data,many=True)
        return JsonResponse({'data':filter_serializer.data})