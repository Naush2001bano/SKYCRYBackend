from ..views_imports import *
from .apr_views import *

@api_view(['POST'])
def cms_data(request):
    username = request.user.username
    leadid = request.POST.get('lead__id')
    rendered = request.POST.get('rendered')
    progressive = request.POST.get('progressive')
    # print(leadid,'leadid')
    lead_data = LeadDetails.objects.filter(id=leadid)
    serialized_data = LeadDetailsSerializer(lead_data, many=True)
    
    # Access the serialized data as a list
    serialized_data_list = serialized_data.data
    
    # Add 'rendered' and 'progressive' to each item in the list
    for item in serialized_data_list:
        item['render'] = rendered
        item['progressive'] = progressive
        item['username'] = username
        
    # print(serialized_data_list)
    return JsonResponse({'status':200,'data':serialized_data_list})

@api_view(['POST'])
@validate_bearer_token
def get_dispositions(request):
    process=request.user.process
    
    dispo = disposition.objects.all().values('dispo').distinct()
    dispo = DispositionsSerializers(dispo,many=True)

    sdispo =  disposition.objects.all()
    print(sdispo,"sknjnfdkjfkewfkwwbfbb")
    if request.method == 'POST':
        sub_val = json.loads(request.body)
        print(sub_val,"POSTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
        if "sub_val" in sub_val:
            print(sub_val["sub_val"])
            sdispo = disposition.objects.filter(dispo=sub_val["sub_val"])
            print(sdispo,"subbbbbbbbbbbbbbbbbbbbbbbb")
            # if process:
            #     sdispo=sdispo.filter(direction=process)
            #     print("processssssssssssssssssss",sdispo,process)
    sdispo = SubDispositionsSerializers(sdispo,many=True) 
    print(sdispo,"SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsss")
    return JsonResponse({'status':200,'disposition':dispo.data,'subdisposition':sdispo.data})


@api_view(['POST'])
@validate_bearer_token
def get_additional_info(request):
    body = json.loads(request.body)
    try:
        obj = AdditionalInfo.objects.filter(lead_id=body['leadid'])
        obj = AdditionalInfoSerializer(obj,many=True)
    except Exception as e:
        print(e)
        return JsonResponse({"status":300,"data":"No data found"})

    return JsonResponse({"status":200,"data":obj.data})


@api_view(['POST'])
@validate_bearer_token
def get_additional_numbers(request):
    body = json.loads(request.body)
    print(body,'get_additional_numbers')
    try:
        obj = AdditionalInfo.objects.filter(lead_id=body['leadid'])
        obj2 = LeadDetails.objects.filter(id=body['leadid'])
        ser2 = LeadDetailsSerializer(obj2,many=True)
        ser = AllNumbersSerializers(obj,many=True)
        # print(ser2.data,"DATA")
    except Exception as e:
        print(e,"ERROR")
        return JsonResponse({"status":404,'msg':'Something went wrong'})
    
    return JsonResponse({"status":200,"data":ser.data,"data2":ser2.data})


@api_view(['POST'])
@validate_bearer_token
def addition_details(request):
    body = json.loads(request.body)
    id = body['id']
    contact_no = body['contact_no'] if "contact_no" in body else None
    address = body['address'] if "address" in body else None
    email = body['email'] if "email" in body else None
    wap_no = body['wap_no'] if "wap_no" in body else None
    wap_no_inp = body['wap_no_inp'] if "wap_no_inp" in body else None
    relation = body['relation'] if "relation" in body else None 
    print(contact_no,"contactnoooo",address,"adress",email,"emaillll",wap_no,"wap_nooooo",wap_no_inp,"wap_no_inp",relation,"ssdfds",id)

    try:
        lead_instance= LeadDetails.objects.get(id=id)
    except Exception as e:
        return JsonResponse({'status':300})
    


    if len(contact_no) > 6:
        AdditionalInfo.objects.create(lead_id=lead_instance,relation=relation,phone_no=contact_no)
    
    if address != "" and len(address) >= 1:
        AdditionalInfo.objects.create(lead_id=lead_instance,address=address)

    if wap_no is not None and wap_no != "add_no" and len(wap_no) > 7 :
        AdditionalInfo.objects.create(lead_id=lead_instance,whatsapp_no=wap_no)

    if len(wap_no_inp) > 4 and wap_no_inp is not None:
        AdditionalInfo.objects.create(lead_id=lead_instance,whatsapp_no=wap_no_inp)

    if len(email) > 5:
        AdditionalInfo.objects.create(lead_id=lead_instance,email=email)
    return JsonResponse({'status':200})


@api_view(['POST'])
@validate_bearer_token
def customer_history(request):
    body = json.loads(request.body)
    lead_id = body['leadid']
    obj = LogData.objects.filter(lead_forkey=lead_id).order_by('-id')[:10]
    ser = HistorySerializers(obj,many=True)
    return JsonResponse({"status":200,"data":ser.data})

@api_view(['POST'])
@validate_bearer_token
def cms_submit_ajax(request):
    body = json.loads(request.body)
    inbound = body['inbound'] if 'inbound' in body else None
    lead_id = body['lead_id'] if 'lead_id' in body else None
    dispo = body['dispo'] if 'dispo' in body else None
    subdispo = body['subdispo'] if 'subdispo' in body else None
    remark = body['remark'] if 'remark' in body else None
    ptp_date = body['ptp_date'] if 'ptp_date' in body else None
    ptp_amount = body['ptp_amount'] if 'ptp_amount' in body else None
    lc_remark = body['lc_remark'] if 'lc_remark' in body else None
    callback_time = body['callback_time'] if 'callback_time' in body else None
    schdatetime = body['schdatetime'] if 'schdatetime' in body else None
    ots_amount = body['ots_amount'] if 'ots_amount' in body else None
    paid_amt = body['paid_amt'] if 'paid_amt' in body else None
    mode = body['mode'] if 'mode' in body else None
    cheque_no = body['cheque_no'] if 'cheque_no' in body else None
    online = body['online'] if 'online' in body else None
    lastdial = body['lastdial'] if 'lastdial' in body else None
    miss_call = body['miss_call'] if 'miss_call' in body else None
    miss_id = body['miss_id'] if 'miss_id' in body else None

    username = request.user.username
    ext = request.user.extension

    current_date = datetime.now().date()

    if lastdial:
        lastdial = lastdial[:10]

    try:
        obj = LeadDetails.objects.get(id=lead_id)
        print(obj)
    except Exception as e:
        print(e)
        return JsonResponse({'status':300})

    if not dispo or not subdispo:
        return JsonResponse({'status':300})

    obj.disposition = dispo
    obj.sub_disposition = subdispo
    obj.remark = remark
    obj.attempted =  obj.attempted + 1

    if obj.Unassigned ==True:
        print("in if attempted is empty")
        if dispo =="Non-Contacted":
            print("in nc ready to add in unassign")
            if not UnassignedDialing.objects.filter(lead_forkey_id=obj.id).exists():
                UnassignedDialing.objects.create(lead_forkey_id=obj.id,dispo=dispo,sub_dispo=subdispo,caller_name=request.user.username)
            else:
                UnassignedDialing.objects.filter(lead_forkey_id=obj.id).update(dispo=dispo,sub_dispo=subdispo,caller_name=request.user.username)
    

    dt = datetime.now()
    am = dt + timedelta(minutes=0)
    
    if inbound == "Inbound":
        obj.direction='Inbound'
        obj.attempted_by =  username
    else:
        obj.direction = "Outbound"
        if subdispo in ['Promise To Pay','Paid','Schedule Call','Call Back','OTS Request'] and request.user.process != 'Inbound':
            obj.caller_name = username
        obj.attempted_by = username

    obj.first_name = request.user.first_name

    if miss_call == "missedcall":
        print("in missedcall",miss_id)
        misscall_qery=Inbound_log.objects.filter(id=miss_id)
    
        print(misscall_qery,"ueyugfergyu")
        misscall_qery.update(status=subdispo,disposition=subdispo,contacted_dt=dt) if subdispo == "Ringing No Response" else misscall_qery.update(status="Yes",disposition=subdispo,contacted_dt=dt)

    

    print(type(ptp_amount),ptp_amount,"werwerwerwerwerweew")

    ft= am.strftime("%Y-%m-%d %H:%M:%S")

    if callback_time == "15min":
        am = dt + timedelta(minutes=15)
    elif callback_time == "30min":
        am = dt + timedelta(minutes=30)
    elif callback_time == "45min":
        am = dt + timedelta(minutes=45)
    elif callback_time == "60min":
        am = dt + timedelta(minutes=60)


    if callback_time:

        obj.callback_datetime = am
    elif ptp_date:
        obj.callback_datetime = ptp_date
    else :
        obj.callback_datetime = schdatetime
    
    if ptp_amount:
        obj.amount = ptp_amount
    elif paid_amt:
        obj.amount = paid_amt
    elif ots_amount:
        obj.amount = ots_amount

    obj.mode_of_payment = mode

    if cheque_no:
        obj.cheque_transaction_no = cheque_no
    else:
        obj.cheque_transaction_no = online

    if lastdial:
        obj.last_dial_no = lastdial


    obj.save()
    
    u=User.objects.filter(username=request.user.username).last()
    if dispo=="Contacted":
        User.objects.filter(username=request.user.username).update(contacted=F("contacted")+1)
    elif dispo == "Non-Contacted":
        User.objects.filter(username=request.user.username).update(noncontacted=F("noncontacted")+1)

    u=User.objects.filter(username=request.user.username).last()
    user_total_calls=int(u.contacted)+int(u.noncontacted)
    User.objects.filter(username=request.user.username).update(calls=user_total_calls)
    print("**********************************",user_total_calls,"updated","**********************************************************")

    if dispo and lastdial:
        call_to = lastdial
    else:
        call_to = obj.mobile_no

    prefix = request.user.prefix
    phoneno = call_to   
    if prefix: phoneno = prefix+call_to
    
    agid = agentevents.objects.filter(call_time__icontains=current_date,personalkey=obj.id,call_from=request.user.extension,call_to__icontains=phoneno).last()

    print(agid)
    if agid:
        a = agentevents.objects.get(id=agid.id)
        a.disposed_time = dt
        a.save()
        print("averageeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee AHT",a.disposed_time,a.call_time)
        print(agid.disposed_time.strftime('%H:%M:%S'),"doooooooooooooooooooooooooooo",agid.call_time.strftime('%H:%M:%S'))
        aht=timediffernece(a.disposed_time.strftime('%H:%M:%S'),a.call_time.strftime('%H:%M:%S'))
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&",aht,"$$$$$$$$$$$$$$$$$$$4")
        ld=LeadDetails.objects.get(id=obj.id)
        ld.AHT = aht
        ld.save()

    # dispose_apr(request,obj.id) #need to uncomment
    obj=LeadDetails.objects.get(id=obj.id)
    print(obj.AHT,"ahtttttttttttttttttttttt")
    lgd = LogData.objects.create(name=obj.name,mobile_no=obj.mobile_no,address=obj.address,state=obj.state,pincode=obj.pincode,email=obj.email,co_name=obj.co_name,co_mobile_no=obj.co_mobile_no,lender_name=obj.lender_name,merchant_name=obj.merchant_name,agreement_id=obj.agreement_id,agreement_no=obj.agreement_no,nach_status=obj.nach_status,due_date=obj.due_date,advisor=obj.advisor,main_amount=obj.main_amount,first_emi_date=obj.first_emi_date,ref_name1=obj.ref_name1,ref_no1=obj.ref_no1,ref_name2=obj.ref_name2,ref_no2=obj.ref_no2,additional_email=obj.additional_email,additional_address=obj.additional_address,additional_no=obj.additional_no,disposition=obj.disposition,sub_disposition=obj.sub_disposition,callback_datetime=obj.callback_datetime,remark=obj.remark,amount=obj.amount,mode_of_payment=obj.mode_of_payment,cheque_transaction_no=obj.cheque_transaction_no,contacted_dt=obj.contacted_dt,attempted = obj.attempted,caller_name=obj.caller_name,uploaded_by=obj.uploaded_by,last_dial_no=obj.last_dial_no,list_id=obj.list_id,lead_forkey=obj,dnd_detail=obj.dnd_detail,direction=obj.direction,lc_remark=obj.lc_remark,first_name=obj.first_name,AHT=obj.AHT,attempted_by=obj.attempted_by,Unassigned=obj.Unassigned,lead_update_date=obj.lead_update_date)
    lgd.save()

    # cdr_update_dispositions(subdispo,ext,username,lead_id,call_to,obj.direction) #need to uncomment
    if ptpbehaviour.objects.filter(forkey=obj.id).exists() != True:
        
        if obj.sub_disposition == "Promise To Pay":
            
            pt_pquery = ptpbehaviour.objects.create(first_status=obj.sub_disposition,first_date=obj.callback_datetime,forkey_id=obj.id,callerid=obj.caller_name,first_contact_datetime=obj.contacted_dt,main_amount=obj.main_amount,agreement_no=obj.agreement_no,lender_name=obj.lender_name,name=obj.name,ptp_amount=obj.amount)
            pt_pquery.save()

    else :
        if ptpbehaviour.objects.filter(forkey=obj.id).filter(first_status="Promise To Pay").exists() and obj.sub_disposition == "Promise To Pay":
            ptpbehaviour.objects.filter(forkey=obj.id).update(first_status=obj.sub_disposition,first_date=obj.callback_datetime,first_contact_datetime=obj.contacted_dt,next_status=None,next_date=None,next_contact_datetime=None)
        else:
            ptpbehaviour.objects.filter(forkey=obj.id).update(next_status=obj.sub_disposition,next_date=obj.callback_datetime,next_contact_datetime=obj.contacted_dt)

    con_count=LogData.objects.filter(lead_forkey_id=obj.id,disposition="Contacted").count()
    non_con_count=LogData.objects.filter(lead_forkey_id=obj.id,disposition="Non-Contacted").count()
    atmp=LeadDetails.objects.filter(id=obj.id).last()
    print(atmp.id,atmp.attempted,"before function")
    # probablity=probability_calculation(atmp.attempted,con_count,non_con_count) #need to uncomment
    # LeadDetails.objects.filter(id=lead_id).update(contacted_probablity=probablity) #need to uncomment
    # LogData.objects.filter(id=lgd.id).update(contacted_probablity=probablity) #need to uncomment
    user_mode=User.objects.filter(id=request.user.assigned_to).last()
    u_mode=user_mode.mode


    query = f'''SELECT count(*) as count,
            SUM(CASE WHEN disposition = "Contacted" THEN 1 ELSE 0 END) AS contacted_count,
            SUM(CASE WHEN disposition = "Non-Contacted" THEN 1 ELSE 0 END) AS non_contacted_count
            FROM app1_logdata
            WHERE
                contacted_dt LIKE "%{current_date}%"
                AND (caller_name = "{username}" OR attempted_by = "{username}")'''

    with connection.cursor() as cursor:
        cursor.execute(query)
        result=cursor.fetchall()
    total,con,non_con = result[0]
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%",total,"kkjdnld",con,"dlknln",non_con,username,"/////////////////////////////")
    user_call_count =User.objects.get(id=request.user.id)
    user_call_count.calls = total
    user_call_count.contacted = con
    user_call_count.noncontacted = non_con
    user_call_count.save()

    return JsonResponse({'status':200,"u_mode":u_mode})

@api_view(['POST','GET'])
@validate_bearer_token
def set_pagerefreshed(request):
    del_log = request.GET.get('del_id')
    print(del_log,"delllll_logggg")
    username = request.user.username

    if del_log:
        LogData.objects.filter(id=del_log).delete()

    if request.method == "POST":
        filterValue=json.loads(request.body)
        id = filterValue['lead_id']
        print(id,username,"username idddd")
        u=User.objects.get(username=username)
        u.calls=int(u.calls)+1
        u.noncontacted=int(u.noncontacted)+1
        u.save()

        try:
            LeadDetails.objects.filter(id = id).update(disposition='Non-Contacted',sub_disposition="Page Refreshed",remark=f"Page Refreshed by {username} before submitting details")
            obj = LeadDetails.objects.get(id = id)
            obj.attempted_by=username if obj.Unassigned == True else ""
            lgd = LogData.objects.create(name=obj.name,mobile_no=obj.mobile_no,address=obj.address,state=obj.state,pincode=obj.pincode,email=obj.email,co_name=obj.co_name,co_mobile_no=obj.co_mobile_no,lender_name=obj.lender_name,merchant_name=obj.merchant_name,agreement_id=obj.agreement_id,agreement_no=obj.agreement_no,nach_status=obj.nach_status,due_date=obj.due_date,advisor=obj.advisor,main_amount=obj.main_amount,first_emi_date=obj.first_emi_date,ref_name1=obj.ref_name1,ref_no1=obj.ref_no1,ref_name2=obj.ref_name2,ref_no2=obj.ref_no2,additional_email=obj.additional_email,additional_address=obj.additional_address,additional_no=obj.additional_no,disposition=obj.disposition,sub_disposition=obj.sub_disposition,callback_datetime=obj.callback_datetime,remark=obj.remark,amount=obj.amount,mode_of_payment=obj.mode_of_payment,cheque_transaction_no=obj.cheque_transaction_no,contacted_dt=obj.contacted_dt,attempted = obj.attempted,caller_name=obj.caller_name,uploaded_by=obj.uploaded_by,last_dial_no=obj.last_dial_no,list_id=obj.list_id,lead_forkey=obj,dnd_detail=obj.dnd_detail,direction=obj.direction,lc_remark=obj.lc_remark,first_name=obj.first_name,AHT=obj.AHT,attempted_by=obj.attempted_by,Unassigned=obj.Unassigned,lead_update_date=obj.lead_update_date)
            lgd.save()
            return JsonResponse({"status":200,"log_id":lgd.id})
        except Exception as e:
            print(e,'msggg')
    return JsonResponse({"status":200})

