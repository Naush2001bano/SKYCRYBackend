from ..views_imports import *

# /////////////////////////Missedcall function starts/////////////////////////
@api_view(["POST"])
@validate_bearer_token
def missajax(request):
    miss=Inbound_log.objects
    m_ct=Inbound_log.objects.filter(status="No")
    com_ct=Inbound_log.objects.filter(status="Yes")
    nc_ct=Inbound_log.objects.filter(status="Ringing No Response")
    all_ct=Inbound_log.objects
    if request.method=="POST":
        getFilter=json.loads(request.body)
        filt = getFilter["filter"] if "filter" in getFilter else None
        sd=getFilter["sd"].rstrip() if "sd" in getFilter else None
        ed=getFilter["ed"].rstrip() if "ed" in getFilter else None
        order_fil = getFilter['date_fil'] if "date_fil" in getFilter else None
        sd=datetime.strptime(sd,'%d-%m-%Y')
        ed=datetime.strptime(ed,'%d-%m-%Y')
        if sd != ed:
            print(ed, type(ed))
            ed = ed + timedelta(days=1)

        sd=sd.strftime("%Y-%m-%d")
        ed=ed.strftime("%Y-%m-%d")

        if sd != "" and ed != "":

            if sd == ed:
                miss=Inbound_log.objects.filter(start__contains=ed)
                m_ct=m_ct.filter(start__contains=ed)
                com_ct=com_ct.filter(start__contains=ed)
                nc_ct=nc_ct.filter(start__contains=ed)
            else:
                miss=Inbound_log.objects.filter(start__range=[sd,ed])
                m_ct=m_ct.filter(start__range=[sd,ed])
                com_ct=com_ct.filter(start__range=[sd,ed])
                nc_ct=nc_ct.filter(start__range=[sd,ed])

        if order_fil == 'Ascending':
            miss=miss.order_by('-id')
        elif order_fil == 'Descending':
            miss=miss.order_by('id')
        
        all_ct=miss.count()
        if filt == "all":
            miss = miss.filter(status__isnull = False)
        elif filt == "completed":
            miss = miss.filter(status = "Yes")
        elif filt == "no":
            miss = miss.filter(status = "No")
        elif filt == "rnr":
            miss = miss.filter(status = "Ringing No Response")

        miss = miss[:150]
        m_ct=m_ct.count()
        com_ct=com_ct.count()
        nc_ct=nc_ct.count()
        print(miss,"misscall data")
        return JsonResponse({"miss":list(miss.values()),"m_ct":m_ct,"com_ct":com_ct,"nc_ct":nc_ct,"all_ct":all_ct})
    return JsonResponse({"status":600})


@api_view(["GET"])
@validate_bearer_token
def check_missedcall(request):
    ph=request.GET.get("phone")
    miss_id=request.GET.get("miss_id")
    print("check missed",ph)
    ph=ph[-10:]
    print(ph,"phhhhhhhh")
    try:
        add=AdditionalInfo.objects.values_list('lead_id',flat=True).filter(phone_no=ph).last()
        print(add,"asdasd")

        per=LeadDetails.objects.filter(Q(id = add) |Q(mobile_no=ph)|Q(additional_no=ph)).last()
        if per:
            per=per.id
            print("iffffffffffffffffffffffffffffff ",per)   
        else:
            per=LeadDetails.objects.create(mobile_no=ph,created_by="MissedCall")
            per.save()
            per = per.id
            print("in elseeeeeeeeeeeeeeeeeeeeeeeeeee",per)
        
        return JsonResponse({"status":200,"id":per,"ph":ph,"miss_id":miss_id})

    except Exception as e:
        print(e,"error")
    
        return JsonResponse({"status":200,"id":per,"ph":ph,"miss_id":miss_id})

    



# //////////////////Missedcall function  ends//////////////
