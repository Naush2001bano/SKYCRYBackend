from . import views
from django.conf import settings
from django.urls import path
from .views_imports import checktoken
from .utils.loginandlogout import login_user_ajax,logoutuser,get_user_info
from .utils.upload_export import check_list_id,upload_ajax,dataexport,get_uploaded_data,datastatus
from .utils.search import searchajax
from .utils.nonattempted import non_attempted_data,non_attempted
from .utils.cms import *
from .utils.reminder import filterrm
from .utils.notification import notificationCount,misscallednotiCount
from .utils.recovery import filterrs
from .utils.apr_views import apr_report_export
from .utils.qualityanalysis import dropdowndata_quality,qsdata
from .utils.score import scoredata,get_score,score
from .export_views import export_qualityscore
from .export_views import export_qualityscore
from .utils.leadupdate import check_list_id_leadupdate,upload_lead,get_uploaded_data_lead
from .utils.dndupdate import upload_dnd,get_uploaded_data_dnd
from .utils.dashboard import agent_available,total_calls,top_five_dispo,paid_ptp_status

from .utils.incomming import *
from .telephony import calling_api
from .telephony.subscriber_api import *
from .utils.misscalled import *
from .utils.rtm import rtm_table,queue_screen
from .utils.createuser import create_user_data, savedata , update_pas, update_user,getuser_details,showstatus
from .utils.sms import smsajax ,check_sms_id

from .utils.teamoverall import ptpajax,ptp_status,paid_status,tvajax
from .utils.connect_to_customer import filter_sub_dispo_attmpts,IVRDatacount,get_data,fetch_Ivrdata,start_file_IVRexecution,stop_file_IVRexecution


urlpatterns = [
    path('checktoken',checktoken,name="checktoken"),
    path('login_user_ajax',login_user_ajax,name="login_user_ajax"),
    path('append_nav',views.append_nav,name="append_nav"),
    path('logout',logoutuser,name="logout"),
    path('get_user_info',get_user_info,name="get_user_info"),


    #dashboard
    path("agent_available",agent_available,name="agent_available"),
    path("totalcalls",total_calls,name="totalcalls"),
    path("top_five_dispo",top_five_dispo,name="top_five_dispo"),
    path("paid_ptp_status",paid_ptp_status,name="paid_ptp_status"),

    #search
    path('sajax',searchajax,name="sajax"),

    #cms
    path('cms_data',cms_data,name="cms_data"),
    path('get_dispositions',get_dispositions,name="get_dispositions"),
    path('addition_details',addition_details,name="addition_details"),
    path('get_additional_info',get_additional_info,name="get_additional_info"),
    path('get_additional_numbers',get_additional_numbers,name="get_additional_numbers"),
    path('customer_history',customer_history,name="customer_history"),
    path('cms_submit_ajax',cms_submit_ajax,name="cms_submit_ajax"),
    path('set_pagerefreshed',set_pagerefreshed,name="set_pagerefreshed"),

    #notification 
    path('notificationCount',notificationCount,name="notificationCount"),
    path('misscallednotiCount',misscallednotiCount,name="misscallednotiCount"),

    #reminder 
    path('filterrm',filterrm,name="filterrm"),

    #recovery
    path('filterrs',filterrs,name="filterrs"),

    #nonattempted
    path('non_attempted_data',non_attempted_data,name="non_attempted_data"),
    path('non_attempted',non_attempted,name="non_attempted"),
    
    #dataupload
    path('check_list_id',check_list_id,name="check_list_id"),
    path('upload_ajax',upload_ajax,name="upload_ajax"),
    path('get_uploaded_data',get_uploaded_data,name="get_uploaded_data"),
    path('datastatus',datastatus,name="datastatus"),

    #dnd
    path('upload_dnd',upload_dnd,name="upload_dnd"),
    path('get_uploaded_data_dnd',get_uploaded_data_dnd,name="get_uploaded_data_dnd"),

    #leadupdate
    path('check_list_id_leadupdate',check_list_id_leadupdate,name="check_list_id_leadupdate"),
    path('upload_lead',upload_lead,name="upload_lead"),
    path('get_uploaded_data_lead',get_uploaded_data_lead,name="get_uploaded_data_lead"),

    #dataexport
    path('dataexport',dataexport,name="dataexport"),

    #quality
    path('dropdowndata_quality',dropdowndata_quality,name="dropdowndata_quality"),
    path('qsdata',qsdata,name="qsdata"),
    path('scoredata',scoredata,name="scoredata"),
    path('get_score',get_score,name="get_score"),
    path('score',score,name="score"),
    path("export_qualityscore",export_qualityscore,name="export_qualityscore"),

    #apr
    path('apr_report_export',apr_report_export,name="apr_report_export"),

    #Calling API
    path('publish',calling_api.publish,name="publish"),
    path('call_response',calling_api.calling_response,name="call_response"),
    path("hangup",calling_api.hang_up,name="hangup"),
    path("rt",calling_api.realtime,name="rt"),
    path("queue_paused",calling_api.queue_paused,name="queue_paused"),
    path("queue_unpaused",calling_api.queue_unpaused,name="queue_unpaused"),
    path("incomming_response",calling_api.incomming_response,name="incomming_response"),
    path("incoming_hangup",calling_api.incoming_hangup,name="incoming_hangup"),
    path("click_to_IVR",calling_api.click_to_IVR,name="click_to_IVR"),

    # urls for subscriber_api.py starts
    path("check_misscall",check_misscall,name="check_misscall"),
    path("update_status",update_status,name="upate_status"),
    path("create_cdr",create_cdr,name="create_cdr"),
    path("update_calltransfer",update_calltransfer,name="update_calltransfer"),
    path("insert_incoming",insert_incoming,name="insert_incoming"),
    path("insert_queue_incoming",insert_queue_incoming,name="insert_queue_incoming"),
    path("delete_incoming",delete_incoming,name="delete_incoming"),
    path("get_queue_status_response",get_queue_status_response,name="get_queue_status_response"),
    path('change_user_extension_status',change_user_extension_status,name="change_user_extension_status"),

    #queue urls
    path("queue_paused",calling_api.queue_paused,name="queue_paused"),
    path("login_in_queue",calling_api.login_in_queue,name="login_in_queue"),
    path("logout_queue",calling_api.logout_queue,name="logout_queue"),
    path("queuestatus",calling_api.queue_status,name="queuestatus"),
    # urls for subscriber_api.py ends

    #view Urls starts
    path('cmsstrartstop',views.cmsstrartstop,name="cmsstrartstop"),


    #missedcall
    path("missajax",missajax,name="missajax"),
    path("check_missedcall",check_missedcall,name="check_missedcall"),

    #incoming cms
    path("check_for_incoming",check_for_incoming,name="check_for_incoming"),
    path('updatefield',updatefield,name="updatefield"),
    path("queues_call",queues_call,name="queues_call"),
    path("check_extension_in_queue",check_extension_in_queue,name="check_extension_in_queue"),
    path("queues_data",queues_data,name="queues_data"),
    
    #rtm
    path("rtm_table",rtm_table,name="rtm_table"),
    path("queue_screen",queue_screen,name="queue_screen"),

    #createuser
    path("create_user_data",create_user_data,name="create_user_data"),
    path("save",savedata,name="save"),
    path("update_pas",update_pas,name="update_pas"),
    path("getuser_details",getuser_details,name="getuser_details"),
    path("update_user",update_user,name="update_user"),
    path("showstatus",showstatus,name="showstatus"),

    #sms
    path('smsajax',smsajax,name="smsajax"),
    path('check_sms_id',check_sms_id,name="check_sms_id"),


    #teamoverall
    path("ptpajax",ptpajax,name='ptpajax'),
    path('ptp_status',ptp_status,name="ptp_status"),
    path('paid_status',paid_status,name="paid_status"),
    path("tvajax",tvajax,name="tvajax"),

    path("fil_sub_attmp",filter_sub_dispo_attmpts,name="fil_sub_attmp"),
    path("IVRDatacount",IVRDatacount,name='IVRDatacount'),
    path("get_data",get_data,name='get_data'),
    path("fetch_Ivrdata",fetch_Ivrdata,name='fetch_Ivrdata'),
    path("start_file_IVRexecution",start_file_IVRexecution,name='start_file_IVRexecution'),
    path("stop_file_IVRexecution",stop_file_IVRexecution,name='stop_file_IVRexecution'),

     path("check_virual_agent_status",check_virual_agent_status,name="check_virual_agent_status"),
    path('get_leads_to_dial',get_leads_to_dial,name="get_leads_to_dial"),

]