from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    user_level=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=25,null=True,blank=True)
    is_loggedin = models.CharField(max_length=2,null=True,blank=True,default=0)
    extension = models.CharField(max_length=10,null=True,blank=True)
    display_pass = models.CharField(max_length=50,null=True,blank=True)
    process = models.CharField(max_length=25,null=True,blank=True)
    area = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.CharField(max_length=100,null=True,blank=True)
    prefix = models.CharField(max_length=5,null=True,blank=True)
    travelby = models.CharField(max_length=100,null=True,blank=True)
    user_created_by = models.CharField(max_length=200,null=True,blank=True)
    status=models.CharField(max_length=100,default="Not Ready")
    event=models.TimeField(null=True,blank=True)
    process=models.CharField(max_length=50,null=True,blank=True)
    mode=models.CharField(max_length=20,null=True,blank=True)
    calls=models.BigIntegerField(default=0,null=True,blank=True) 
    contacted=models.BigIntegerField(default=0,null=True,blank=True) 
    noncontacted=models.BigIntegerField(default=0,null=True,blank=True) 
    avgTT=models.CharField(max_length=100,null=True,blank=True)
    queue=models.CharField(max_length=100,null=True,blank=True)
    permission=models.IntegerField(null=True,blank=True,default=1)
    assigned_to=models.CharField(max_length=100,null=True,blank=True)
    module = models.CharField(max_length=15,null=True,blank=True)



class Valid_token(models.Model):
    datetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    token = models.CharField(max_length=400,null=True,blank=True)
    userid = models.CharField(max_length=200,null=True,blank=True)
    

class UserExtendedInfo(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    extension_status = models.CharField(max_length=2,null=True,blank=True)
    extension_pause_status = models.CharField(max_length=2,null=True,blank=True)

class LoginHistory(models.Model):
    username=models.CharField(max_length=100,null=True,blank=True)
    logdt=models.DateTimeField(null=True,blank=True)
    event = models.CharField(max_length=100,null=True,blank=True)

class Dataupload(models.Model):
    listid=models.CharField(max_length=100,null=True,blank=True,unique=True)
    listname=models.CharField(max_length=100,null=True,blank=True)
    file=models.FileField(upload_to='uploaded_csv/',blank=True,null=True)
    count = models.BigIntegerField(null=True,blank=True)
    entry=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    status=models.IntegerField(null=True,blank=True,default=1)
    data_count= models.BigIntegerField(null=True,blank=True)
    uploaded_by = models.CharField(max_length=100,null=True,blank=True)
    module=models.CharField(max_length=200,null="true")

class LeadDetails(models.Model):
    #customer_info
    name = models.CharField(max_length=200,null=True,blank=True)
    mobile_no = models.CharField(max_length=15,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    state = models.CharField(max_length=150,null=True,blank=True)
    pincode = models.CharField(max_length=10,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    co_name = models.CharField(max_length=200,null=True,blank=True)
    co_mobile_no = models.CharField(max_length=15,null=True,blank=True)

    #process_info
    lender_name = models.CharField(max_length=200,null=True,blank=True)
    merchant_name = models.CharField(max_length=200,null=True,blank=True)
    agreement_id = models.CharField(max_length=50,null=True,blank=True)
    agreement_no = models.CharField(unique=True,max_length=100,null=True,default=None)
    due_date = models.DateField(null=True,blank=True)
    nach_status = models.CharField(max_length=200,null=True,blank=True)
    bounced_reason = models.CharField(max_length=100,null=True,blank=True)
    advisor = models.CharField(max_length=200,null=True,blank=True)

    #process Additional Info
    main_amount = models.CharField(max_length=100,null=True,blank=True)
    first_emi_date = models.DateField(null=True,blank=True)

    #Reference details or mortgage details
    ref_name1 = models.CharField(max_length=200,null=True,blank=True)
    ref_no1 = models.CharField(max_length=15,null=True,blank=True)
    ref_name2 = models.CharField(max_length=200,null=True,blank=True)
    ref_no2 = models.CharField(max_length=15,null=True,blank=True)

    
    #additional added during call for export data
    additional_address = models.TextField(null=True,blank=True)
    additional_email = models.CharField(max_length=150,null=True,blank=True)
    additional_no = models.CharField(max_length=15,null=True,blank=True)

    # agent captured details
    disposition = models.CharField(max_length=30,null=True,blank=True)
    sub_disposition = models.CharField(max_length=200,null=True,blank=True)
    lc_remark = models.CharField(max_length=20,null=True,blank=True)
    callback_datetime = models.DateTimeField(null=True,blank=True)
    remark = models.TextField(null=True,blank=True)
    amount = models.CharField(max_length=30,null=True,blank=True)
    mode_of_payment = models.CharField(max_length=20,null=True,blank=True)
    dnd_detail = models.CharField(max_length=25,default=0)
    cheque_transaction_no = models.CharField(max_length=100,null=True,blank=True)


    # system capture details
    direction=models.CharField(max_length=15,null=True,blank=True)
    contacted_dt = models.DateTimeField(auto_now=True,blank=True,null=True)
    attempted = models.BigIntegerField(default=0,null=True,blank=True) 
    caller_name = models.CharField(max_length=100,null=True,blank=True)
    uploaded_by = models.CharField(max_length=100,null=True,blank=True)
    first_name = models.CharField(max_length=150,null=True,blank=True)

    last_dial_no = models.CharField(max_length=15,null=True,blank=True)
    list_forkey = models.ForeignKey(Dataupload,on_delete=models.CASCADE,null=True,blank=True)
    list_id = models.CharField(max_length=200,null=True,blank=True)
    AHT = models.CharField(max_length=20,null=True,blank=True)
    created_by = models.CharField(max_length=20,null=True,blank=True)
    contacted_probablity=models.CharField(max_length=10,null=True,default=0)

    #to view data according to lead details
    lead_update_date=models.DateTimeField(blank=True,null=True)

    #For progressive_Dialing
    attempted_by=models.CharField(max_length=100,null=True,blank=True)
    Unassigned=models.BooleanField(null=True,blank=True)


class LogData(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    mobile_no = models.CharField(max_length=15,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    state = models.CharField(max_length=150,null=True,blank=True)
    pincode = models.CharField(max_length=10,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    co_name = models.CharField(max_length=200,null=True,blank=True)
    co_mobile_no = models.CharField(max_length=15,null=True,blank=True)

    #process_info
    lender_name = models.CharField(max_length=200,null=True,blank=True)
    merchant_name = models.CharField(max_length=200,null=True,blank=True)
    agreement_id = models.CharField(max_length=50,null=True,blank=True)
    agreement_no = models.CharField(max_length=100,null=True,blank=True)
    due_date = models.DateField(null=True,blank=True)
    nach_status = models.CharField(max_length=200,null=True,blank=True)
    bounced_reason = models.CharField(max_length=100,null=True,blank=True)
    advisor = models.CharField(max_length=200,null=True,blank=True)

    #process Additional Info
    main_amount = models.CharField(max_length=100,null=True,blank=True)
    first_emi_date = models.DateField(null=True,blank=True)

    #Reference details or mortgage details
    ref_name1 = models.CharField(max_length=200,null=True,blank=True)
    ref_no1 = models.CharField(max_length=15,null=True,blank=True)
    ref_name2 = models.CharField(max_length=200,null=True,blank=True)
    ref_no2 = models.CharField(max_length=15,null=True,blank=True)

    
    #additional added during call for export data
    additional_address = models.TextField(null=True,blank=True)
    additional_email = models.CharField(max_length=150,null=True,blank=True)
    additional_no = models.CharField(max_length=15,null=True,blank=True)

    # agent captured details
    disposition = models.CharField(max_length=30,null=True,blank=True)
    sub_disposition = models.CharField(max_length=200,null=True,blank=True)
    callback_datetime = models.DateTimeField(null=True,blank=True)
    remark = models.TextField(null=True,blank=True)
    lc_remark = models.CharField(max_length=20,null=True,blank=True)


    amount = models.CharField(max_length=30,null=True,blank=True)
    mode_of_payment = models.CharField(max_length=20,null=True,blank=True)
    cheque_transaction_no = models.CharField(max_length=100,null=True,blank=True)

    # system capture details
    direction=models.CharField(max_length=15,null=True,blank=True)
    contacted_dt = models.DateTimeField(auto_now=True,blank=True,null=True)
    attempted = models.BigIntegerField(null=True,blank=True,default=0) 
    caller_name = models.CharField(max_length=100,null=True,blank=True)
    uploaded_by = models.CharField(max_length=100,null=True,blank=True)
    first_name = models.CharField(max_length=150,null=True,blank=True)

    last_dial_no = models.CharField(max_length=15,null=True,blank=True)
    list_forkey = models.CharField(max_length=30,null=True,blank=True)
    list_id = models.CharField(max_length=200,null=True,blank=True)
    dnd_detail = models.CharField(max_length=25,default=0)
    AHT = models.CharField(max_length=20,null=True,blank=True)
    contacted_probablity=models.CharField(max_length=10,null=True,default=0)

    #to view data according to lead details
    lead_update_date=models.DateTimeField(blank=True,null=True)

    #For progressive_Dialing
    attempted_by=models.CharField(max_length=100,null=True,blank=True)
    Unassigned=models.BooleanField(null=True,blank=True)

    lead_forkey = models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True,blank=True)

class AdditionalInfo(models.Model):
    email = models.CharField(max_length=100,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    pincode = models.CharField(max_length=10,null=True,blank=True)
    phone_no = models.CharField(max_length=15,null=True,blank=True)
    whatsapp_no = models.CharField(max_length=15,null=True,blank=True)
    relation = models.CharField(max_length=100,null=True,blank=True)
    lead_id = models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True,blank=True)


class disposition(models.Model):
    dispo=models.CharField(max_length=30,null=True,blank=True)
    sub_dispo=models.CharField(max_length=100,null=True,blank=True)
    direction=models.CharField(max_length=100,null=True,blank=True)


# ///////////////////////////////Lead Update  //////////////////////////////////////////////////////////////
class Leadupload(models.Model):
    listid=models.CharField(max_length=100,null=True,blank=True,unique=True)
    listname=models.CharField(max_length=100,null=True,blank=True)
    file=models.FileField(upload_to='lead_csv/',blank=True,null=True)
    count = models.BigIntegerField(null=True,blank=True)
    entry=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    status=models.IntegerField(null=True,blank=True,default=1)
    uploaded_by = models.CharField(max_length=100,null=True,blank=True)
# ///////////////////////////////Lead Update  //////////////////////////////////////////////////////////////

# //////////////////////////////////////ptp behaviuor//////////////////////////////////////////////////////////////////

class ptpbehaviour(models.Model):
    first_status = models.CharField(max_length=250,blank=True,null=True)
    first_date =  models.DateTimeField(null=True,blank=True)
    first_contact_datetime = models.DateTimeField(null=True,blank=True)
    next_status = models.CharField(max_length=250,blank=True,null=True)
    next_date = models.DateTimeField(null=True,blank=True)
    next_contact_datetime = models.DateTimeField(null=True,blank=True)
    callerid = models.CharField(max_length=250,blank=True,null=True)
    forkey = models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True,blank=True)
    main_amount = models.CharField(max_length=100,blank=True,null=True)
    ptp_amount = models.CharField(max_length=100,blank=True,null=True)
    lender_name = models.CharField(max_length=250,null=True,blank=True)
    name = models.CharField(max_length=250,null=True,blank=True)
    agreement_no = models.CharField(max_length=250,null=True,blank=True)
    module=models.CharField(max_length=50,null=True,blank=True)
# //////////////////////////////////////ptp behaviuor//////////////////////////////////////////////////////////////////

# //////////////////////////////////////quality//////////////////////////////////////////////////////////////////
class Score(models.Model):
    qs_id=models.CharField(max_length=100,null=True,blank=True)
    agent=models.CharField(max_length=100,null=True,blank=True)
    direction=models.CharField(max_length=100,null=True,blank=True)
    sub=models.CharField(max_length=100,null=True,blank=True)
    contacted_dt=models.CharField(max_length=100,null=True,blank=True)
    recordingfile=models.FileField(null=True)
   
    lastupdate=models.DateTimeField(null=True,blank=True)
    m1=models.BigIntegerField(null=True,blank=True)
    gm1=models.BigIntegerField(null=True,blank=True)
    m2=models.BigIntegerField(null=True,blank=True)
    gm2=models.BigIntegerField(null=True,blank=True)
    m3=models.BigIntegerField(null=True,blank=True)
    gm3=models.BigIntegerField(null=True,blank=True)
    m4=models.BigIntegerField(null=True,blank=True)
    gm4=models.BigIntegerField(null=True,blank=True)
    m5=models.BigIntegerField(null=True,blank=True)
    gm5=models.BigIntegerField(null=True,blank=True)
    m6=models.BigIntegerField(null=True,blank=True)
    gm6=models.BigIntegerField(null=True,blank=True)
    m7=models.BigIntegerField(null=True,blank=True)
    gm7=models.BigIntegerField(null=True,blank=True)
    m8=models.BigIntegerField(null=True,blank=True)
    gm8=models.BigIntegerField(null=True,blank=True)
    m9=models.BigIntegerField(null=True,blank=True)
    gm9=models.BigIntegerField(null=True,blank=True)
    total=models.BigIntegerField(null=True,blank=True)
    got=models.BigIntegerField(null=True,blank=True)
    phone=models.CharField(max_length=30,null=True,blank=True)
    performance=models.CharField(max_length=100,null=True,blank=True)
    
# //////////////////////////////////////quality//////////////////////////////////////////////////////////////////


# ///////////////////////////////DNC  //////////////////////////////////////////////////////////////

class dnd_upload(models.Model):
    file=models.FileField(upload_to='dnd_csv/',blank=True,null=True)
    uploaded_by=models.CharField(max_length=100,null=True,blank=True)
    count = models.BigIntegerField(null=True,blank=True)
    entry=models.DateTimeField(null=True,blank=True)

class dnd(models.Model):
    dnd_forid=models.ForeignKey(dnd_upload,on_delete=models.CASCADE,null=True)
    per_forid=models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True)
    # loan=models.CharField(max_length=100,null=True,blank=True)
    reason=models.TextField(null=True,blank=True)
    enddate=models.DateField(null=True,blank=True)


# ///////////////////////////////DNC  //////////////////////////////////////////////////////////////




# ////////////////////////////////////APR/////////////////////////////////////////////////////////////

class agentevents(models.Model):
    agentname=models.CharField(max_length=100,null=True,blank=True)
    call_from=models.CharField(max_length=100,null=True,blank=True)
    call_to=models.CharField(max_length=100,null=True,blank=True)
    call_time=models.DateTimeField(null=True,blank=True)
    hang_time=models.DateTimeField(null=True,blank=True)
    disposed_time=models.DateTimeField(null=True,blank=True)
    call_id = models.CharField(max_length=150,null=True,blank=True)
    personalkey= models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True,blank=True)


class agent_performance(models.Model):
    agentname=models.CharField(max_length=100,null=True,blank=True)
    login_hours=models.CharField(max_length=20,null=True,blank=True,default="0:00:00")
    break_hours=models.CharField(max_length=20,null=True,blank=True,default="0:00:00")
    idle_time=models.CharField(max_length=20,null=True,blank=True,default="0:00:00")
    talk_time=models.CharField(max_length=20,null=True,blank=True,default="0:00:00")
    wrap_up=models.CharField(max_length=20,null=True,blank=True,default="0:00:00")
    hold_hours=models.CharField(max_length=20,null=True,blank=True,default="0:00:00")
    ringing_hrs=models.CharField(max_length=20,null=True,blank=True,default="0:00:00")
    event_date=models.DateField(null=True,blank=True)
    nonactive_hrs = models.CharField(max_length=100,null=True,blank=True,default="0:00:00")
    active_status = models.CharField(max_length=100,null=True,blank=True,default="inactive")
    last_event=models.CharField(max_length=20,null=True,blank=True,default="login")
    date_time_added = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    tos = models.CharField(max_length=20,null=True,blank=True,default="0:00:00")
    AHT = models.CharField(max_length=20,null=True,blank=True,default="0:00:00")
    first_name = models.CharField(max_length=100,blank=True,null=True)



class break_details(models.Model):
    agentname=models.CharField(max_length=100,null=True,blank=True)
    break_name=models.CharField(max_length=100,null=True,blank=True)
    break_start=models.DateTimeField(null=True)
    break_end=models.DateTimeField(null=True)
    break_total=models.CharField(max_length=100,null=True,blank=True)

class infobreak(models.Model):
    agentname=models.CharField(max_length=200,null=True,blank=True)
    date=models.DateField(null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    total=models.CharField(max_length=20,null=True,blank=True,default="00:00:00")


# ////////////////////////////////////APR/////////////////////////////////////////////////////////////

# /////////////////////////////////////// mqtt/////////////////////////////////////////////////////////////

class AgentCall(models.Model):
    request_id = models.CharField(max_length=200,null=True,blank=True)
    event = models.CharField(max_length=250,null=True,blank=True)
    extension = models.CharField(max_length=25,null=True,blank=True)
    status = models.CharField(max_length=250,null=True,blank=True)
    ipaddr = models.CharField(max_length=250,null=True,blank=True)
    channel = models.CharField(max_length=250,null=True,blank=True)
    message =  models.CharField(max_length=250,null=True,blank=True)
    callid = models.CharField(max_length=250,null=True,blank=True)
    callee = models.CharField(max_length=250,null=True,blank=True)

class CallRecording(models.Model):
    agentname=models.CharField(max_length=40,null=True,blank=True)
    sub_dispos=models.CharField(max_length=100,null=True,blank=True)
    callid = models.CharField(max_length=200,null=True,blank=True)
    src = models.CharField(max_length=200,null=True,blank=True)
    srctech = models.CharField(max_length=200,null=True,blank=True)
    dst= models.CharField(max_length=200,null=True,blank=True)
    dsttech = models.CharField(max_length=200,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    billsec = models.CharField(max_length=200,null=True,blank=True)
    disposition = models.CharField(max_length=200,null=True,blank=True)
    direction = models.CharField(max_length=200,null=True,blank=True)
    recordfile = models.CharField(max_length=200,null=True,blank=True)
    dtmf=models.CharField(max_length=4,null=True,blank=True)


class Incoming_info(models.Model):
    direction =models.CharField(max_length=100,null=True,blank=True)
    source=models.CharField(max_length=100,null=True,blank=True)
    destination=models.CharField(max_length=100,null=True,blank=True)
    callid=models.CharField(max_length=100,null=True,blank=True)
    called=models.CharField(max_length=100,null=True,blank=True)
    caller=models.CharField(max_length=100,null=True,blank=True)
    income_date=models.DateTimeField(null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True)

class Calltransfer(models.Model):
    extension=models.CharField(max_length=100,null=True,blank=True)
    call_id=models.CharField(max_length=100,null=True,blank=True)
    peer_id=models.CharField(max_length=100,null=True,blank=True)
    channel_id=models.CharField(max_length=100,null=True,blank=True)
    direction=models.CharField(max_length=100,null=True,blank=True)
    to_num=models.CharField(max_length=100,null=True,blank=True)


class Inbound_log(models.Model):
    callid = models.CharField(max_length=200,null=True,blank=True)
    src = models.CharField(max_length=200,null=True,blank=True)
    srctech = models.CharField(max_length=200,null=True,blank=True)
    dst= models.CharField(max_length=200,null=True,blank=True)
    dsttech = models.CharField(max_length=200,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    billsec = models.CharField(max_length=200,null=True,blank=True)
    disposition = models.CharField(max_length=200,null=True,blank=True)
    direction = models.CharField(max_length=200,null=True,blank=True)
    recordfile = models.CharField(max_length=200,null=True,blank=True)
    count=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=200,null=True,blank=True)
    contacted_dt=models.DateTimeField(null=True,blank=True)

class QueueLog(models.Model):
    direction =models.CharField(max_length=100,null=True,blank=True)
    source=models.CharField(max_length=100,null=True,blank=True)
    destination=models.CharField(max_length=100,null=True,blank=True)
    callid=models.CharField(max_length=100,null=True,blank=True)
    called=models.CharField(max_length=100,null=True,blank=True)
    caller=models.CharField(max_length=100,null=True,blank=True)
    income_date=models.DateTimeField(null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True)

# /////////////////////////////////////// mqtt/////////////////////////////////////////////////////////////


class EOM(models.Model):
    profile_img = models.FileField(null=True,blank=True)
    profile_name = models.CharField(max_length=20,null=True,blank=True)
    change_dt=models.DateTimeField(null=True,blank=True)
    module=models.CharField(max_length=100,blank=True,null=True)

class Queues(models.Model):
    queue_no = models.CharField(max_length=10,null=True,blank=True)
    queue_name = models.CharField(max_length=50,null=True,blank=True)


#//////////////////////////////////SMS Starts///////////////////////////////////////////////////////////#


class SMSUpload(models.Model):
    upload_by=models.CharField(max_length=100,null=True,blank=True)
    smsid=models.CharField(max_length=100,null=True,blank=True,unique=True)
    smstype=models.CharField(max_length=100,null=True,blank=True)
    file=models.FileField(null=True)
    count = models.BigIntegerField(null=True,blank=True)
    entry=models.DateTimeField(null=True,blank=True)
    sent=models.CharField(max_length=100,null=True,blank=True)

class SMSDetails(models.Model):
    phone_no=models.CharField(max_length=100,null=True,blank=True)
    Date=models.DateField(null=True,blank=True)
    loan_account_no=models.CharField(max_length=100,null=True,blank=True,)
    amount=models.CharField(max_length=100,null=True,blank=True)
    agency_name=models.CharField(max_length=100,null=True,blank=True)
    response=models.CharField(max_length=100,null=True,blank=True)
    smsty=models.CharField(max_length=100,null=True,blank=True)
    sms=models.CharField(max_length=1000,null=True,blank=True)
    entry=models.DateField(null=True,blank=True)
    created_by=models.ForeignKey(SMSUpload,on_delete=models.CASCADE,null=True)


#//////////////////////////////////SMS ends///////////////////////////////////////////////////////////#


#///////////////////////////////////// Unassigned Case starts///////////////////////////////////////#
class UnassignedDialing(models.Model):
    lead_forkey=models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True)
    attempted_by=models.CharField(max_length=100,null=True,blank=True)
    sub_dispo=models.CharField(max_length=100,null=True,blank=True)
    dispo=models.CharField(max_length=100,null=True,blank=True)
    caller_name=models.CharField(max_length=100,null=True,blank=True)
#///////////////////////////////////// Unassigned Case ends///////////////////////////////////////#


class QueueDetails(models.Model) : 
    queue_no=models.CharField(max_length=10,null=True,blank=True)
    queue_name=models.CharField(max_length=50,null=True,blank=True)
    extension=models.CharField(max_length=10,null=True,blank=True)
    status = models.CharField(max_length=10,null=True,blank=True)
    paused=models.CharField(max_length=10,null=True,blank=True)
    dt=models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=50,null=True,blank=True)

class PredictiveLeads(models.Model):
    phone_no = models.CharField(max_length=20,null=True)
    case_status = models.CharField(max_length=30,null=True)
    lead_forkey = models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True)

class PredictiveDialedCaseStatus(models.Model):
    phone_no = models.CharField(max_length=20,null=True,blank=True)
    dial_dt = models.DateTimeField(auto_now=True,null=True)
    lead_forkey = models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True)
    call_status = models.CharField(max_length=40,null=True)


#//////////////////////////IVR starts /////////////////////////////////////////////////#

class IVRLeads(models.Model):
    phone_no = models.CharField(max_length=20,null=True)
    case_status = models.CharField(max_length=30,null=True)
    lead_forkey = models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True)
    ivr_no=models.CharField(max_length=30,null=True)

class IVRLeadStatus(models.Model):
    phone_no = models.CharField(max_length=20,null=True,blank=True)
    dial_dt = models.DateTimeField(auto_now=True,null=True)
    lead_forkey = models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True)
    call_status = models.CharField(max_length=40,null=True)
    ivr_number=models.CharField(max_length=20,null=True,blank=True)

class IVR_LogData(models.Model):
    lead_forkey=models.ForeignKey(LeadDetails,on_delete=models.CASCADE,null=True)
    phone_no=models.CharField(max_length=20,null=True,blank=True)
    call_status = models.CharField(max_length=40,null=True)
    ivr_number=models.CharField(max_length=20,null=True,blank=True)
    dtmf=models.CharField(max_length=10,null=True,blank=True)
    dt=models.DateTimeField(auto_now=True,null=True)
    callid=models.CharField(max_length=50,null=True,blank=True)
    dst= models.CharField(max_length=40,null=True)
    dsttech= models.CharField(max_length=40,null=True)

#//////////////////////////IVR ends /////////////////////////////////////////////////#


class Calling_filters(models.Model):
    mode = models.CharField(max_length=30,blank=True,null=True)
    fromdate = models.CharField(max_length=30,blank=True,null=True)
    todate = models.CharField(max_length=30,blank=True,null=True)
    listid = models.TextField(blank=True,null=True)
    subdisposition = models.TextField(blank=True,null=True)
    operator = models.CharField(max_length=20,blank=True,null=True)
    attempts = models.CharField(max_length=5,blank=True,null=True)
    assigndatetime = models.CharField(max_length=30,blank=True,null=True)
    assigned_by = models.CharField(max_length=30,blank=True,null=True)