from ..views_imports import *
from django.db import IntegrityError
import os
import chardet
import tempfile


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
def get_uploaded_data_dnd(request):
    try:
        query = dnd_upload.objects.filter(uploaded_by=request.user.username)
        serializeddata = DndUploadDataSerializer(query,many=True).data
        return JsonResponse({'status':200,'data':serializeddata})
    except Exception as e:
        print(e)
        return JsonResponse({'status':404,'msg':e})
    return JsonResponse({'status':200})

@api_view(["POST"])
@validate_bearer_token
def upload_dnd(request):
    dt=datetime.now()
    user=request.user.username
    data = LeadDetails.objects
    excel_file = request.FILES.get('excel_file')
    print(excel_file,'filepath')
    error = {"status":"200","message":"Success"}
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            excel_file.seek(0)  # Reset the file pointer to the beginning
            temp_file.write(excel_file.read())  # Save the InMemoryUploadedFile to the temporary file
        encoding = chardet.detect(open(temp_path, 'rb').read())['encoding']
        df = pd.read_csv(temp_path,encoding=encoding,dtype={'Mobile No.':str}) #reading excel file
        row_count = df.shape[0] #counting rows
        print(row_count)
        df.fillna("",inplace=True) #replacing nan with empty str
        #upload list details
        update_dnd_upload=dnd_upload.objects.create(entry=dt,count=row_count,file=excel_file,uploaded_by=user)
        skipped_row = [] #skipped rows while uploading
        # data = data.filter(list_forkey__status__icontains="0")
        for i, row in df.iterrows():
            print('excel datas',row['Mobile No.'],row['Reason'],row['End Date'])
            try:
                # upd_obj = LeadDetails.objects.get(id = update_dnd.id )
                update_dnd = LeadDetails.objects.filter(mobile_no=row['Mobile No.']).last()
                # print(upd_obj,'upd_obj')
                end__date=str(row['End Date']).strip()
                if len(end__date) > 1:
                    LeadDetails.objects.filter(mobile_no=row['Mobile No.']).update(dnd_detail=1)
                    temp=convert_date(end__date)
                    dnd.objects.create(dnd_forid=update_dnd_upload,per_forid=update_dnd,reason=row['Reason'],enddate=temp)
                else:
                    raise AttributeError
            except AttributeError:
                error['status'] = 300
                error['message']='Mobile No. is Mandatory'
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


def dnd_update(request):
    dt=datetime.now().date()
    data=dnd.objects.filter(enddate=dt)
    print(data,'datas')
    for i in data:
        lead_data=LeadDetails.objects.filter(id=i.per_forid_id).update(dnd_detail=0)
        print(lead_data,'leaddetails')
    return JsonResponse({'status':200})