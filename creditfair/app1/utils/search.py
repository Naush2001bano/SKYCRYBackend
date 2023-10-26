from ..views_imports import *


@api_view(["POST"])
@validate_bearer_token
def searchajax(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        given_name=json_data.get('name', '')
        # user_level=json_data.get('user_level', '')
        user_level=request.user.user_level
        print(given_name,'give name',user_level,type(user_level))
        try:
            add = AdditionalInfo.objects.values_list('lead_id_id',flat=True).get(phone_no=given_name)
            # print("in addddddddddddddddddddddddddddddddddddddddd",add)
        except:
            add = None
            if add == 0:
                add = None
        # print(add,"Additional")
        try:
            if user_level == 9:
                print('in user 9')
                per=LeadDetails.objects.all()
                print(per,"in elseeeeeeeeee")
            else:
                per=LeadDetails.objects.filter(caller_name=request.user.username)
            
            if given_name != "":
                print('in perrerer',given_name)
                per=per.filter(Q(name__icontains=given_name)|Q(mobile_no__icontains=given_name) | Q(id = add) | Q(additional_no__icontains=given_name) | Q(co_mobile_no__icontains=given_name)|Q(agreement_no__icontains=given_name)|Q(agreement_id__icontains=given_name)|Q(list_id__icontains=given_name))
                print(per,'perererer')
            
            per=per[:500]

            sc_serializer = FilterSerializers(per,many=True)
            print(sc_serializer.data,'data')
            
            return JsonResponse({"status":200,'all_data':sc_serializer.data})
        except Exception as e:
            print(e)
            return JsonResponse({'status':300})
    
    return JsonResponse({'status':400})
