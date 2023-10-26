from ..views_imports import *
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


@api_view(["GET"])
@validate_bearer_token
def get_uploaded_data_lead(request):
    try:
        query = Leadupload.objects.filter(uploaded_by=request.user.username)
        serializeddata = LeadUpdateDataSerializer(query,many=True).data
        print(query,'query')
        return JsonResponse({'status':200,'data':serializeddata})
    except Exception as e:
        print(e)
        return JsonResponse({'status':404,'msg':e})
    return JsonResponse({'status':200})



@api_view(["GET"])
@validate_bearer_token
def check_list_id_leadupdate(request):
    query = Leadupload.objects.all()
    ser = LeaduploadSerializer(query,many=True)
    return JsonResponse({"status":400,"list_id":ser.data})


@api_view(["POST"])
@validate_bearer_token
def upload_lead(request):
    dt=datetime.now()
    user=request.user.username
    data = LeadDetails.objects
    if request.method == "POST":
        list_id = request.POST.get('list_id')
        list_name = request.POST.get('list_name')
        excel_file = request.FILES.get('excel_file')
        print(excel_file,'filepath')
        if list_id == "":
            return JsonResponse({'status':300,"message":"Enter List Id"})
        if Leadupload.objects.filter(listid=list_id).exists():
            return JsonResponse({'status':300,"message":"List_id already exists"})
        error = {"status":"200","message":"Success"}
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name
                excel_file.seek(0)  # Reset the file pointer to the beginning
                temp_file.write(excel_file.read())  # Save the InMemoryUploadedFile to the temporary file
            encoding = chardet.detect(open(temp_path, 'rb').read())['encoding']
            df = pd.read_csv(temp_path, encoding=encoding) #reading excel file
            row_count = df.shape[0] #counting rows
            print(row_count)
            df.fillna("",inplace=True) #replacing nan with empty str
            #upload list details
            Leadupload.objects.create(listid=list_id,listname=list_name,count=row_count,file=excel_file,uploaded_by=user)
            skipped_row = [] #skipped rows while uploading
            for i, row in df[::-1].iterrows():
                # print(len(data),"length of data")
                try:
                    # print(len(data),"length of data")
                    dt=datetime.now()

                    print(row['Name'],row['Mobile No.'],row['Address'],row['Amount'],row['Nach Status'],row["Bounce Reason"],row['Due Date'],row['Caller Name'],row["Agreement Number"])
                    
                    col_dict={'agreementno':str(row['Agreement Number']).strip(),'name':str(row['Name']).strip(),'mobile':str(row['Mobile No.']).strip(),'nach':str(row['Nach Status']).strip(),'bounce_reason':str(row['Bounce Reason']).strip(),'due_date':str(row['Due Date']).strip(),'address':str(row['Address']).strip(),'amount':str(row['Amount']).strip(),'callername':str(row['Caller Name']).strip()} #dictionary to save the datas of column and convert it to string
                    print(row['Caller Name'],'dictionary')
                    data = LeadDetails.objects.filter(agreement_no=col_dict['agreementno']).last()
                    upd_obj = LeadDetails.objects.get(id = data.id )
                    print(data,upd_obj,"thisssssssssssssssss")
                    if len(col_dict['name']) > 1:
                        upd_obj.name = col_dict['name']
                    if len(col_dict['mobile']) > 1:
                        upd_obj.mobile_no = col_dict['mobile']
                    if len(col_dict['nach']) > 1:
                        print("in nach status")
                        upd_obj.nach_status = col_dict['nach']
                    if len(col_dict['due_date']) > 1:
                        col_dict['due_date'] = convert_date(col_dict['due_date'])
                        upd_obj.due_date = col_dict['due_date']
                    if len(col_dict['address']) > 1:
                        upd_obj.address = col_dict['address']
                    if len(col_dict['amount']) > 1:
                        print("in amount")
                        upd_obj.main_amount = col_dict['amount']
                    if len(col_dict['callername']) > 1:
                        print("inside callerrrrrrrrrrrrrrrr",col_dict['callername'],type(col_dict['callername']))
                        if col_dict['callername'].lower().strip() == "na":
                            print("inside naaaaaaaaaa")
                            upd_obj.caller_name = None
                            if not UnassignedDialing.objects.filter(lead_forkey_id=upd_obj.id).exists():
                                UnassignedDialing.objects.create(lead_forkey_id=upd_obj.id)
                            upd_obj.Unassigned = True
                        else:
                            upd_obj.caller_name = col_dict['callername']
                    if len(col_dict['bounce_reason']) > 1:
                        upd_obj.bounced_reason=col_dict['bounce_reason']
                    upd_obj.attempted = 0
                    upd_obj.lead_update_date=dt
                    upd_obj.save()
                except AttributeError:
                    error['status'] = 300
                    error['message']='Agreement No. is Mandatory'
                    return
                except KeyError:
                    print("Customer Name column not found in the dataset.")
                    error['status']=300
                    error['message']="Incorrect file format."
                    row_count = 0
                    return
                except Exception as e:
                    skipped_row.append(i+1)
                    error['status']=300
                    error['message']=str(e)
                    print(e,"eeeeeeeeeeee")
                    return
            print(skipped_row)
        except Exception as e:
            error['status']=300
            error['message']=str(e)
            print(e,"ffffffffffffffffffffff-")
        finally:
            print(error['message'],'finally')
            response_data = {
                "status": error['status'], 
                "message": error['message']
            }
            return JsonResponse(response_data)            
    return JsonResponse({"status":200})