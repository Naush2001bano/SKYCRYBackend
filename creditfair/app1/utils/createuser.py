from .. views_imports import *

# ////////////////////create user views starts////////////////////
@api_view(["POST"])
@validate_bearer_token
def create_user_data(request):
    user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
    print('createuser panel called')
    data=User.objects.all().filter(user_level=1,module=request.user.module,username__in=user_list)
    return JsonResponse({"data":list(data.values())})


@api_view(["POST"])
@validate_bearer_token
def savedata(request): 
    if request.method=="POST":
        new_data=json.loads(request.body)
        print("its posted all",new_data)
        name=new_data["name"] if 'name' in new_data else None
        passw=new_data["password"] if 'password' in new_data else None
        j_date=new_data["joindate"] if 'joindate' in new_data else None
        area = new_data["area"] if 'area' in new_data else None
        pincode = new_data["pincode"] if 'pincode' in new_data else None
        travel = new_data["travel"] if 'travel' in new_data else None
        process = request.user.process
        module= request.user.module
        print(module,'moduleee') 
        query=User.objects.filter(user_level='1',username__icontains='CRF').last()
        print(query,'queryyyyyyyyyyyyyyyyy')
        if query:
            prev_user_id= query.username
        else:
            prev_user_id="LOC000"
            

        i=int(prev_user_id[3:])+1
        newid = f"LOC{i:03}" 
        print(newid)
        
        print(name,passw,j_date)
        # query=usercreatee.objects.filter("")

        User.objects.create_user(first_name=name,password=passw,date_joined=j_date,user_level='1',user_created_by=request.user.username,process=process,username=newid,status="1",area=area,pincode=pincode,travelby=travel,assigned_to=request.user.id,module=module)

        stud=User.objects.values()
        # print(stud)
        dataa=list(stud)
        msg='User Created Sucessfully'
        return JsonResponse({'status':'save','dataa':dataa,'idd':newid,'msg':msg})
    else:
        msg = "Something Went Wrong"
        return JsonResponse({'status':0})


@api_view(["POST"])
@validate_bearer_token
def update_pas(request):
    if request.method == 'POST':
        update_rec=json.loads(request.body)
        id = update_rec['id']
        print(id,'idddddddddd')
        us  = User.objects.get(id=id)
        us.set_password('1234')
        us.save()
        print(us)
        msg='Password Reset Sucessfully as 1234'
    return JsonResponse({'status':200,'msg':msg})


@api_view(["POST"])
@validate_bearer_token
def getuser_details(request):
    data=User.objects
    if request.method == "POST":
        get_data=json.loads(request.body)
        id = get_data['id']
        print(id,'iddddddddddddddddddddddddd')
        data=data.filter(id=id)
    return JsonResponse({'status':200,'data':list(data.values())})


@api_view(["POST"])
@validate_bearer_token
def update_user(request):
    data=User.objects
    msg=''
    if request.method == 'POST':
        updated_data=json.loads(request.body)
        print(updated_data,"all info for an update")
        id = updated_data['id'] if "id" in updated_data else None
        name = updated_data['name'] if "name" in updated_data else None
        joindate = updated_data['joindate'] if "joindate" in updated_data else None
        process = updated_data['process'] if "process" in updated_data else None
        area = updated_data['area'] if "area" in updated_data else None
        pincode = updated_data['pincode'] if "pincode" in updated_data else None
        travel = updated_data['travel'] if "travel" in updated_data else None
        if id :
            data=data.filter(id=id).update(first_name=name,date_joined=joindate,process=process,area=area,travelby=travel,pincode=pincode)
            msg= 'Data Updated Sucessfully'
            return JsonResponse({'status':200,'msg':msg})
        msg="Updated User Id not found"
        return JsonResponse({'status':404,'msg':msg})




# function to update the permission
@api_view(["POST"])
@validate_bearer_token
def showstatus(request):
    data=User.objects
    if request.method=='POST':
        get_data=json.loads(request.body)
        print(get_data,"show status")
        listid = get_data['lstid'] if "lstid" else None
        an = get_data['an'] if "an" else None
        print('reteretere',listid,an)
        data=data.filter(id=listid).update(permission=an)
        a=User.objects.filter(id=listid).last()
        if an == "0":
            # Valid_token.objects.filter(userid=a.username).delete()
            User.objects.filter(id=listid).update(is_loggedin=0)
        msg="Action Updated Successfully"
    return JsonResponse({'status':200,"msg":msg})


# function for change password on user level
@api_view(["POST"])
@validate_bearer_token
def change_pas(request):
    id = request.user.id
    if request.method == 'POST':
        c_pass=request.POST.get('pass')
        conf_pass=request.POST.get('conf_pass')
        print('valuessssssssssss',c_pass,conf_pass)
        if (len(c_pass) > 1 and len(conf_pass) > 1) and (c_pass == conf_pass):
            us  = User.objects.get(id=id)
            us.display_pass = conf_pass
            us.set_password(conf_pass)
            us.is_loggedin = "0"
            us.save()
            print('if')
            msg ='Password Changed'
            logout(request)
            # redirect('/login')
            return JsonResponse({'status':200,'msg':msg})
        else:
            print('else')
            msg ='Something Went Wrong'
            return JsonResponse({'status':300,'msg':msg})
    return JsonResponse({'status':200})

        
