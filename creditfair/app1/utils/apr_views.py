from ..views_imports import *


def timeaddition(ls):
    if len(ls)==0:
        return "0:00:00"
    sumup = timedelta()
    for i in ls:
        (h, m, s) = i.split(':')
        d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        sumup += d
    return sumup

def timediffernece(t1,t2):
    format = '%H:%M:%S'
    difference = datetime.strptime(t1, format) - datetime.strptime(t2, format)
    return difference


def time_percent(time_in_str1,time_in_str2):
    time1 = timedelta(hours=int(time_in_str1.split(':')[0]), 
                minutes=int(time_in_str1.split(':')[1]), 
                seconds=int(time_in_str1.split(':')[2]))

    time2 = timedelta(hours=int(time_in_str2.split(':')[0]), 
                    minutes=int(time_in_str2.split(':')[1]), 
                    seconds=int(time_in_str2.split(':')[2]))
    
    # Calculate the total time elapsed in seconds
    total_seconds = (time2 - timedelta(hours=0)).total_seconds()
    
    # Calculate the time elapsed between the two time values
    time_elapsed = (time1 - timedelta(hours=0)).total_seconds()
    
    # Calculate the percentage of time
    percentage = round((time_elapsed / total_seconds) * 100)

    return percentage


def add_time_all(total_duration):
    total_seconds = total_duration.total_seconds()
    total_hours, remainder = divmod(total_seconds, 3600)
    total_minutes, total_seconds = divmod(remainder, 60)
    total_time = '{:02d}:{:02d}:{:02d}'.format(int(total_hours),int(total_minutes),int(total_seconds))
    return total_time

def convert_seconds(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, remaining_seconds)

def test(request):
    return render(request,"test.html")

def call_apr(request):
    return JsonResponse({"status":200})

def hangup_apr(request):
    return JsonResponse({"status":300})

def dispose_apr(request,id):
    try:
        print("dispoooooseeeeeeeaprrrrrrrrrrrr")
        current_date =datetime.now().date()
        extid = request.user.extension
        username = request.user.username
        forkey = id

        query = agentevents.objects.filter(agentname=username,call_time__icontains=current_date,personalkey_id=forkey).last()

        query2 = agent_performance.objects.filter(agentname=username,event_date= current_date).last()

        current_calltime = '0:00:00'
        current_hanguptime = '0:00:00'
        current_disposition_time = '0:00:00'
        if query:
            current_calltime = query.call_time.time().strftime("%H:%M:%S")
            current_hanguptime = query.hang_time.time().strftime("%H:%M:%S")
            current_disposition_time = query.disposed_time.time().strftime("%H:%M:%S")

            # /////////////////////getting talktime//////////////////  
            talktime = timediffernece(current_hanguptime,current_calltime)
            prev_talktime = query2.talk_time
            talktime_sumup = timeaddition([str(talktime),str(prev_talktime)])
            print(talktime_sumup,prev_talktime,talktime,"talktimeeeeeeeee")

            #//////////////////////getting wrap-up time////////////
            wrapup_time = timediffernece(current_disposition_time,current_hanguptime)
            prev_wrapup_time = query2.wrap_up
            wrapup_time_sumup = timeaddition([str(wrapup_time),str(prev_wrapup_time)])
            print(wrapup_time_sumup,prev_wrapup_time,wrapup_time,"wraptimeeee")
        
        query4 = agentevents.objects.filter(agentname=username,call_time__icontains=current_date).order_by('-id')

        query5 = break_details.objects.filter(agentname=username,break_end__icontains=current_date).last()

        flag = False
        idle_time_sumup = "0:00:00"
        inactive_hrs_sumup = "0:00:00"
        if query2.last_event == "call":
            prev_calltime = query4[1].disposed_time.time().strftime("%H:%M:%S")
            idletime = timediffernece(current_calltime,prev_calltime)
            prev_idletime = query2.idle_time
            idle_time_sumup = timeaddition([str(prev_idletime),str(idletime)])
            print(query2.last_event,idle_time_sumup,"lastttteventtttttcallllllll")
            flag = True

        elif query2.last_event == "break" :
            prev_breaktime = query5.break_end.time().strftime("%H:%M:%S")
            idletime = timediffernece(current_calltime,prev_breaktime)
            prev_idletime = query2.idle_time
            idle_time_sumup = timeaddition([prev_idletime,str(idletime)])
            print(query2.last_event,prev_breaktime,idletime,prev_idletime,idle_time_sumup,"lastttteventtttttbreakkk")
            flag = True

        elif query2.last_event == "login":
            login_time = query2.date_time_added.time().strftime("%H:%M:%S")
            inactive_hrs = timediffernece(current_calltime,login_time)
            prev_inactive_hrs = query2.nonactive_hrs
            inactive_hrs_sumup = timeaddition([str(inactive_hrs),prev_inactive_hrs])
            print(query2.last_event,prev_inactive_hrs,inactive_hrs,login_time,inactive_hrs_sumup)

        else:
            print("no event found")

        get_agent = agent_performance.objects.get(id=query2.id)
        if flag:
            get_agent.idle_time = idle_time_sumup
        else:
            get_agent.nonactive_hrs = inactive_hrs_sumup
            
        get_agent.last_event = "call"
        get_agent.talk_time = talktime_sumup
        get_agent.wrap_up  = wrapup_time_sumup

        get_agent.save()


        # sum and update login and tos hours
        get_agent2 = agent_performance.objects.get(id = get_agent.id)
        login_sum_ls = timeaddition([get_agent2.idle_time,get_agent2.wrap_up,get_agent2.talk_time,get_agent2.hold_hours,get_agent2.ringing_hrs,get_agent2.nonactive_hrs,get_agent2.break_hours])
        get_agent2.login_hours = login_sum_ls
        get_agent2.tos = timeaddition([get_agent2.idle_time,get_agent2.wrap_up,get_agent2.talk_time])

        print([get_agent2.idle_time,get_agent2.wrap_up,get_agent2.talk_time,get_agent2.hold_hours,get_agent2.ringing_hrs,get_agent2.nonactive_hrs,get_agent2.break_hours],login_sum_ls,"loginhoursss calculation")

        get_agent2.save()

    except Exception as e:
        print(e)


def login_apr(request):
    current_date =datetime.now().date()
    username = request.user.username
    firstname = request.user.first_name
    entry = datetime.now()
    query = agent_performance.objects.filter(agentname=username,event_date=current_date)
    if query.exists():
        print("exists")
        query.update(date_time_added=entry,last_event='login')
    else:
        agent_performance.objects.create(agentname=request.user.username,event_date=current_date,last_event='login',first_name=firstname)
        print("created")
    
    return JsonResponse({"status":200})

def logout_apr(request):
    username = request.user.username
    current_date =datetime.now().date()
    current_time =datetime.now().time().strftime("%H:%M:%S")

    query =  agent_performance.objects.filter(agentname=username,event_date=current_date)

    # login_time = "00:00:00"
    gap = "0:00:00"
    query_last_event = ""
    if query:
        query = query.last()
        query_last_event = query.last_event 
        print(query)
        print(query.last_event,query.login_hours,query.idle_time)
    
    if query_last_event == "login":
        prev_time = query.date_time_added.strftime("%H:%M:%S")
        print(prev_time,current_time)
        gap = timediffernece(current_time,prev_time)
        prev_non_active_hrs = query.nonactive_hrs
        gap_sum = timeaddition([str(gap),prev_non_active_hrs])
        agent_performance.objects.filter(id=query.id).update(nonactive_hrs=gap_sum)

    elif query_last_event == "call":

        call_query = agentevents.objects.filter(agentname=request.user.username,disposed_time__icontains=current_date).last()
        prev_time = call_query.disposed_time.time().strftime("%H:%M:%S")
        gap = timediffernece(current_time,prev_time)
        prev_idle_time = query.idle_time
        gap_sum = timeaddition([str(gap),prev_idle_time])
        print(prev_time,current_time,gap,"calllll")
        agent_performance.objects.filter(id=query.id).update(idle_time=gap_sum)

    elif query_last_event == "break":
        break_query = break_details.objects.filter(agentname=request.user.username,break_end__icontains=current_date).last()
        prev_time = break_query.break_end.time().strftime("%H:%M:%S")
        gap = timediffernece(current_time,prev_time)
        prev_idle_time = query.idle_time
        gap_sum = timeaddition([str(gap),prev_idle_time])
        print(gap,prev_time,prev_idle_time,current_time,"breakkkkkkk",gap_sum)
        agent_performance.objects.filter(id=query.id).update(idle_time=gap_sum)

    if query_last_event == "call" or query_last_event  == "break":
        prev_tos = query.tos
        tos_sumup = timeaddition([prev_tos,str(gap)])
        print(prev_tos,prev_tos,gap,"intossssssssss")
        agent_performance.objects.filter(id=query.id).update(tos=tos_sumup)
    # ////////////login hrs sumup
    login_hrs = query.login_hours 
    login_hrs_sumup = timeaddition([str(login_hrs),str(gap)])
    print(str(login_hrs),str(gap),"loginhrssssssssssss")
    agent_performance.objects.filter(id=query.id).update(login_hours=login_hrs_sumup,last_event="inactive")
    if request.user.user_level == 9 :
        User.objects.filter(username=request.user.username).update(is_loggedin=0,status='Not Ready',avgTT='',extension='')
    else:
        User.objects.filter(username=request.user.username).update(is_loggedin=0,status='Not Ready',mode="",avgTT='',extension='')


    return JsonResponse({"status":200})

@api_view(['POST'])
@validate_bearer_token
def apr_report_export(request):
    try:
        user_level_1_ls = User.objects.filter(user_level=1)
        direction_val = request.user.process
        break_details_query = infobreak.objects
        dispo_query = LogData.objects
        user_ls = agent_performance.objects
        read = agent_performance.objects

        print(user_level_1_ls,direction_val)
        user_list = []
        if request.user.user_level==9:
            user_list = User.objects.filter(assigned_to=request.user.id).values_list('username', flat=True)
        elif request.user.user_level==10:
            user_list=User.objects.filter(module=request.user.module,user_level=1).values_list('username', flat=True)
        else:
            user_list=User.objects.filter(username=request.user.username).values_list('username', flat=True)
        print(user_list,'userlist')



        # user_directions = []
        # if direction_val:
        #     user_level_1_ls=user_level_1_ls.filter(process=direction_val).values_list('username',flat=True)  
        #     print(user_level_1_ls,'userlevel1')
        # else:
        #     user_level_1_ls = user_level_1_ls.values_list('username',flat=True)

            # user_directions=user_level_1_ls.filter(process=direction_val)
        user_ls=user_ls.filter(agentname__in=user_list)
        print(user_list,user_ls,'userlsssssssssssssssssssssssssssssssssss')
        read=read.filter(agentname__in=user_list)
        print(read.count(),'readdddddddd' )
        break_details_query=break_details_query.filter(agentname__in=user_list)


        # print(direction_val)
        body = json.loads(request.body)
        username = request.user.username
        fd = body['apr_fdate'].rstrip() if 'apr_fdate' in body else None
        td = body['apr_tdate'].rstrip() if 'apr_tdate' in body else None
        # username = "admin"
        current_date = datetime.now().date()

        if fd != "" and td != "":
            fd = datetime.strptime(fd,'%d-%m-%Y')
            td = datetime.strptime(td,'%d-%m-%Y')
        if fd != td:
            td = td + timedelta(days=1)
        fd = fd.strftime("%Y-%m-%d")
        td = td.strftime("%Y-%m-%d")
        

        date_range = [fd,td]
        # query2 = dispositions_count.objects
        # dispo_query = LogData.objects.all().values_list('sub_disposition', flat=True).distinct().order_by('sub_disposition')
        
        dispo_query = dispo_query.all().values_list('sub_disposition', flat=True).distinct().order_by('sub_disposition')

        if fd == td:
            dispo_query = dispo_query.filter(contacted_dt__icontains=fd)
        else:
            dispo_query = dispo_query.filter(contacted_dt__range=date_range)
        
        # dispo_query = dispo_query.values_list('sub_disposition', flat=True).distinct().order_by('sub_disposition')
    

    

        # print(username,date_range,fd,td)

        if fd == td:
            user_ls = user_ls.filter(event_date__icontains=fd)
            read = read.filter(event_date__icontains=fd)
            break_details_query = break_details_query.filter(date__icontains=fd)
        else:
            user_ls = user_ls.filter(event_date__range=date_range)
            read = read.filter(event_date__range=date_range)
            break_details_query = break_details_query.filter(date__range=date_range)
            
        # else:
        #     user_ls = user_ls.filter(agentname=username)
        #     read = read.filter(agentname=username)
        #     break_details_query = break_details_query.filter(agentname=username)

        user_ls = user_ls.values_list('agentname', 'event_date').order_by('agentname')
        break_details_query =  break_details_query.values_list('name', flat=True).distinct().order_by('name')
        
        # print(user_ls,"lssssssssslssl")

        ls = []
        break_ls = []
        total_call_count = []
        dispo_dict={}
        break_dict={}

        print(break_dict,dispo_dict)

        for i in range(len(user_ls)):
            print(user_ls[i][1],"sdasa",user_ls[i][0])
            query = LogData.objects.filter(Q(caller_name=user_ls[i][0])|Q(attempted_by=user_ls[i][0]),contacted_dt__icontains=user_ls[i][1])
            total_call_count.append(len(query))
            dispo_dict = dispo_dict.fromkeys(dispo_query,0)
            for i in query:
                dispo_dict[i.sub_disposition] += 1
                
            ls.append(dispo_dict)

        for i in range(len(user_ls)):
            print(user_ls[i][1],"sdasa",user_ls[i][0])
            inbk = infobreak.objects.filter(agentname=user_ls[i][0],date=user_ls[i][1]).order_by('name')
            break_dict = break_dict.fromkeys(break_details_query,"00:00:00")
            # query = LogData.objects.filter(caller_name=user_ls[i][0],contacted_dt__icontains=user_ls[i][1])
            for i in inbk:
                break_dict[i.name] = i.total
                
            break_ls.append(break_dict)

        print(break_dict,"breskkskskdictttttt",break_ls)

        # print(ls,"dictsssss")

        output = io.BytesIO()

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data') 

        row_num = 0

        columns = ["Agent Name","First Name","Date","Login Hours","Idle hours","Talk Hours","Wrap-up Hours","Break Hours","TOS (Time on system)","Non-active Hours"]

        col_num_value = 0
        col_num_key = 0
        dispo_col_num_value = 0
        for col_num in range(len(columns)):
            col_num_key += 1
            col_num_value += 1
            dispo_col_num_value += 1
            ws.write(row_num, col_num, columns[col_num])


        # //////////// break keys start////////
        for col_num in range(len(break_details_query)):
            ws.write(row_num,col_num_key,break_details_query[col_num])
            col_num_key+=1
            col_num_value += 1
        # //////////// break keys end////////
        
        # //////////total calls key//////////
        ws.write(row_num,col_num_key,"Total Calls")
        col_num_key += 1
        col_num_value += 1
        # //////////total calls key//////////

        #////// disposition keys start///////
        # for col_num in dict:
        for col_num in range(len(dispo_query)):
            ws.write(row_num,col_num_key,dispo_query[col_num])
            col_num_key+=1

        #////// disposition keys end///////

        rows = read.values_list("agentname","first_name","event_date","login_hours","idle_time","talk_time","wrap_up","break_hours","tos","nonactive_hrs").order_by('agentname')

        # ///////////////////////////agent performance values append in excel//////////////////////////
        print(rows,"rowssssssssssssssssssssssssssssssagenttttttttttt")
        row_num1 = 0
        for row in rows:
            row_num1 += 1
            for col_num in range(len(row)):
                data=str(row[col_num]).replace("nan"," ")
                data=data.replace("None"," " )
                ws.write(row_num1,col_num,data)
        # ///////////////////////////agent performance values append in excel//////////////////////////

        # //////////////////// subdisposition append in excel////////////
        for row in range(len(ls)):
            row_num += 1
            temp_col_num = col_num_value
            ws.write(row_num,col_num_value-1,total_call_count[row])
            for col_num in ls[row]:
                data=str(ls[row][col_num]).replace("nan"," ")
                data=data.replace("None"," ")
                ws.write(row_num,temp_col_num,ls[row][col_num])
                print(row_num,temp_col_num,ls[row][col_num],"subssssssssss")
                temp_col_num += 1  
        # //////////////////// subdisposition append in excel //////////// 

        # ///////////////////// break append in excel////////////
        row_num2 = 0 
        for i in range(len(break_ls)):
            row_num2 += 1
            temp_col_num2 = dispo_col_num_value
            for col_num in break_ls[i]:
                data=str(break_ls[i][col_num]).replace("nan"," ")
                data=data.replace("None"," ")
                ws.write(row_num2,temp_col_num2,break_ls[i][col_num])
                print(row_num2,temp_col_num2,break_ls[i][col_num],"breaksssssssssss")
                temp_col_num2 += 1
        # ///////////////////// break append in excel//////////////////

        wb.save(output)
        output.seek(0)
        response = FileResponse(output, content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        return response
    except Exception as e:
        print(e)
        return JsonResponse({"status": 500, "message": "Error generating Excel file"})
    return JsonResponse({"status":200})

def break_events(request):
    if request.method == "POST":
        username =request.user.username
        event=request.POST.get("event")
        b_type=request.POST.get("type")
        break_id = request.POST.get('break_id')

        print(b_type,event,"breaksssss")

        current_dt = datetime.now()
        current_d = datetime.now().date()
        current_t = current_dt.time().strftime("%H:%M:%S")

        if event == "start": 
            break_query = break_details.objects.create(agentname=username,break_start=current_dt,break_end = current_dt,break_name=b_type)
            break_query.save()

            return JsonResponse({"status":200,"break_id":break_query.id})

        elif event == "end":
            b_start =  break_details.objects.filter(id=break_id).last()
            b_start_time = b_start.break_start.time().strftime("%H:%M:%S")
            total_break_time = timediffernece(current_t,b_start_time) 
            break_details.objects.filter(id = b_start.id).update(break_end=current_dt,break_total=total_break_time)

            # ////////////////////////// insert the sum up of break in agentperformance table///////////////////
            agn_p=agent_performance.objects.filter(agentname=request.user.username,event_date=current_d).last()

                # //////////////////////gap between login and break time////////////////////
            gap="00:00:00"
            if agn_p.last_event == "login":
                prev_time = agn_p.date_time_added.time().strftime("%H:%M:%S")
                gap = timediffernece(b_start_time,str(prev_time))
                prev_nonactive_hrs = agn_p.nonactive_hrs
                nonactive_hrs_sumup = timeaddition([str(gap),prev_nonactive_hrs])
                agent_performance.objects.filter(id=agn_p.id).update(nonactive_hrs=nonactive_hrs_sumup)

            elif agn_p.last_event == "call":
                query = agentevents.objects.filter(agentname=request.user.username,disposed_time__icontains=current_d).last()
                prev_time = query.disposed_time.time().strftime("%H:%M:%S")
                prev_idle_time = agn_p.idle_time
                gap = timediffernece(b_start_time,str(prev_time))
                idle_time_gap_sum = timeaddition([str(gap),prev_idle_time])
                agent_performance.objects.filter(id=agn_p.id).update(idle_time=idle_time_gap_sum)
           
            elif agn_p.last_event == "break":
                query2 = break_details.objects.filter(agentname=request.user.username,break_end__icontains=current_d).order_by('-id')
                print(query2,"qqqqqqq2222222222")   
                prev_end_time = query2[1].break_end.time().strftime("%H:%M:%S")
                current_start_time = query2.first().break_start.time().strftime("%H:%M:%S")
                prev_idle_time=agn_p.idle_time
                gap = timediffernece(str(current_start_time),str(prev_end_time))
                idle_time_gap_sum = timeaddition([str(gap),prev_idle_time])
                print([str(gap),prev_idle_time],"breakkkkkkinggg")
                agent_performance.objects.filter(id=agn_p.id).update(idle_time=idle_time_gap_sum)
            
                # ////////////login hrs sumup
            login_hrs = agn_p.login_hours 
            login_hrs_sumup = timeaddition([str(login_hrs),str(total_break_time),str(gap)])

                #//////////////////////// breakhrs sumup//////////////////
            prev_break_hrs = agn_p.break_hours
            break_hrs_sumup = timeaddition([str(prev_break_hrs),str(total_break_time)])
            print([str(login_hrs),str(total_break_time)],[str(prev_break_hrs),str(total_break_time)])

            get_agnp = agent_performance.objects.get(id=agn_p.id)

            get_agnp.login_hours = login_hrs_sumup
            get_agnp.break_hours = break_hrs_sumup
            get_agnp.last_event = "break"
            get_agnp.tos = timeaddition([get_agnp.idle_time,get_agnp.talk_time,get_agnp.wrap_up])

            get_agnp.save()

            # agent_performance.objects.filter(id=agn_p.id).update(login_hours=login_hrs_sumup,break_hours=break_hrs_sumup,last_event="break")

            # ///////////////////insert the sum up of break in infobreak table///////////////////////
            ib_query =  infobreak.objects.filter(agentname=request.user.username,date=current_d,name=b_type).last()
            print(ib_query)
            if not ib_query:
                infobreak.objects.create(agentname=request.user.username,date=current_d,name=b_type,total=total_break_time)
            else:
                info_prev_break_hrs = ib_query.total
                info_break_sumup = timeaddition([str(info_prev_break_hrs),str(total_break_time)])
                print(info_break_sumup,"info_breakkksumupppp")
                infobreak.objects.filter(id=ib_query.id).update(total=info_break_sumup)

            return JsonResponse({"status":202})

        print(event,b_type)
       
    return JsonResponse({"status":300})
 
