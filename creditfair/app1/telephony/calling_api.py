
import time
import json
import random, string
from ..models import *
from datetime import datetime
from app1.telephony.mqttclient import client
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from ..views_imports import validate_bearer_token


import random
from django.db import transaction

token = "zjku2Eie3Hv"


def generate_request_id():
    request_id=''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    request_id="LOCAL"+request_id
    return request_id

def get_hangup_id(request_id,ext):
    send_msg={"cmd": "extcallinfo","request_id": request_id,"extension":ext}
    info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))
    info.wait_for_publish()
    print(info.is_published(),"piblishhhhhing")
    time.sleep(1)
    print("its calll")
    return "Done"

def on_connect(client,usedata,flags,rc):
    if rc == 0:
        print("connected Successfully")
        global connected
        connected = True
        return
    else:
        print("connection failed")

# def connect():
#     return client


@api_view(["POST"])
@validate_bearer_token
def publish(request):
    request_id=generate_request_id()
    if request.method == 'POST':
        data=json.loads(request.body)
        print(data,"get data ")
        phoneno = data['dialed_no']
        per_id=data['lead_id']
        print(phoneno,per_id,"individual")
        current_datetime=datetime.now()
        extension = request.user.extension
        prefix = request.user.prefix
        print(extension,prefix,'hgshgshgshgshgshgshg')
        t=datetime.now().time()
        t=t.strftime("%H:%M:%S")
        print("hhf ieuf",phoneno,extension,per_id)

        if prefix:phoneno = prefix+phoneno
        send_msg = { "cmd": "dial", "request_id": request_id,"callee": phoneno,"caller": extension}
        if AgentCall.objects.filter(extension=extension).exists() != True:
            AgentCall.objects.create(callee=phoneno,request_id=request_id,extension=extension)
        else:
            AgentCall.objects.filter(extension=extension).update(callee=phoneno,request_id=request_id,extension=extension)

        info = client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg),0,True)
        info.wait_for_publish()
        print(info.is_published())
        time.sleep(1)
        print(request_id)
        agentevents.objects.create(agentname=request.user.username,call_from=extension,call_to=phoneno,call_time=current_datetime,hang_time=current_datetime,disposed_time=current_datetime,personalkey_id=per_id)
        LeadDetails.objects.filter(id=per_id).update(AHT=t)
        get_hangup_id(request_id=request_id,ext=extension)


    return JsonResponse({'status':200})

@api_view(["POST"])
@validate_bearer_token
def hang_up(request):
    
    json_data=json.loads(request.body)
    print("hanguppppppppppppppppppppppppppppppp",json_data)
    phoneno=json_data['dialed_no']
    prefix =  request.user.prefix
    if prefix:phoneno = prefix+phoneno
    current_date = datetime.now().date()
    per_id=request.POST.get("lead_id")
    extension=request.user.extension
    # phoneno = request.POST.get('number')[:10]
    # current_datetime=datetime.now()
    on_call=AgentCall.objects.filter(extension=extension).last()
    print(on_call.request_id,"parameters",on_call.channel,"***************************")
    send_msg={"cmd": "hangup","request_id":on_call.request_id, "callid": on_call.channel}
    info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    agid = agentevents.objects.filter(call_time__icontains=current_date,personalkey=per_id,call_from=extension,call_to=phoneno).last()
    print(agid)
    if agid:
        agentevents.objects.filter(id=agid.id).update(hang_time=current_datetime,disposed_time=current_datetime,call_id=on_call.callid)
    return JsonResponse({'status':200})





@api_view(["POST"])
@validate_bearer_token
def calling_response(request):
    if request.method == 'POST':
        q =  AgentCall.objects.filter(extension = request.user.extension)
        print(q,"slkdklsd",request.user.extension)
    return JsonResponse({'status':200,'response':list(q.values())}) 


def call_recording(request):
    send_msg={"cmd": "queue_paused","request_id": "e914b5997b762aa7","queue":"123456","extension":"8001",'paused':'no'}

    info = client.publish(f"device/{token}/api/v1.0/command/queue",json.dumps(send_msg),0,True)
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    return JsonResponse({'status':200})




def call_conf(request):
    send_msg={"cmd": "conf_status","request_id": "27397bc2427c9274cb92","conf":"98675","dialpermission":"","member":"102"}
    info = client.publish(f"device/{token}/api/v1.0/command/conf",json.dumps(send_msg),0,True)
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    return JsonResponse({'status':200})


def device_info(request):
    send_msg={"cmd": "deviceinfo","request_id": "27397bc2427c9274cb92"}
    info = client.publish(f"device/{token}/api/v1.0/command/system",json.dumps(send_msg),0,True)
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    return JsonResponse({'status':200})

@api_view(["POST"])
@validate_bearer_token
def incoming_hangup(request):
    if request.method == 'POST':
        print("hangupgdgdgdgdgdgdgddg")
        request_id = generate_request_id()
        data=json.loads(request.body)
        phoneno =data['dialed_no']
        per_id=data['lead_id']
        extension=request.user.extension
        current_datetime=datetime.now()
        current_date = datetime.now().date()
        on_call = Incoming_info.objects.filter(called=extension).last()
        AgentCall.objects.filter(extension=extension).update(callid=on_call.callid,callee=phoneno,event=on_call.direction)
        try:
            send_msg={"cmd": "hangup","request_id":request_id, "callid": on_call.callid}
            print(send_msg)
            info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))
            info.wait_for_publish()
            print(info.is_published())
            time.sleep(3)
            agid = agentevents.objects.filter(call_time__icontains=current_date,personalkey=per_id,call_from=extension,call_to=phoneno).last()
            print('agid',agid)
            if agid:
                agentevents.objects.filter(id=agid.id).update(hang_time=current_datetime,disposed_time=current_datetime,call_id=on_call.callid)
            return JsonResponse({'status':200})

        except Exception as e:
            print(e)

        return JsonResponse({'status':200})
    

@api_view(["POST"])
@validate_bearer_token
def incomming_response(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        phoneno = data['num']
        per_id=data['lead_id']
        current_datetime=datetime.now()
        extension = request.user.extension
        print('phonenumber',phoneno)
        agentevents.objects.create(agentname=request.user.username,call_from=extension,call_to=phoneno,call_time=current_datetime,hang_time=current_datetime,disposed_time=current_datetime,personalkey_id=per_id)        
    return JsonResponse({'status':200})


        

@csrf_exempt
def realtime(request):
    request_id = generate_request_id()
    print("its an request id",request_id)
    send_msg= {"cmd": "livecall", "request_id":request_id}
    info = client.publish(f"device/{token}/api/v1.0/command/system",json.dumps(send_msg),0,True)
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    return JsonResponse({'status':200})



def ext_call_info_search(request):
   
    print("*******************************************************************")
    request_id = generate_request_id()
    ext=request.user.extension
    send_msg={"cmd": "extcallinfo","request_id": request_id,"extension":ext}
    info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))
    info.wait_for_publish()
    print(info.is_published(),"piblishhhhhing")
    time.sleep(1)
    print("its calll")
    return JsonResponse({"status":200,"channelid" :"channelid"})


def attn_transfer(request):
    if request.method == "POST":
        to_num=request.POST.get("to_number")[:10]
        direction = request.POST.get('direction')
        peer=Calltransfer.objects.filter(to_num=request.user.extension).last()
        if direction == "outbound":
            peer=Calltransfer.objects.filter(extension=request.user.extension).last()
            
        Incoming_info.objects.filter(caller=peer.to_num).update(status="attend_transfer")
        request_id = generate_request_id()
        print(peer,"tooooooooooooooooooo",to_num)
        for i in to_num:
            print(i,to_num)
        send_msg={"cmd": "atxfer","request_id":request_id,"channelid":peer.channel_id,"tonumber":to_num}
        info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))

        info.wait_for_publish()
        print(info.is_published())
        time.sleep(3)
        return JsonResponse({"status":200})
    return JsonResponse({"status":300})


def attn_hangup(request):

    direction = request.POST.get('direction')
    print(direction,"directionsssssss")
    request_id = generate_request_id()
    peer=Calltransfer.objects.filter(to_num=request.user.extension).last()

    if direction == "outbound":
        peer=Calltransfer.objects.filter(extension=request.user.extension).last()

    
    send_msg={"cmd": "atxferoperate","request_id":request_id,"channelid":peer.channel_id,"operate":"complete"
}
    info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    return JsonResponse({"status":200})


@api_view(["GET"])
@validate_bearer_token
def queue_paused(request):
    request_id = generate_request_id()
    print("itsss calll")
    extension=request.user.extension
    if extension:
        send_msg={"cmd": "queue_paused","request_id":request_id,"queue":"","extension":extension,"paused":"yes"}
        info=client.publish(f"device/{token}/api/v1.0/command/queue",json.dumps(send_msg))
        info.wait_for_publish()
        # print(info.is_published())
        time.sleep(.5)
    return JsonResponse({"status":200})


@api_view(["GET"])
@validate_bearer_token
def queue_unpaused(request):
    request_id = generate_request_id()
    extension=request.user.extension
    if extension:
        send_msg={"cmd": "queue_paused","request_id":request_id,"queue":"","extension":extension,"paused":"no"}
        info=client.publish(f"device/{token}/api/v1.0/command/queue",json.dumps(send_msg))
        info.wait_for_publish()
        print(info.is_published())

    return JsonResponse({"status":200})

@api_view(["GET"])
@validate_bearer_token
def queue_status(request):
    request_id = generate_request_id()
    print("queuestatus calllinggggggggggggggggggggggggggg")
    q_ls=request.user.queue
    if q_ls and len(q_ls)>1:
        q_ls = json.loads(q_ls)
        for i in q_ls:
            print(i,"qlsssssssssssssssss")
            send_msg={"cmd": "queue_status","request_id":request_id,"queue":i}
            info=client.publish(f"device/{token}/api/v1.0/command/queue",json.dumps(send_msg))
            info.wait_for_publish()
            print(info.is_published())
    return JsonResponse({"status":200})

@api_view(["POST"])
@validate_bearer_token
def login_in_queue(request):
    print('login_in_queue')
    ext=request.user.extension
    json_body = json.loads(request.body)
    print(json_body,ext,type(json_body))
    # queue_no=request.POST.get("queue_ls")
    queue_no = json_body['queue_ls']
    request_id = generate_request_id()
    for i in queue_no:
        
        print("in iffffffffffffffffff QQQQQQQQQQQQQqqqqq",i,len(i))
        send_msg={"cmd": "queue_add","request_id":request_id, "queue":i,"extension":ext}
        info=client.publish(f"device/{token}/api/v1.0/command/queue",json.dumps(send_msg))
        info.wait_for_publish()
    #     print(info.is_published())
        # time.sleep(3)
    User.objects.filter(username=request.user.username).update(queue=json.dumps(queue_no))
    return JsonResponse({"status":200})


@api_view(["GET"])
@validate_bearer_token
def logout_queue(request):
    request_id = generate_request_id()
    ext=request.user.extension
    q_ls=request.user.queue
    if q_ls and len(q_ls)>1:
        q_ls = json.loads(q_ls)
        print(q_ls,type(q_ls))
        for i in q_ls:
            send_msg={"cmd": "queue_remove","request_id":request_id,"queue":i,"extension":ext}
            info=client.publish(f"device/{token}/api/v1.0/command/queue",json.dumps(send_msg))
            info.wait_for_publish()
            print(info.is_published())
            time.sleep(.5)
    return JsonResponse({"status":200})


def call_monitor(request):
    if request.method == "POST":
        mode=request.POST.get("mode")
        monitor_to=request.POST.get("monitor_to")
        extension=request.user.extension
        print("its call monitor post",monitor_to,mode,request.user.extension)
        request_id = generate_request_id()

        send_msg={"cmd": "listen","request_id": request_id,"monitor": request.user.extension,"extension":monitor_to,"type":mode}
        info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))
        info.wait_for_publish()
        print(info.is_published())
        if AgentCall.objects.filter(extension=extension).exists() != True:
            AgentCall.objects.create(request_id=request_id,extension=extension)
        else:
            AgentCall.objects.filter(extension=extension).update(request_id=request_id,extension=extension)

        time.sleep(3)
        get_hangup_id(request_id=request_id,ext=request.user.extension)
        return JsonResponse({"status":200})
    return JsonResponse({"status":300})


def call_monitor_hangup(request):
    if request.method == 'POST':
        print("hanguppppppppppppppppppppppppppppppp")
        extension=request.user.extension
        on_call=AgentCall.objects.filter(extension=extension).last()
        request_id = generate_request_id()

        print(on_call.request_id,"parameters",on_call.channel,"***************************")
        send_msg={"cmd": "hangup","request_id":request_id, "callid": on_call.channel}
        info=client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg))
        info.wait_for_publish()
        print(info.is_published())
        time.sleep(3)
        return JsonResponse({'status':200})

@csrf_exempt
def click_to_IVR(request):
    request_id = generate_request_id()
    if request.method == "POST" :
        json_body=json.loads(request.body)
        print(type(json_body),"dkjhfdkfhs",json_body)
        num_ls=json_body['num_ls']
        ivr_no=json_body['ivr_no']
        for i in num_ls :
            send_msg={"cmd": "dial","request_id":request_id, "caller": ivr_no,  "callee": '82'+i ,"dialpermission": "8201"}
            info = client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg),0,True)
            info.wait_for_publish()
            time.sleep(.5)
    return JsonResponse({'status':200})

# def ivr_start(request):
#     request_id=generate_request_id()
#     ivr=IVRLeads.objects.all()
#     if ivr :
#         data=ivr.first()
#         check=IVRLeadStatus.objects.filter(phone_no=data.phone_no)
#         if check : 
#             IVRLeads.objects.create(phone_no=data.phone_no,lead_forkey_id=data.lead_forkey)
#             IVRLeads.objects.filter(id=data.id).delete()
#         else:
#             print("ITS ready to hit the API")
#             IVRLeadStatus.objects.create(phone_no=data.phone_no,lead_forkey_id=data.lead_forkey)
#             send_msg={"cmd": "dial","request_id":request_id, "caller": "1001",  "callee": '82'+data.phone_no ,"dialpermission": "8201"}
#             info = client.publish(f"device/{token}/api/v1.0/command/call",json.dumps(send_msg),0,True)
#             info.wait_for_publish()
#             print(info.is_published())
#             IVRLeads.objects.filter(id=data.id).delete()
#             time.sleep(.5)
#         print(data.phone_no , "First IVR")
#     return JsonResponse({'status':200})


def add_nums(request):
    phone_numbers = ['9137475747', '7972861253', '7984830341']
    # Define the number of records you want to insert
    num_records = 18
    # Create records in a loop
    # with transaction.atomic():
    for _ in range(num_records):
        phone_number = random.choice(phone_numbers)
        IVRLeads.objects.create(phone_no=phone_number,lead_forkey_id=2)

    return JsonResponse({"status":200})