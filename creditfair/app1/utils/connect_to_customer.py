from ..views_imports import *
import subprocess
import os

@api_view(["POST"])
@validate_bearer_token
def filter_sub_dispo_attmpts(request):
  dt=datetime.today().date()
  if request.method == "POST" : 
    dates = json.loads(request.body)
    username=request.user.username
    print(dates,"data from json")

    data_ct =LeadDetails.objects.filter(list_forkey_id__entry__range = [dates['fd'],dates['td']],list_forkey_id__status = '1',list_forkey__uploaded_by = username,Unassigned = '1').count()
  
    lead_data = LeadDetails.objects.filter(list_forkey_id__entry__range = [dates['fd'],dates['td']],list_forkey_id__status = '1',list_forkey__uploaded_by = username,Unassigned='1',sub_disposition__isnull = False)

    subdispo_counts = lead_data.values('sub_disposition').annotate(count=Count('sub_disposition'))
    sb = [ i for i in subdispo_counts ]
    print(sb,"get sub",data_ct)
  return JsonResponse({"sb" : sb , "data_ct" : data_ct})



def filter_records(username,filterValue):
  data = LeadDetails.objects
  data=data.filter(list_forkey_id__entry__range = [filterValue['fdate'],filterValue['tdate']],list_forkey_id__status = '1',list_forkey__uploaded_by = username,Unassigned = '1')
  if len(filterValue['subdispo']) > 0 :
      data=data.filter(sub_disposition__in=filterValue['subdispo'])
      print("in subdispo",data.count())
  if len(filterValue['operators']) > 0 and len(filterValue['attempts']) > 0:
            if filterValue['operators'] == '=':
                data=data.filter(attempted = filterValue['attempts'])
            if filterValue['operators'] == '>=':
                data=data.filter(attempted__gte = filterValue['attempts'])
            if filterValue['operators'] == '<=':
                data=data.filter(attempted__lte = filterValue['attempts'])

  return data

@api_view(["POST"])
@validate_bearer_token
def IVRDatacount(request):
  username = request.user.username
  if request.method == "POST" : 
    filterValue = json.loads(request.body)
    print(filterValue , "data from json")
    data = filter_records(username,filterValue)
    print(len(data),'length data')
    count=len(data)
  return JsonResponse({"data_count":count})


@api_view(["POST"])
@validate_bearer_token
def get_data(request):
  username = request.user.username
  if request.method == "POST" : 
    IVRLeads.objects.all().delete()
    filterValue = json.loads(request.body)
    print(filterValue , "data from json")
    data = filter_records(username,filterValue)
    print(len(data),'length dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    for i in range(len(data)):
      IVRLeads.objects.create(phone_no=data[i].mobile_no,lead_forkey_id=data[i].id,ivr_no=filterValue['ivr_no'])
       
  return JsonResponse({"data":list(data.values())})

def fetch_Ivrdata(request):
   data=IVRLeads.objects.all()
   ser=IVRSerializer(data,many=True)
   return JsonResponse({"data" : ser.data})
   
   
# def start_file_execution(request):
#     global process
#     if not process:
#         # Start the Python file execution using subprocess
#         process = subprocess.Popen(['python3', 'C:/Users/Nausheen.sayyed/Desktop/predictive/predictive.py'])
#         return JsonResponse({'status': 'started'})
#     else:
#         return JsonResponse({'status': 'already_running'})
    
# def stop_file_execution(request):
#     global process
#     print(process,"processsssssssssss")
#     if process:
#         # Terminate the Python file execution process
#         process.terminate()
#         process = None
#         return JsonResponse({'status': 'stopped'})
#     else:
#         return JsonResponse({'status': 'not_running'})


process2 = None

def start_file_IVRexecution(request):
    global process2
    if not process2:
        # Start the Python file execution using subprocess
        command=['python3' ,'C:/Users/Nimesh.vishwakarma/Desktop/projects/frontendbackend/backendandfrontend/IVR/Ivr.py']
        process2 = subprocess.Popen(command)
        # process2 = os.getpgid(process2.pid)
        return JsonResponse({'status': 'started'})
    else:
        return JsonResponse({'status': 'already_running'})
    
def stop_file_IVRexecution(request):
    global process2
    if process2:
        print(process2,"sjdshfhdkjfhfjhf")
        try:
            # os.kill(process, signal.SIGTERM)  
            process2.terminate()
            # os.killpg(os.getpgid(process2), signal.SIGTERM)
            process2 = None
            return JsonResponse({'status': 'stopped'}) 
        except Exception as e:
            print("error",e)
            return JsonResponse({'status': 'permission_error'})
    else:
        return JsonResponse({'status': 'not_running'})
