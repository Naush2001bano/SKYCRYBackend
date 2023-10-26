from ..views_imports import *



@api_view(["POST"])
@validate_bearer_token
def non_attempted_data(request):
    user_level=request.user.user_level
    print('itscalled')
    direction_val = request.user.process
    process_users = []
    if direction_val:
        process_users = User.objects.filter(process=direction_val).values_list('username', flat=True)

    # tk = token_authetication(request)
    u_m = User.objects.filter(id=request.user.assigned_to).last()
    print(u_m,'ummodemdode')
    supervisor_mode = ""
    if request.user.user_level == 1:
        print('ininininin')
        supervisor_mode = u_m.mode
   

    data = LeadDetails.objects.filter(caller_name=request.user.username, attempted=0).exclude(
        list_forkey__status__contains="0", caller_name="")

    if request.user.user_level == 9:
        data = LeadDetails.objects.filter(attempted=0).exclude(list_forkey__status__contains="0", caller_name="")
        if direction_val:
            data = data.filter(caller_name__in=process_users)

    if request.method == "POST":
        data_body =  json.loads(request.body)
        print(data_body)
        agent = data_body['agent'] if 'agent' in data_body else None
        list_id = data_body['list_id']
        print(agent,list_id,"asdasdadasdaojbsdiabs")
        if request.user.user_level == 1:
            agent = request.user.username
        if list_id != "" and list_id != "all":
            try:
                list_id = data.filter(list_id=list_id).last().list_id_id
            except Exception as e:
                print(e)
            data = data.filter(list_id=list_id)
        if agent != "all" and agent != "":
            data = data.filter(caller_name=agent)

        data = data.filter(attempted=0).exclude(list_forkey__status__contains="0").exclude(dnd_detail=1).order_by(
            "-lead_update_date")[:1000]
        data_count = data.count()
        return JsonResponse({"data": list(data.values()), "count": data_count, "mode": supervisor_mode,"user_level":user_level})


@api_view(["POST"])
@validate_bearer_token
def non_attempted(request):
    user_level=request.user.user_level
    u = User.objects.filter(user_level=1).values()  # Convert User QuerySet to a list of dictionaries
    l_id = Dataupload.objects.filter(status=1).values()  # Convert Dataupload QuerySet to a list of dictionaries
    print(user_level,'userlevelele' , l_id)
    supervisor_mode = ""
    
    if request.user.user_level == 1:
        u_m = User.objects.filter(id=request.user.assigned_to).last()
        supervisor_mode = u_m.mode
    
    return JsonResponse({ "u": list(u), "l_id": list(l_id), "user_level":user_level })
