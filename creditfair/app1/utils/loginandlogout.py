from ..views_imports import *



@api_view(["POST"])
def login_user_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        username = request.data['username']
        password = request.data['password']
        extension = request.data['extension']
        force = request.data['force']

        entry=datetime.now()
        dt=datetime.now().time()
        cr_date = datetime.now().date()

        print(cr_date,username,"jasihdahdhadakshdalhdlahdsadatetetetet")

        if not User.objects.filter(username=username).exists():
            return JsonResponse({'status':301})
        
        if force:
            User.objects.filter(username=username).update(is_loggedin=0)


        query = User.objects.get(username=username)
        

        user = authenticate(username=username,password=password)
        if user is not None:

            if user.user_level == 1 and (entry.time() < time(7, 59) or entry.time() > time(19,1)) and process == 'Outbound':
                print("not in shift time",entry.time())
                return JsonResponse({'status':306,"message":"Can't login right now"})
            
            if query.is_loggedin == "1":
                print(query,"qeryyyyy logedddddddd iiiiiiinnnnnn")
                return JsonResponse({'status':500,'message':"User Already Logged in"})

            if extension and user.user_level == 1:
                extLoggedin = User.objects.filter(extension=extension).exclude(username=username).last()
                if extLoggedin:
                    print(extLoggedin.username,'extension logged in')
                    userwithext = extLoggedin.username
                    return JsonResponse({'status':406,'username':userwithext})

            if query.permission == 0:
                return JsonResponse({'status':700,'message':"Sorry You are not allowed to login"})

            

            last_date = user.last_login

            token, created = Token.objects.get_or_create(user=user)


            login(request,user)
            if last_date and last_date.date()!= cr_date:
                User.objects.filter(username=username).update(extension=extension,is_loggedin=1,event=dt,status="Not Ready",avgTT="",mode="",calls=0,contacted=0,noncontacted=0)
            else:
                 User.objects.filter(username=username).update(extension=extension,is_loggedin=1,event=dt,status="Not Ready")

            LoginHistory.objects.create(username=username,logdt=entry,event="LOGIN")
            # login_apr(request)
            return JsonResponse({'status':200,'token':token.key})

        print(username,password,"isidipssss")
    return JsonResponse({"status":400})

@api_view(["GET"])
@validate_bearer_token
def logoutuser(request):
    print(request.user.username)
    try:
        dt = datetime.now()
        LoginHistory.objects.create(username=request.user.username,logdt=dt,event="LOGOUT")
        token = Token.objects.filter(user_id=request.user.id)
        token.delete()
        # logout_queue(request)
        # logout_apr(request)
        logout(request)
        return JsonResponse({'status':200})
    except Exception as e:
        print(e)
        return JsonResponse({"status":400})


@api_view(["GET"])
@validate_bearer_token
def get_user_info(request):
    user = User.objects.filter(id=request.user.id)
    return JsonResponse({"status":200,"user":list(user.values())})

