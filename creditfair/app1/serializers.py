from rest_framework import serializers
from rest_framework import status
from .models import *

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

class DatauploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataupload
        fields = ["listid","entry","status","uploaded_by","listname","count","data_count"]

class FilterSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeadDetails
        fields = ["id","list_id","name","agreement_no","agreement_id","mobile_no","dnd_detail","attempted"]

class LeadDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadDetails
        fields = ['id','name','mobile_no','address','state','pincode','email','co_name','co_mobile_no','lender_name','merchant_name','agreement_id','agreement_no','due_date','nach_status','bounced_reason','advisor','main_amount','first_emi_date','caller_name','sub_disposition','contacted_dt','remark','last_dial_no','Unassigned','attempted_by']


class DispositionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = disposition
        fields = ['dispo']

class SubDispositionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = disposition
        fields = ['dispo','sub_dispo']

class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = "__all__"

class AllNumbersSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = ['phone_no',"relation"]


class HistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = LogData
        fields = ['sub_disposition','caller_name','remark','contacted_dt','Unassigned','attempted_by']
        

class CallmanagementSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeadDetails
        fields = ["id","name","agreement_no","mobile_no","main_amount","contacted_probablity","contacted_dt","caller_name","callback_datetime",'sub_disposition']

class DataexportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadDetails
        fields = ["name","mobile_no","address","state","pincode","email","co_name","co_mobile_no","lender_name","merchant_name","agreement_id","agreement_no","due_date","nach_status","bounced_reason","advisor","main_amount","first_emi_date","ref_name1","ref_no1","ref_name2","ref_no2","additional_address","additional_email","additional_no","last_dial_no","caller_name","first_name","attempted_by","disposition","sub_disposition","contacted_dt","AHT","direction","callback_datetime","amount","mode_of_payment","cheque_transaction_no","remark"]


class CallrecordingSerializers(serializers.ModelSerializer):
    class Meta :
        model = CallRecording
        fields = ["start","recordfile","agentname","direction","sub_dispos","id","src","dst"]


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['id','agent','direction','sub','phone','recordingfile','contacted_dt']

class LeaduploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leadupload
        fields = ["listid"]

class LeadUpdateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leadupload
        fields = ["listid","listname","file","listname","count","entry"]

class DatauploadDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataupload
        fields = "__all__"

class DndUploadDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = dnd_upload
        fields = "__all__"


class QueueLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = QueueLog
        fields = "__all__"