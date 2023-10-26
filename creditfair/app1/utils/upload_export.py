from ..views_imports import *
from django.db import IntegrityError
import os
import tempfile
import chardet


def convert_date(dt):
    formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%y','%d-%m-%Y','%Y/%m/%d']
    for fmt in formats:
        try:
            dt = datetime.strptime(dt, fmt).date()
            return dt
        except ValueError:
            pass
    return None

@api_view(["POST"])
@validate_bearer_token
def datastatus(request):
    body = json.loads(request.body)
    an=body['an']
    listid=body['listid']
    print(an,listid)
    Dataupload.objects.filter(id=listid).update(status=an)
    print("info",an,listid,Dataupload.objects.filter(id=listid))
    return JsonResponse({'status':400})

@api_view(["GET"])
@validate_bearer_token
def get_uploaded_data(request):
    try:
        query = Dataupload.objects.filter(uploaded_by=request.user.username)
        serializeddata = DatauploadDataSerializer(query,many=True).data
        # print(query,'query')
        return JsonResponse({'status':200,'data':serializeddata})
    except Exception as e:
        print(e)
        return JsonResponse({'status':404,'msg':e})
    return JsonResponse({'status':200})


@api_view(["GET"])
@validate_bearer_token
def check_list_id(request):
    query = Dataupload.objects.all()
    ser = DatauploadSerializer(query,many=True)
    return JsonResponse({"status":200,"list_id":ser.data})

@api_view(["POST"])
@validate_bearer_token
def upload_ajax(request):
    user=request.user.username
    if request.method == "POST":
        module = request.user.module
        list_id = request.POST.get('list_id')
        list_name = request.POST.get('list_name')
        excel_file = request.FILES.get('excel_file')
        
        print(list_id,list_name,excel_file)

        # if list id already exists return error
        if list_id == "":
            return JsonResponse({'status':300,"message":"Enter List Id"})

        if Dataupload.objects.filter(listid=list_id).exists():
            return JsonResponse({'status':300,"message":"List_id already exists"})
        error = {"status":"200","message":"Success"}

        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name
                excel_file.seek(0)  # Reset the file pointer to the beginning
                temp_file.write(excel_file.read())  # Save the InMemoryUploadedFile to the temporary file
            encoding = chardet.detect(open(temp_path, 'rb').read())['encoding']
            print(encoding, "encodinggg")
            df = pd.read_csv(temp_path, encoding=encoding, dtype={'Mobile No': str, 'Aadhar No': str})  # reading excel file
            row_count = df.shape[0]  # counting rows
            skipped_row = []  # skipped rows while uploading
            duplicate_data = []
            duplicate_data_ct=[]
      
            print(row_count, "row count")
            df.fillna("", inplace=True)  # replacing NaN with empty string
            #upload list details
            obj = Dataupload.objects.create(listid=list_id,listname=list_name,count=row_count,file=excel_file,uploaded_by=user,module=module)
            obj.save()
            if  row_count == 0:
                print({"status": 300, "message": "No Data Found"})
                error['status'] = 300
                error["message"] = "No Data Found"
                return
            for i, row in df.iterrows():
                # print(i,row)
                try:

                    if len(str(row['Id'])) < 1 and len(row['Agreement Number']) < 1:
                        print("empttttt") 
                        Dataupload.objects.get(id=obj.id).delete()
                        error['status'] = 300
                        error["message"] = "Field Agreemnt Id and Id  is mandatory"
                        break
                    print(row['Agreement Number'],"after break")
                    
                    dt=datetime.now()
                    # converting str to date
                    row['First EMI Date'] = convert_date(row['First EMI Date'])
                    row['Due Date'] = convert_date(row['Due Date'])
                    print(row['Agreement Number'],"befaore create")
                    lead=LeadDetails.objects.create(agreement_no=row['Agreement Number'],agreement_id=row['Id'],name=row['Name'],co_name=row['Co Applicant Name'],co_mobile_no=row['Co Applicant Number'],merchant_name=row['Merchant  Name'],lender_name=row['Lender Name'],email=row['Email'],mobile_no=row['Phone'],main_amount=row['Amount'],first_emi_date=row['First EMI Date'],nach_status=row['Nach Status'],bounced_reason=row['Bounce Reason'],advisor=row['Advisor'],address=row['Current City'],state=row['Current State'],caller_name=row['Caller'],uploaded_by=user,due_date=row['Due Date'],pincode=row['Pincode'],lead_update_date=dt,list_forkey=obj,list_id=list_id)
                    lead.save()
                    print(lead,"Its created")
                    if row["Caller"] == None or row["Caller"] == "nan" or row["Caller"] == "":
                        print("in this")
                        UnassignedDialing.objects.create(lead_forkey_id=lead.id)
                        LeadDetails.objects.filter(id=lead.id).update(Unassigned=True)
                    
                except KeyError:
                    print("Customer Name column not found in the dataset.")
                    error['status']=300
                    error['message']="Incorrect file format."
                    row_count = 0
                    return
                except IntegrityError:
                    error["status"] = 300
                    # Create a dictionary for the duplicate row
                    duplicate_row = {
                        'id': i + 1,
                        'agreement_no': row['Agreement Number'],
                        'agreement_id': row['Id'],
                        'name': row['Name'],
                        'co_name': row['Co Applicant Name'],
                        'co_mobile_no': row['Co Applicant Number'],
                        'merchant_name': row['Merchant  Name'],
                        'lender_name': row['Lender Name'],
                        'email': row['Email'],
                        'mobile_no': row['Phone'],
                        'main_amount': row['Amount'],
                        'first_emi_date': row['First EMI Date'],
                        'nach_status': row['Nach Status'],
                        'bounced_reason':row['Bounce Reason'],
                        'advisor': row['Advisor'],
                        'address': row['Current City'],
                        'state': row['Current State'],
                        'caller_name': row['Caller'],
                        'due_date': row['Due Date'],
                        'pincode': row['Pincode'],
                        # 'list_forkey': obj.id,
                        # 'list_id': list_id,
                    }
                    
                    # Append the duplicate row dictionary to the duplicate_data list
                    duplicate_data.append(duplicate_row)

                    duplicate_data_ct.append(i+1)

                except Exception as e:
                    print("Error occurred:", e)
                    skipped_row.append(i + 1)
    
        except FileNotFoundError:
            error["status"] = 300
            error["message"] = "File not found."
        except Exception as e:
            print(e)
            error["status"]= 300
            error["message"] = str(e)
        finally:
            updated_row_count = row_count - len(skipped_row) - len(duplicate_data_ct)
            print(len(duplicate_data),len(skipped_row))
            Dataupload.objects.filter(id=obj.id).update(count=updated_row_count,data_count=row_count)
            print(updated_row_count)
            os.remove(temp_path)
            print("finallyyyyyyy",duplicate_data_ct,duplicate_data,error['status'],error['message'])
            duplicate_count=len(duplicate_data)
            if len(duplicate_data) != 0:
                duplicate_data = preprocess_data(duplicate_data)

                response_data = {
                    "status": error['status'], 
                    "message": error['message'],
                    'has_duplicate_data': True,
                    'duplicate_data': duplicate_data,
                    'duplicate_data_ct':duplicate_data_ct,
                    "duplicate_count":duplicate_count
                }
                return JsonResponse(response_data)
            return JsonResponse({"status": error['status'], "message": error['message'] , "duplicate_data": duplicate_data})



def preprocess_data(data_list):
    for item in data_list:
        for key, value in item.items():
            if value is None:
                item[key] = ""  # Convert None to empty string or any other desired representation
            else:
                item[key] = str(value)  # Convert all values to strings
    return data_list



# @api_view(['POST'])
# @validate_bearer_token
# def dataexport(request):
#     module = request.user.module
#     print(module,"modyulkekejejehj")
#     # user_list=[]
   
#     if request.user.user_level==9:
#         user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
#     elif request.user.user_level==10:
#         user_list=User.objects.filter(module=request.user.module,user_level=1).values_list('username', flat=True)
#     else:
#         user_list=User.objects.filter(username=request.user.username).values_list('username', flat=True)
#     print(user_list,'userlist')

#     body = json.loads(request.body)
#     sd = body['fdate'].rstrip() if 'fdate' in body else None
#     ed = body['tdate'].rstrip() if 'tdate' in body else None
#     sel = body["report_type"] if 'report_type' in body else None
#     process_sel = body["process_sel"] if 'process_sel' in body else None
#     direction_val = request.user.process
#     print(sd,ed,sel,direction_val,process_sel,"infgafdsajyaffafga")

#     if sel == "single":
#         print("reradadada")
#         read=LeadDetails.objects.filter(Q(caller_name__in=user_list)|Q(attempted_by__in=user_list)|Q(caller_name=""))
#     else:
#         read=LogData.objects.filter(Q(caller_name__in=user_list)|Q(attempted_by__in=user_list)|Q(caller_name__isnull=True)|Q(caller_name=""))

#     # if direction_val:
#     #     user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
#     #     read=read.filter(Q(caller_name__in=user_list)|Q(caller_name__in=["",None]))
        
#     print(read,"readddddddddddddd")
#     if sd != "" and ed != "":
#         sd = datetime.strptime(sd,'%d-%m-%Y')
#         ed= datetime.strptime(ed,'%d-%m-%Y')
#         sd= sd.strftime("%Y-%m-%d")
#         # ed= ed.strftime("%Y-%m-%d")
#         if sd == ed:
#             print(sd,ed,"containssss")
#             read=read.filter(contacted_dt__icontains=sd)
#         else:
#             print(sd,ed,"rangeeee")
#             ed = ed + timedelta(days=1)
#             read=read.filter(contacted_dt__range=[sd,ed])

    
#     # if  agn != None and agn != "":
#     #     print(agn,"inside if")
#     #     read=read.filter(caller_name=agn)
#     #     print(read)
    
#     if direction_val == "Inbound":
#         read=read.filter(Q(direction="Inbound")|Q(disposition="Missed Call"))
#     elif direction_val == "Outbound":
#         read=read.filter(direction="Outbound")

    

#     try:
#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="report.csv"'

#         wb = xlwt.Workbook(encoding='utf-8')
#         ws = wb.add_sheet('Users Data') 

#         row_num = 0

#         columns = ["Name","Mobile no","Address","State","Pincode","email","Co Applicant Name","Co Applicant Number","lender Name","Merchant Name","Agreement ID","Agreement No.","Due Date","NACH Status",'Bounced Reason',"Advisor","Amount","First EMI Amount","Reference Name1","Reference No1","Reference Name2","Reference No2","Additional Address","Additional Email","Additional No.","Last Dial No","Caller ID","Caller Name","Attempted By","Disposition","Sub Disposition","Contacted Datetime","AHT","Direction","Callback Time","Collected Amount","Mode of Payment","Transaction No.","Remark"]

#         rows =  read.values_list("name","mobile_no","address","state","pincode","email","co_name","co_mobile_no","lender_name","merchant_name","agreement_id","agreement_no","due_date","nach_status","bounced_reason","advisor","main_amount","first_emi_date","ref_name1","ref_no1","ref_name2","ref_no2","additional_address","additional_email","additional_no","last_dial_no","caller_name","first_name","attempted_by","disposition","sub_disposition","contacted_dt","AHT","direction","callback_datetime","amount","mode_of_payment","cheque_transaction_no","remark")

        
#         for col_num in range(len(columns)):
#             ws.write(row_num, col_num, columns[col_num]) # at 0 row 0 column 

#         # Sheet body, remaining rows
        
        
#         for row in rows:
#             row_num += 1
#             for col_num in range(len(row)):
                
#                 data=str(row[col_num]).replace("nan"," ")
#                 data=data.replace("None"," " )
#                 if col_num == 30:
#                     data = str(row[col_num])[:19]
#                     print(col_num,str(row[col_num])[:19] )
#                 ws.write(row_num, col_num,data)
#         wb.save(response)

#         return response

#     except Exception as e:
#         print(e)
#     return JsonResponse({"status":200})


@api_view(['POST'])
@validate_bearer_token
def dataexport(request):
    module = request.user.module
    print(module,"modyulkekejejehj")
    # user_list=[]
   
    if request.user.user_level==9:
        user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
    elif request.user.user_level==10:
        user_list=User.objects.filter(module=request.user.module,user_level=1).values_list('username', flat=True)
    else:
        user_list=User.objects.filter(username=request.user.username).values_list('username', flat=True)
    print(user_list,'userlist')

    body = json.loads(request.body)
    sd = body['fdate'].rstrip() if 'fdate' in body else None
    ed = body['tdate'].rstrip() if 'tdate' in body else None
    sel = body["report_type"] if 'report_type' in body else None
    process_sel = body["process_sel"] if 'process_sel' in body else None
    direction_val = request.user.process
    print(sd,ed,sel,direction_val,process_sel,"infgafdsajyaffafga")

    if sel == "single":
        print("reradadada")
        read=LeadDetails.objects.filter(Q(caller_name__in=user_list)|Q(attempted_by__in=user_list)|Q(caller_name=""))
    else:
        read=LogData.objects.filter(Q(caller_name__in=user_list)|Q(attempted_by__in=user_list)|Q(caller_name__isnull=True)|Q(caller_name=""))

    # if direction_val:
    #     user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
    #     read=read.filter(Q(caller_name__in=user_list)|Q(caller_name__in=["",None]))
        
    print(read,"readddddddddddddd")
    if sd != "" and ed != "":
        sd = datetime.strptime(sd,'%d-%m-%Y')
        ed= datetime.strptime(ed,'%d-%m-%Y')
        sd= sd.strftime("%Y-%m-%d")
        # ed= ed.strftime("%Y-%m-%d")
        if sd == ed:
            print(sd,ed,"containssss")
            read=read.filter(contacted_dt__icontains=sd)
        else:
            print(sd,ed,"rangeeee")
            ed = ed + timedelta(days=1)
            read=read.filter(contacted_dt__range=[sd,ed])

    
    # if  agn != None and agn != "":
    #     print(agn,"inside if")
    #     read=read.filter(caller_name=agn)
    #     print(read)
    
    if direction_val == "Inbound":
        read=read.filter(Q(direction="Inbound")|Q(disposition="Missed Call"))
    elif direction_val == "Outbound":
        read=read.filter(direction="Outbound")

    

    try:

        output = io.BytesIO()

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data') 

        row_num = 0

        columns = ["Name","Mobile no","Address","State","Pincode","email","Co Applicant Name","Co Applicant Number","lender Name","Merchant Name","Agreement ID","Agreement No.","Due Date","NACH Status",'Bounced Reason',"Advisor","Amount","First EMI Amount","Reference Name1","Reference No1","Reference Name2","Reference No2","Additional Address","Additional Email","Additional No.","Last Dial No","Caller ID","Caller Name","Attempted By","Disposition","Sub Disposition","Contacted Datetime","AHT","Direction","Callback Time","Collected Amount","Mode of Payment","Transaction No.","Remark"]
        

        rows =  read.values_list("name","mobile_no","address","state","pincode","email","co_name","co_mobile_no","lender_name","merchant_name","agreement_id","agreement_no","due_date","nach_status","bounced_reason","advisor","main_amount","first_emi_date","ref_name1","ref_no1","ref_name2","ref_no2","additional_address","additional_email","additional_no","last_dial_no","caller_name","first_name","attempted_by","disposition","sub_disposition","contacted_dt","AHT","direction","callback_datetime","amount","mode_of_payment","cheque_transaction_no","remark")

        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num]) # at 0 row 0 column 

        # Sheet body, remaining rows
        
        
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                data=str(row[col_num]).replace("nan"," ")
                data=data.replace("None"," " )
                if col_num == 30:
                    data = str(row[col_num])[:19]
                    # print(col_num,str(row[col_num])[:19] )
                ws.write(row_num, col_num,data)
        wb.save(output)
        output.seek(0)

        # Create a FileResponse with the Excel file content
        response = FileResponse(output, content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        return response

    except Exception as e:
        print(e)
        return JsonResponse({"status": 500, "message": "Error generating Excel file"})
    return JsonResponse({"status":200})




