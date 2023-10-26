from .models import *
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse,JsonResponse,FileResponse
from datetime import datetime,timedelta
import xlwt
import json
from rest_framework.decorators import api_view
from .views_imports import validate_bearer_token
import io



def export_reminder(request):
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

    if request.method == "POST":
        fd = request.POST.get('fdate').rstrip()
        td = request.POST.get('todate').rstrip()
        fil = request.POST.get('filterval').split(",")
        sortval = request.POST.get('sortby')
        fd = datetime.strptime(fd,'%d-%m-%Y')
        td = datetime.strptime(td,'%d-%m-%Y')
        if fd == td:
            data = data.filter(callback_datetime__icontains=fd)
        else:
            data = data.filter(callback_datetime__range=[fd,td])
      
        if sortval == "ascending":
            data = data.order_by('amount')
        elif sortval == "descending":
            data = data.order_by('-amount')  


        if fil != ['']:
            data = data.filter(Q(sub_disposition__in=fil))

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data')

        row_num = 0

        columns = ["Name","Agreement No.","Amount","Disposition","Date&Time","Caller ID"]
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num]) 
        
        rows = data.values_list("name","agreement_no","main_amount","sub_disposition","callback_datetime","caller_name")

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                
                data=str(row[col_num]).replace("nan"," ")
                data=data.replace("None"," " )
                if col_num == 4:
                    data = str(row[col_num])[:19]
                ws.write(row_num, col_num,data)
        wb.save(response)

        print(response)
        return response
        
        
    return JsonResponse({'status':200})



def export_recovery(request):
    direction_val = request.user.process
    user_directions = []
    if direction_val:
        user_directions=User.objects.filter(process=direction_val).values_list('username',flat=True)

    data=LeadDetails.objects.exclude(Q(sub_disposition='Schedule Call')|Q(sub_disposition='Promise To Pay')|Q(sub_disposition='Call Back')|Q(sub_disposition='OTS Request')).exclude(attempted=0)

    if request.user.user_level == 9:
        if  direction_val:
            data = data.filter(caller_name__in=user_directions)
    else:
        data = data.filter(Q(caller_name=request.user.username)|Q(attempted_by=request.user.username))

    if request.method == "POST":
        fd = request.POST.get('fdate').rstrip()
        td = request.POST.get('tdate').rstrip()
        sel = request.POST.getlist('remcb')
        fd = datetime.strptime(fd,'%d-%m-%Y').date()
        td = datetime.strptime(td,'%d-%m-%Y').date()
        if fd == td:
            data = data.filter(contacted_dt__icontains=fd)
        else:
            data = data.filter(contacted_dt__range=[fd,td])
        
        if sel:
            data = data.filter(sub_disposition__in=sel)


        data = data.exclude(list_forkey__status__contains="0").order_by("-contacted_dt")
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data')

        row_num = 0

        columns = ["Name","Agreement No.","Amount","Contacted DateTime","Sub Disposition","Caller ID"]
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num]) 
        
        rows = data.values_list("name","agreement_no","main_amount","contacted_dt","sub_disposition","caller_name")

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                
                data=str(row[col_num]).replace("nan"," ")
                data=data.replace("None"," " )
                if col_num == 4:
                    data = str(row[col_num])[:19]
                ws.write(row_num, col_num,data)
        wb.save(response)

        print(response)
        return response
        
    print("all_data",data)
    return JsonResponse({'status':200})



def export_misscall(request):
        
    todaydate = datetime.today().strftime("%Y-%m-%d")   
     #todaydate = "2022-09-19"
   
    if request.method=="POST":
        sd=request.POST.get("fdate").rstrip()
        ed=request.POST.get("todate").rstrip()
        sd=datetime.strptime(sd,'%d-%m-%Y')
        ed=datetime.strptime(ed,'%d-%m-%Y')
    
        sd=sd.strftime("%Y-%m-%d")
        ed=ed.strftime("%Y-%m-%d")
        filt = request.POST.get("filter")

        today=datetime.now().date()
        print(today)
    
        if request.user.user_level == 9:
            miss=Inbound_log.objects.filter(start__contains=today)
        else:
            print("else",request.user.username)
            miss=Inbound_log.objects.filter(start__contains=today)

        if request.user.user_level == 9: 
            miss=Inbound_log.objects.filter(start__range=[sd,ed])
            if sd == ed:
               miss=Inbound_log.objects.filter(start__contains=ed)
        else:
            miss=Inbound_log.objects.filter(start__range=[sd,ed])
            if sd == ed:
               miss=Inbound_log.objects.filter(start__contains=ed)
        
        if filt == "all":
            miss = miss.filter(status__isnull = False)
        elif filt == "completed":
            miss = miss.filter(status = "Yes")
        elif filt == "no":
            miss = miss.filter(status = "No")
        elif filt == "rnr":
            miss = miss.filter(status  = "Ringing No Response")

        # miss = miss[:150]

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data')

        row_num = 0

        columns = ["Contact no.","Misscall Date","Misscall Count","Status"]
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num]) 
        
        rows = miss.values_list("src","start","count","status")

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                print(row[col_num])
                data=str(row[col_num]).replace("nan"," ")
                data=data.replace("None"," ")
                # if col_num == 5:
                #     data = str(row[col_num])[:19]
                ws.write(row_num, col_num,data)
        wb.save(response)
        
        return response

    
    return JsonResponse({"miss":list(miss.values())})


@api_view(["POST"])
@validate_bearer_token
def export_qualityscore(request):
    try:
        module = request.user.module
        user_list = []

        if request.user.user_level == 10:
            user_list = User.objects.filter(module=module).values_list('username', flat=True)
        else:
            user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
        print(user_list, "users callers name")

        data = CallRecording.objects.filter(agentname__in=user_list)
        body = json.loads(request.body)
        print(body,'bodyyyyy')
        fd = body['fdate'] if 'fdate' in body else None
        td = body['tdate'] if 'tdate' in body else None
        process = body['process'] if 'process' in body else None
        agn = body['agn'] if 'agn' in body else None
        dispo = body['dispo'] if 'dispo' in body else None
        phone_no = body['phone_no'] if 'phone_no' in body else None
        
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

        output = io.BytesIO()

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data')

        row_num = 0

        columns = ["Agent Name","Direction","Source",'Destination',"Dispositon","Date & Time","Call Recording"]
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num]) 
        
        rows = data.values_list("agentname","direction","src","dst","sub_dispos","start","recordfile")

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                data=str(row[col_num]).replace("nan"," ")
                data=data.replace("None"," ")
                # if col_num == 5:
                #     data = str(row[col_num])[:19]
                ws.write(row_num, col_num,data)
        wb.save(output)
        output.seek(0)

        response = FileResponse(output, content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        
        return response
    except Exception as e:
        print(e)
        return JsonResponse({"status": 500, "message": "Error generating Excel file"})
    
    return JsonResponse({"miss":list(data.values())})
