from ..views_imports import *

@api_view(['POST'])
@validate_bearer_token
def scoredata(request):
    if request.method=="POST":
        body = json.loads(request.body)
        print("from scoredata",body)
        phno = body['phno'] if 'phno' in body else None
        agn= body['agn'] if 'agn' in body else None
        sub= body['sub'] if 'sub' in body else None
        dispo= body['dispo'] if 'dispo' in body else None
        contact= body['contact'] if 'contact' in body else None
        id= body['id'] if 'id' in body else None
        rec= body['rec'] if 'rec' in body else None
        up=datetime.now().date()

        print("test",id,rec,"POST from qsajax")
        if Score.objects.filter(qs_id=id).exists():
            print("in if",id)
            qs=Score.objects.filter(qs_id=id).update(agent=agn,direction=dispo,contacted_dt=contact,recordingfile=rec,phone=phno,sub=sub)
        else:
            print(id,"in else")
            qs=Score.objects.create(agent=agn,direction=dispo,contacted_dt=contact,recordingfile=rec,phone=phno,sub=sub,qs_id=id)
            qs.save()
        print("from here")
        return JsonResponse({"id":id,"status":200})

@api_view(['POST'])
def get_score(request):
    id = request.POST.get('id')
    s=Score.objects.filter(qs_id=id)
    serializer_data = ScoreSerializer(s,many=True).data
    return JsonResponse({'status':200,'data':serializer_data})

@api_view(['POST'])
@validate_bearer_token
def score(request):
    print("from function")
    if request.method == "POST":
        body = json.loads(request.body)
        print("here in post")
        id=body['id'] if 'id' in body else None
        m1=body['1st'] if '1st' in body else None
        m2=body['2nd'] if '2nd' in body else None
        m3=body['3rd'] if '3rd' in body else None
        m4=body['4rd'] if '4rd' in body else None
        m5=body['5th'] if '5th' in body else None
        m6=body['6th'] if '6th' in body else None
        m7=body['7th'] if '7th' in body else None
        m8=body['8th'] if '8th' in body else None
        m9=body['9th'] if '9th' in body else None
        total=body['tot'] if 'tot' in body else None
        got=body['got'] if 'got' in body else None
        per=body['per'] if 'per' in body else None
        ls=body['ls'] if 'ls' in body else None
        ls = ls.split(',')
        dt=datetime.now()
        print(ls)
        print(type(ls))
        q=Score.objects.filter(id=id)
        q.update(lastupdate=dt,gm1=m1,gm2=m2,gm3=m3,gm4=m4,gm5=m5,gm6=m6,gm7=m7,gm8=m8,gm9=m9,total=total,got=got,performance=per,m1=ls[0],m2=ls[1],m3=ls[2],m4=ls[3],m5=ls[4],m6=ls[5],m7=ls[6],m8=ls[7],m9=ls[8])
        
        print(m1,m2,m3,m4,m5,m6,m7,m8,m9,total,got,per,ls)
        return JsonResponse({"status":200})
    return JsonResponse({"status":400})