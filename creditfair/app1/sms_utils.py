from .models import *
from datetime import datetime
import requests
import ast

sms_api_key = "n7OtTfzmtE6uXFjgMNmQ5g"
    #   url=f"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=n7OtTfzmtE6uXFjgMNmQ5g&senderid=OMARPL&channel=2&DCS=0&flashsms=0&number={phone}&text=Your CIBIL will get impacted because of the non-payment of RS. {amt} in your loan account no.{loan}. You are requested to make the payment to OMKARA ARC against your respective{id}. In case of any query please call our toll-free number 1800120757575 or email us at customercare@omkaraarc.com with your loan account %26 contact details.&route=1&DLTtemplateid=1207165778565465130"

def sms_cibil(phone,loan,amt,smstyp,id,ent):

    url=f"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey={sms_api_key}&senderid=OMARPL&channel=2&DCS=0&flashsms=0&number={phone}&text=Your CIBIL will get impacted because of the non-payment of RS. {amt} in your loan account no.{loan}. You are requested to make the payment to OMKARA ARC against your respective{id}. In case of any query please call our toll-free number 1800120757575 or email us at customercare@omkaraarc.com with your loan account %26 contact details.&route=1&DLTtemplateid=1207165778565465130"
    g_url = requests.get(url)
    r=g_url.text
    # print("its",type(r))
    a=ast.literal_eval(r.replace("null",'None'))
    res=a["ErrorMessage"]
    # res = "Success"
    # print("error",a["ErrorMessage"])
    print("before saveing",res,phone,loan,amt,res,smstyp,id,ent)
    SMSDetails.objects.create(phone_no=phone,loan_account_no=loan,amount=amt,response=res,smsty=smstyp,created_by_id=id,entry=ent)

def sms_pca(phone,dt,loan,amt,agn,smstyp,id,ent):
    try:
        lpd = str(dt)
        lpd = datetime.strptime(lpd,'%Y-%m-%d')
        lpd = lpd.strftime("%Y-%m-%d")
    except Exception as e:
        lpd = None

    url=f"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey={sms_api_key}&senderid=OMARPL&channel=2&DCS=0&flashsms=0&number={phone}&text=We are in receipt of your payment amounting to Rs. {amt} dated {dt} in your loan account no {loan} by our authorised representative from {agn}. In case of any dispute with respect to your payment please contact toll-free number 1800120757575 or email us at customercare@omkaraarc.com with your loan account %26 contact details.&route=1&DLTtemplateid=1207165778580107494"
    g_url = requests.get(url)
    r=g_url.text
    print("its",type(r))
    a=ast.literal_eval(r.replace("null",'None'))
    res=a["ErrorMessage"]
    print("error",a["ErrorMessage"])
        
    s=SMSDetails.objects.create(phone_no=phone,Date=dt,loan_account_no=loan,amount=amt,agency_name=agn,response=res,smsty=smstyp,created_by_id=id,entry=ent)
    s.save()

def sms_awr(phone,loan,smsty,id,entry):
    url=f"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey={sms_api_key}&senderid=OMARPL&channel=2&DCS=0&flashsms=0&number={phone}&text=Your%20loan%20account%20number%20{loan}%20with%20Fullerton%20{loan}%20has%20been%20transferred%20to%20Omkara%20Assets%20Reconstruction%20Private%20Limited%20as%20of%2001.01.21.%20To%20have%20more%20clarity%20contact%20Omkara%20ARC%20on%201800120757575%20or%20email%20us%20at%20customercare@omkaraarc.com%20with%20your%20loan%20account%20%26%20contact%20details&route=1&DLTtemplateid=1207165778558300648"
    g_url = requests.get(url)
    r=g_url.text
    print("its",type(r))
    a=ast.literal_eval(r.replace("null",'None'))
    res=a["ErrorMessage"]
    print("error",a["ErrorMessage"])
    # res = "Success"

    s=SMSDetails.objects.create(phone_no=phone,loan_account_no=loan,response=res,smsty=smsty,created_by_id=id,entry=entry)
    s.save()
    print("done phon",phone)
    s=SMSUpload.objects.all()

def sms_pa(phone,dt,loan,amt,smsty,id,entry):
       
    try:
        lpd = str(dt)
        lpd = datetime.strptime(lpd,'%Y-%m-%d')
        lpd = lpd.strftime("%Y-%m-%d")
        
    except Exception as e:
        print(e)
        lpd = None
        
    url=f"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey={sms_api_key}&senderid=OMARPL&channel=2&DCS=0&flashsms=0&number={phone}&text=We%20are%20in%20receipt%20of%20your%20payment%20amounting%20to%20Rs.%20{amt}%20dated%20{lpd}%20in%20your%20loan%20account%20no.%20{loan}.%20In%20case%20of%20any%20dispute%20with%20respect%20to%20your%20payment%20please%20contact%20toll-free%20number%201800120757575%20or%20email%20us%20at%20customercare@omkaraarc.com%20with%20your%20loan%20account%20%26%20contact%20details.&route=1&DLTtemplateid=1207165778573635216"
    g_url = requests.get(url)
    r=g_url.text
    
    a=ast.literal_eval(r.replace("null",'None'))
    res=a["ErrorMessage"]
    # print("error",a["ErrorMessage"])
    
    res = "Success"

    s=SMSDetails.objects.create(phone_no=phone,Date=lpd,loan_account_no=loan,amount=amt,response=res,smsty=smsty,created_by_id=id,entry=entry)
    s.save()
    s=SMSUpload.objects.all()

