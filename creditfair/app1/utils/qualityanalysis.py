from ..views_imports import *

@api_view(['GET'])
@validate_bearer_token
def dropdowndata_quality(request):
    subdispo = disposition.objects.all()
    serialized_subdispo = SubDispositionsSerializers(subdispo,many=True).data
    users_data = User.objects.filter(assigned_to = request.user.id,user_level = '1')
    serialized_user = UsernameSerializer(users_data,many=True).data
    return JsonResponse({'status':200,'subdispo':serialized_subdispo,'username':serialized_user})


@api_view(['POST'])
@validate_bearer_token
def qsdata(request):
    module = request.user.module
    user_list = []

    if request.user.user_level == 10:
        user_list = User.objects.filter(module=module).values_list('username', flat=True)
    else:
        user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
    print(user_list, "users callers name")

    data = CallRecording.objects.filter(Q(agentname__in=user_list)|Q(agentname='')|Q(agentname__isnull=True))
    print(data,"callrecord")
    if request.method == "POST":
        body = json.loads(request.body)
        print(body,'bodyyyyy')
        fd = body['fdate'] if 'fdate' in body else None
        td = body['tdate'] if 'tdate' in body else None
        process = body['process'] if 'process' in body else None
        agn = body['agn'] if 'agn' in body else None
        dispo = body['dispo'] if 'dispo' in body else None
        phone_no = body['phone_no'] if 'phone_no' in body else None
        # print(data,"exraaaa")
        # if fd and td:
        #     fd_date = parse_date(fd)
        #     td_date = parse_date(td)
        #     if fd_date and td_date:
        #         td_date += timedelta(days=1)
        #         data = data.filter(start__range=[fd_date, td_date])

        fdate = datetime.strptime(fd,'%d-%m-%Y')
        tdate = datetime.strptime(td,'%d-%m-%Y')

        tdate = tdate + timedelta(days=1)
        print(fdate,tdate,"its date after conversion")
        if fdate == tdate:
            data=data.filter(start__icontains = fdate)
        else:
            data=data.filter(start__range=[fdate,tdate])
        if agn and agn != 'all':
            data = data.filter(agentname=agn)

        if dispo and dispo != 'all':
            data = data.filter(sub_dispos=dispo)

        if phone_no:
            data = data.filter(Q(src__icontains=phone_no) | Q(dst__icontains=phone_no))

        data = data.order_by("-id")[:1000]
        print(data,"queues data")
        serializer = CallrecordingSerializers(data, many=True)
        serializer_data = serializer.data
        
    return JsonResponse({"status": 200, "data": serializer_data})

    