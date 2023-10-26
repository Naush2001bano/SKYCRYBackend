from ..models import *
from datetime import datetime,timedelta
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum,Case,When,F,QuerySet,Q
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
import requests

main_url="127.0.0.1:8001"

@csrf_exempt
def update_status(request):
    print('its post not')
    if request.method == "POST":
        print("in post")
        extension = request.POST.get("extension")
        status = request.POST.get("status")
        # message = request.POST.get("message")
        callid = request.POST.get("callid")
        channelid = request.POST.get('channelid')
        request_id = request.POST.get("request_id")
        print(channelid,"dasdadadadadsssss")
        # AgentCall.objects.filter(extension=extension).update(status=status)
        print("from update status function",extension,status,callid,channelid)
        if request_id :
            AgentCall.objects.filter(request_id=request_id).update(callid=callid,channel=channelid)
        else:
            AgentCall.objects.filter(extension=extension).update(status=status)        
    return JsonResponse({'status':200})

@csrf_exempt
def create_cdr(request):
    print("in create cdr")
    if request.method=="POST":
        callid=request.POST.get('callid')
        src=request.POST.get("src")
        srctech=request.POST.get("srctech")
        dst=request.POST.get("dst")
        dsttech=request.POST.get("dsttech")
        start=request.POST.get("start")
        end=request.POST.get("end")
        billsec=request.POST.get("billsec")
        disposition=request.POST.get("disposition")
        direction=request.POST.get("direction")
        dtmf=request.POST.get("dtmf")
        print(dtmf,"dtmfffffffffffffffffffffffffffffffffffff")
        recordfile=request.POST.get("recordfile").replace("netdesk","10.128.11.67/Recording")
        CallRecording.objects.create(callid=callid,src=src,srctech=srctech,dst=dst,dsttech=dsttech,start=start,end=end,billsec=billsec,disposition=disposition,direction=direction,recordfile=recordfile,dtmf=dtmf)
        if direction == "Inbound":
            Incoming_info.objects.filter(caller__icontains=src).delete()
            QueueLog.objects.filter(caller__icontains=src).delete()

        check_log=IVR_LogData.objects.filter(callid=callid)
        if check_log  : 
            check_log.update(call_status=disposition,dtmf=dtmf,dsttech=dsttech,dst=dst)
        # elif check_log :
        #     check_log.update(call_status=disposition,dtmf=dtmf,dsttech=dsttech,dst=dst)    

    return JsonResponse({'status':200})

@csrf_exempt
def update_calltransfer(request):
    dt=datetime.now()
    if request.method == "POST":
        ext=request.POST.get('ext')
        callid=request.POST.get('callid')
        peer_id=request.POST.get('peer_id')
        channelid=request.POST.get('channelid')
        direction=request.POST.get('direction')
        to=request.POST.get('to')
        res=Calltransfer.objects.filter(extension=ext).last()
        if not res:
            Calltransfer.objects.create(extension=ext,call_id=callid,peer_id=peer_id,channel_id=channelid,direction=direction,to_num=to)
        else:
            Calltransfer.objects.filter(extension=ext).update(call_id=callid,peer_id=peer_id,channel_id=channelid,direction=direction,to_num=to)
    return JsonResponse({'status':200})


@csrf_exempt
def insert_incoming(request):
    if request.method=="POST":
        ext=request.POST.get("ext")
        direction=request.POST.get("direction")
        source=request.POST.get("source")
        destination=request.POST.get("destination")
        callid=request.POST.get("callid")
        called=request.POST.get("called")
        income_date=request.POST.get("income_date")
        status=request.POST.get("status")
        ivrs=request.POST.get("ivrs")
        res=Incoming_info.objects.filter(caller=ext).last()
        if not res:
            res=Incoming_info.objects.create(caller=ext,direction=direction,source=source,destination=destination,callid=callid,called=called,income_date=income_date,status=status)
            QueueLog.objects.filter(caller=ext).delete()
        print("its not Ivrs",ivrs,called,ext)
        ext=ext[-10:]
        lead_forid=IVRLeadStatus.objects.filter(phone_no=ext).last()
        print(lead_forid,"Exsist" , ext)
        check_log=IVR_LogData.objects.filter(callid=callid)
        if ivrs and not check_log:
            IVR_LogData.objects.create(lead_forkey_id=lead_forid.lead_forkey_id,phone_no=lead_forid.phone_no,call_status="Ongoing",ivr_number=lead_forid.ivr_number,dst=destination,callid=callid)
            IVRLeadStatus.objects.filter(id=lead_forid.id).delete()

        elif check_log :
            check_log.update(dst=called )
    return JsonResponse({'status':200})


@csrf_exempt
def insert_queue_incoming(request):
    if request.method=="POST":
        ext=request.POST.get("ext")
        direction=request.POST.get("direction")
        source=request.POST.get("source")
        destination=request.POST.get("destination")
        callid=request.POST.get("callid")
        called=request.POST.get("called")
        status=request.POST.get("status")
        income_date=datetime.now()
        print("Insert queueueueueeueueueueloggggggggggggggggggggggg")
        res=QueueLog.objects.filter(caller=ext).last()
        check_ivrLog=IVR_LogData.objects.filter(callid=callid)
        if not res:
            QueueLog.objects.create(caller=ext,direction=direction,source=source,destination=destination,callid=callid,called=called,income_date=income_date,status=status)
        if check_ivrLog : 
            check_ivrLog.update(call_status ="Queue",dst=called)
            


    return JsonResponse({'status':200})

@csrf_exempt
def delete_incoming(request):
    if request.method == 'POST':
        numbers_str=request.POST.get('numbers_str')
        
        if len(numbers_str) > 3:
            numbers_str=numbers_str.split(',')
        else:
            print(numbers_str,"aljsdkaklsjdaklsjdasjdaslk")
        print('fromm delete',numbers_str,type(numbers_str))
        Incoming_info.objects.exclude(caller__in=numbers_str).delete()
        QueueLog.objects.exclude(caller__in=numbers_str).delete()

    return JsonResponse({'status':200})


@csrf_exempt
def check_misscall(request):
    if request.method == "POST":
        mobile_number=request.POST.get("src")
        callid=request.POST.get("callid")
        srctech=request.POST.get("srctech")
        dst=request.POST.get("dst")
        dsttech=request.POST.get("dsttech")
        start=request.POST.get("start")
        end=request.POST.get("end")
        billsec=request.POST.get("billsec")
        disposition=request.POST.get("disposition")
        direction=request.POST.get("direction")
        recordfile=request.POST.get("recordfile")
        subd = request.POST.get('subd')
        try:
            print(mobile_number,callid,srctech,dst,start,end,billsec,disposition,direction,recordfile,"all parameters")
            # if subd == "ivrs":
            #     IVR_LogData.objects.create()
            d=datetime.now().date()
            check=Inbound_log.objects.filter(src__icontains=mobile_number,start__icontains=d,status="No").last()
            QueueLog.objects.filter(caller__icontains=mobile_number).delete()

            if check:
                Inbound_log.objects.filter(id=check.id).update(count=F("count")+1)
            else:
                print("ready to create")
                Inbound_log.objects.create(src=mobile_number,callid=callid,srctech=srctech,dsttech=dsttech,dst=dst,start=start,end=end,billsec=billsec,disposition=disposition,direction=direction,recordfile=recordfile,status="No",count=1)
            
            try:
                mobile_number = mobile_number[-10:]
                query = LeadDetails.objects.filter(Q(mobile_no__icontains=mobile_number)|Q(last_dial_no=mobile_number)).last()
                obj = LeadDetails.objects.get(id=query.id)
                LogData.objects.create(name=obj.name,mobile_no=obj.mobile_no,address=obj.address,state=obj.state,pincode=obj.pincode,email=obj.email,co_name=obj.co_name,co_mobile_no=obj.co_mobile_no,lender_name=obj.lender_name,merchant_name=obj.merchant_name,agreement_id=obj.agreement_id,agreement_no=obj.agreement_no,nach_status=obj.nach_status,due_date=obj.due_date,advisor=obj.advisor,main_amount=obj.main_amount,first_emi_date=obj.first_emi_date,ref_name1=obj.ref_name1,ref_no1=obj.ref_no1,ref_name2=obj.ref_name2,ref_no2=obj.ref_no2,additional_email=obj.additional_email,additional_address=obj.additional_address,additional_no=obj.additional_no,disposition="Missed Call",sub_disposition=subd,callback_datetime=obj.callback_datetime,remark="User not available",amount=obj.amount,mode_of_payment=obj.mode_of_payment,cheque_transaction_no=obj.cheque_transaction_no,contacted_dt=obj.contacted_dt,attempted = obj.attempted,caller_name="",uploaded_by=obj.uploaded_by,last_dial_no=obj.last_dial_no,list_id=obj.list_id,lead_forkey=obj,dnd_detail=obj.dnd_detail,direction="Inbound",lc_remark=obj.lc_remark,first_name=obj.first_name,AHT=obj.AHT)

            except Exception as e:
                print(e,"error")
                LogData.objects.create(mobile_no=mobile_number,direction="Inbound",disposition="Missed Call",sub_disposition=subd,remark="User not available")

        except Exception as e:
            print(e)

    return JsonResponse({"status":200})


@csrf_exempt
def get_queue_status_response(request):
    if request.method == "POST" : 
        print("POST")
        members = request.POST.get('members')
        queue = request.POST.get('queue')
        members = json.loads(members)
        q=Queues.objects.filter(queue_no=queue).last()
        q_name=q.queue_name
        print(members,queue,"hsiudhiuasyodyeh3dsads")
        if members:
            print("memmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
            for member in members:
                print(member,"tttttttttttttttttttttttttttttttttttttttttttttttt")
                users=User.objects.filter(extension=member['agent'])
                for user in users:
                    obj = QueueDetails.objects.filter(username = user.username)
                    if obj.exists():
                        obj.update(status=member['status'],paused=member['paused'])
                    else:
                        # QueueDetails.objects.create(user_id_id=user.id,extension_status=member['status'],extension_pause_status=member['paused'])
                        q=QueueDetails.objects.create(queue_no=queue,extension=member["agent"],status=member['status'],paused=member['paused'],username=user.username,queue_name=q_name)
                        q.save()
        return JsonResponse({"status":200})
    return JsonResponse({"status":300})

@csrf_exempt
def change_user_extension_status(request):
    if request.method == "POST":
        members = request.POST.get('members')
        queue = request.POST.get('queue')
        members = json.loads(members)

        # print(members,"parammsmsms",type(members),queue)
        if members:
            for member in members:
                print(member)
                users=User.objects.filter(extension=member['agent'])
                print(users)
                for user in users:
                    obj = UserExtendedInfo.objects.filter(user_id = user.id)
                    if obj.exists():
                        obj.update(extension_status=member['status'],extension_pause_status=member['paused'])
                    else:
                        UserExtendedInfo.objects.create(user_id_id=user.id,extension_status=member['status'],extension_pause_status=member['paused'])
    
    current_dt = datetime.now()
    pquery = PredictiveDialedCaseStatus.objects.all()
    for i in pquery:
        differnce = current_dt - i.dial_dt
        print(differnce,"difffernenernnceee")
        if differnce.total_seconds() >= 45:
            if i.call_status != "Answered":
                direction = "Outbound"
                disposition = "Not Answered"
                sub_disposition = "Not Answered"
                remark = ""
                obj = LeadDetails.objects.get(id=i.lead_forkey_id)
                LogData.objects.create(borrowor_name=obj.borrowor_name,mobile_no=obj.mobile_no,address=obj.address,state=obj.state,pincode=obj.pincode,email=obj.email,dob=obj.dob,alt_mno_1=obj.alt_mno_2,alt_mno_3=obj.alt_mno_3,loanamt=obj.loanamt,loan_accountno=obj.loan_accountno,bankname=obj.bankname,trustname=obj.trustname,interest=obj.interest,systemlan=obj.systemlan,bankstate=obj.bankstate,nature_of_facility=obj.nature_of_facility,sanction_amount=obj.sanction_amount,loan_sanction_date=obj.loan_sanction_date,NPA_Date=obj.NPA_Date,interest_rate=obj.interest_rate,account_status=obj.account_status,security_value=obj.security_value,document_custody=obj.document_custody,security_flag=obj.security_flag,current_allocation=obj.current_allocation,current_allocation_date=obj.current_allocation_date,team_leader=obj.team_leader,zone_name=obj.zone_name,branch_name=obj.branch_name,branch_mail_id=obj.branch_mail_id,branch_contact_details=obj.branch_contact_details,toss=obj.toss,poss=obj.poss,total_collected_amount=obj.total_collected_amount,TOS_as_on_Date=obj.TOS_as_on_Date,next_action_date=obj.next_action_date,current_principal_outstanding=obj.current_principal_outstanding,mortgage_type=obj.mortgage_type,category=obj.category,Details=obj.Details,value=obj.value,additional_email=obj.additional_email,additional_address=obj.additional_address,additional_no=obj.additional_no,disposition=disposition,sub_disposition=sub_disposition,callback_datetime=obj.callback_datetime,remark=remark,amount=obj.amount,mode_of_payment=obj.mode_of_payment,cheque_transaction_no=obj.cheque_transaction_no,contacted_dt=obj.contacted_dt,attempted = obj.attempted,caller_name="",uploaded_by=obj.uploaded_by,last_dial_no=i.phone_no,list_id=obj.list_id,lead_forkey_id=i.lead_forkey_id,dnd_detail=obj.dnd_detail,direction=direction)
                PredictiveDialedCaseStatus.objects.filter(id=i.id).delete()

    user_count = UserExtendedInfo.objects.filter(extension_status=1,extension_pause_status=0).count()
    dialed_nos = PredictiveDialedCaseStatus.objects.all().count()

    if user_count > dialed_nos:
        number_to_dial = (user_count*2) - dialed_nos
    else:
        number_to_dial = 0

    print(number_to_dial,"numbers to dialllsss",user_count,dialed_nos)

    return JsonResponse({'status':201,'number_to_dial':number_to_dial})


def check_virual_agent_status(request):
    number_to_dial=0
    available_agn=2
    number_to_dial=int(available_agn)*2
    print(number_to_dial)
    current_dt=datetime.now()
    query=IVRLeadStatus.objects.all()
    for i in query : 
        difference=current_dt-i.dial_dt
        if difference.total_seconds() >= 45 : 
            print("ready to delete")
            IVR_LogData.objects.create(lead_forkey_id=i.lead_forkey_id,phone_no=i.phone_no,call_status="Not Answered",ivr_number=i.ivr_number)
            IVRLeadStatus.objects.filter(id=i.id).delete()
    return JsonResponse({"status":200,"numbers_to_dial":number_to_dial})



def get_leads_to_dial(request):
    number_to_dial=request.GET.get('number_to_dial')
    num_ls=[]
    ivr_no=''
    try : 
        number_to_dial = int(number_to_dial)
    except : 
        number_to_dial = 0
    get_data=IVRLeads.objects.all()

    if number_to_dial and len(get_data) > 1 :
        get_data=get_data[: number_to_dial]
    elif number_to_dial == 0 :
        get_data = []
    else : 
        get_data=[get_data.first()] if get_data.first() else [] 
    print("ready to go",get_data)
    for i in get_data : 
        check=IVRLeadStatus.objects.filter(phone_no__icontains=i.phone_no).exists()
        if check : continue
        num_ls.append(i.phone_no)
        ivr_no=i.ivr_no
        IVRLeadStatus.objects.create(phone_no=i.phone_no,call_status="Dial",lead_forkey_id=i.lead_forkey_id,ivr_number=ivr_no)
        IVRLeads.objects.filter(id=i.id).delete()

    if num_ls:
        print("present its number",num_ls) 
        ivr_url=f'http://{main_url}/click_to_IVR'
        list_json=json.dumps(num_ls)
        requests.post(ivr_url,json={"num_ls":num_ls,"ivr_no":ivr_no})

    return JsonResponse({"status":200})


@csrf_exempt
def call_failed(request):
    if request.method == "POST":
        json_body = json.loads(request.body)
        print(json_body,"data from fail")
        phone_no = json_body['phone_no'][-10:]  if 'phone_no' in json_body else None
        if phone_no:
            print("its in phone")
            ivr_lead=IVRLeadStatus.objects.filter(phone_no = phone_no).last()
            if ivr_lead:
                print("ivr_lead")
                IVR_LogData.objects.create(phone_no=phone_no,call_status="Call Fail",lead_forkey_id=ivr_lead.lead_forkey_id,ivr_number=ivr_lead.ivr_number,callid=json_body['callid'])
                IVRLeadStatus.objects.filter(id=ivr_lead.id).delete()

        #     pred_case_id = PredictiveDialedCaseStatus.objects.filter(phone_no=phone_no).last()
        #     if not pred_case_id:
        #         return JsonResponse({'status':400})
        #     direction = "Outbound"
        #     disposition = "Not Answered"
        #     sub_disposition = "Not Answered"
        #     remark = ""
        #     obj = LeadDetails.objects.get(id=pred_case_id.lead_forkey_id)
        #     LogData.objects.create(borrowor_name=obj.borrowor_name,mobile_no=obj.mobile_no,address=obj.address,state=obj.state,pincode=obj.pincode,email=obj.email,dob=obj.dob,alt_mno_1=obj.alt_mno_2,alt_mno_3=obj.alt_mno_3,loanamt=obj.loanamt,loan_accountno=obj.loan_accountno,bankname=obj.bankname,trustname=obj.trustname,interest=obj.interest,systemlan=obj.systemlan,bankstate=obj.bankstate,nature_of_facility=obj.nature_of_facility,sanction_amount=obj.sanction_amount,loan_sanction_date=obj.loan_sanction_date,NPA_Date=obj.NPA_Date,interest_rate=obj.interest_rate,account_status=obj.account_status,security_value=obj.security_value,document_custody=obj.document_custody,security_flag=obj.security_flag,current_allocation=obj.current_allocation,current_allocation_date=obj.current_allocation_date,team_leader=obj.team_leader,zone_name=obj.zone_name,branch_name=obj.branch_name,branch_mail_id=obj.branch_mail_id,branch_contact_details=obj.branch_contact_details,toss=obj.toss,poss=obj.poss,total_collected_amount=obj.total_collected_amount,TOS_as_on_Date=obj.TOS_as_on_Date,next_action_date=obj.next_action_date,current_principal_outstanding=obj.current_principal_outstanding,mortgage_type=obj.mortgage_type,category=obj.category,Details=obj.Details,value=obj.value,additional_email=obj.additional_email,additional_address=obj.additional_address,additional_no=obj.additional_no,disposition=disposition,sub_disposition=sub_disposition,callback_datetime=obj.callback_datetime,remark=remark,amount=obj.amount,mode_of_payment=obj.mode_of_payment,cheque_transaction_no=obj.cheque_transaction_no,contacted_dt=obj.contacted_dt,attempted = obj.attempted,caller_name="",uploaded_by=obj.uploaded_by,last_dial_no=pred_case_id.phone_no,list_id=obj.list_id,lead_forkey_id=pred_case_id.lead_forkey_id,dnd_detail=obj.dnd_detail,direction=direction)
        #     PredictiveDialedCaseStatus.objects.filter(phone_no=phone_no).delete()
        # print(json_body,"jsonnnn bodyyyy")
        # return JsonResponse({'status':200})
    return JsonResponse({'status':300})