from ..views_imports import *

@api_view(['POST'])
@validate_bearer_token
def filterrm(request):
    user_level = request.user.user_level
    direction_val = request.user.process
    user_directions = []
    if direction_val:
        user_directions=User.objects.filter(process=direction_val).values_list('username',flat=True)

    data=LeadDetails.objects.filter(Q(sub_disposition="Promise To Pay")|Q(sub_disposition="Call Back")|Q(sub_disposition="Schedule Call")).exclude(list_forkey__status__contains="0")
    if request.user.user_level == 9:
        if  direction_val:
            data = data.filter(caller_name__in=user_directions)
    else:
        data=data.filter(caller_name=request.user.username)

    try:
        body = json.loads(request.body)

        fd = body['fdate'].rstrip() if 'fdate' in body else ''
        td = body['tdate'].rstrip() if 'tdate' in body else ''
        fil = body['remfilter'].rstrip() if 'remfilter' in body else None
        sortval = body['sortby'] if 'sortby' in body else None
        fd = datetime.strptime(fd,'%d-%m-%Y').date()
        td = datetime.strptime(td,'%d-%m-%Y').date() 
        print(fd==td,fil.split(),sortval,'filterrs')

        print(fd,td,"dddddddddddddd")
        if fd == td:
            data = data.filter(callback_datetime__icontains=fd)
        else:
            # td=td  + timedelta(days=1)
            data = data.filter(callback_datetime__range=[fd,td])


        if sortval == "ascending":
            data = data.order_by('amount')
        elif sortval == "descending":
            data = data.order_by('-amount')  

        all_ct = data.count()
        cbk_ct=data.filter(sub_disposition='Call Back').count()
        ptp_ct = data.filter(sub_disposition='Promise To Pay').count()
        scbk_ct=data.filter(sub_disposition='Schedule Call').count()

        if fil:
            print('in fil')
            data = data.filter(Q(sub_disposition=fil))

        filter_serializers = CallmanagementSerializers(data,many=True)
        # print(filter_serializers.data,'filter_serializers')

        return JsonResponse({'data':filter_serializers.data,"all_ct":all_ct,'ptp_ct':ptp_ct,"cbk_ct":cbk_ct,"scbk_ct":scbk_ct,"user_level":user_level})
    except Exception as e:
        msg = e
        print(msg,'error')
        return JsonResponse({'status':300,'msg':msg})
    return JsonResponse({'status':404})