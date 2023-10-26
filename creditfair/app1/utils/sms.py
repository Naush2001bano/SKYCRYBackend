from ..views_imports import *
from ..sms_utils import *


@api_view(["POST"])
@validate_bearer_token
def smsajax(request):
    smsid = random.randint(1000,9999)
    id=0
    dsb = "none"
    print("smsajax")
    if request.method == 'POST':
        smsty=request.POST.get('smstype')
        fil = request.FILES.get('smsfile')
        entry=datetime.now()
        print(smsty,"type file",fil)
        try:
            df = pd.read_csv(fil,encoding='utf-16') #reading excel file
            row_count = df.shape[0] #counting rows
            print(row_count,"rowwww counttt")
            df.fillna("",inplace=True) #replacing nan with empty str 
            obj = SMSUpload.objects.create(smstype=smsty,file=fil,entry=entry,smsid=smsid,upload_by=request.user.username)
            obj.save()
            # csv_file_path = SMSUpload.objects.filter(smsid=smsid)
            # print("smsuploadddddd",csv_file_path)
            # for i in csv_file_path:   
            #     csv_file = i.file.url
            id=obj.id
          
            # path = f'{settings.BASE_DIR}{csv_file}'
            # df = pd.read_csv(path)

            # count = len(df.values)
            # print('asd',df.values)
            SMSUpload.objects.filter(id=id).update(count=row_count)

            msgs = ""
            cl = ''
            # res = "Success"


            if smsty == "Payment Acceptance":
                 for i, row in df.iterrows():
                    print(i,"all")
                    sms_pa(row['Phone No.'],row["Date"],row["Account No"],row["Amount"],smsty,id,entry)

            elif smsty=="Awareness":
                for  i, row in df.iterrows():
                    print(i,"aware")
                    sms_awr(row["Phone No"],row["Account No"],smsty,id,entry)
                    
                
            elif smsty=="Payment Confirmation Agency":
                for i, row in df.iterrows():
                    print("pay")
                    sms_pca(row["Phone"],row["Date"],row["Account No."],row["Amount"],row["Agency Name"],smsty,id,entry) 
                    
                
            elif smsty == "CIBIL":
                print("in cibil filter")
                for  i, row in df.iterrows():
                    print(row["Phone number"],row["Account No."],row["Amount"],"cibil")
                    sms_cibil(row["Phone number"],row["Account No."],row["Amount"],smsty,id,entry)
                   
            print("before update its ")   
            st=SMSDetails.objects.filter(created_by_id=id).filter(response="Success").count()
            SMSUpload.objects.filter(id=id).update(sent=st)
            s=SMSUpload.objects.all()
            # return render(request,"sms.html",{"s":s,'cl':cl,'msg':msgs,'dsb':dsb})
            return JsonResponse({'status':200})
        except Exception as e:
            print("error msg",e)
            return JsonResponse({'status':300})
            # messages.warning(request,"Something Went Wrong")
    return JsonResponse({'status':400})
    # return render(request,"sms.html",{"s":s,"dsb":dsb})




@api_view(["GET"])
@validate_bearer_token
def check_sms_id(request):
    query = SMSUpload.objects.all()
    ser = smsuploadSerializer(query,many=True)
    return JsonResponse({"status":400,"list_id":ser.data})

@api_view(["POST"])
@validate_bearer_token
def sms_export(request) :
    if request.method == "POST":
        body = json.loads(request.body)
        sd = body['fd'].rstrip() if 'fd' in body else None
        ed = body['td'].rstrip() if 'td' in body else None
    return
