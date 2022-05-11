from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
from django.core.files.storage import FileSystemStorage
from freelance.local_settings import url

def index(request):
    return render(request,'jobpoint_user/index.html')

def dashboarduser(request):
    msg=""
    if 'username' in request.session:
        username=request.session['username']
        job = f'{url}user_job_list'
        searchjob = f'{url}jobsearch'
        make_praposal = f'{url}make_praposal' 
        notify = f'{url}notification'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        data={
            "username":request.session['username']
        }
        response = requests.post(url=job,headers=token,json=data)
        print(response.json(),"@@@@@@@@@@@@@@@@@@@@@@@@@@")
        find = response.json()
        # notification/////////////////////

        Ndata={
             
            "username":username
        }
        response_notify = requests.get(url=notify,headers=token,json=Ndata)
        
        view_notification = response_notify.json()
        request.session['view_notification'] = view_notification

        # response = requests.get(url=job)
        # find = response.json()
        # print(find,")))))))")
        
        if request.method == 'POST':
            msg = ""
            search_key = request.POST.get('search')
            print(search_key)
            token={
                'Authorization': f"Token {request.session['user_token']}"
              }
            data = {
                "search":search_key
            }
            response_ser = requests.get(url=searchjob,headers=token,params=data)
          
            if response_ser.status_code==200:
                want = response_ser.json()
                print(want,"LLLLL")
                return render(request,'jobpoint_user/userboard.html',{"username":username,"search":want})
            else:
                msg = "not found"
                return HttpResponse("not found .....")
      
        return render(request,'jobpoint_user/userboard.html',{"username":username,"data":find,"notify":view_notification})

    else:
        return redirect('login')

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)    

def qualificaton(request):
    if 'username' in request.session:
        username=request.session['username']
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        qual = f'{url}userqual'
        print(qual)
        if request.method == 'POST':
            user = request.session['username']
           
            print("user",user)
            recent_degree = request.POST.get('degree')
            cpi = request.POST.get('cpi')
            university = request.POST.get('university')
            passing_year = request.POST.get('passing_year')
            about = request.POST.get('about')
            print("OPOP",user)
            data = {
                "username":user,
                "recent_degree":recent_degree,
                "cpi":cpi,
                "passing_year":passing_year,
                "university":university,
                "about":about
                }
            print(data)
            response = requests.post(url=qual,headers=token,json=data)
            print(response)
            if response.status_code==200:
                return redirect('showexp')
            else:
                return redirect('dashboarduser')
        return render(request,'jobpoint_user/qualification.html',{"username":username,"notify":request.session['view_notification']})
    else:
        return redirect('login')
    
#@cache_control(no_cache=True, must_revalidate=True, no_store=True)    

def showexp(request):
    if 'username' in request.session:
        username=request.session['username']
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        print(username)
        exp = f'{url}userexp'
        qual = f'{url}userqual'
        search = f'{url}jobsearch'

        print(exp,"__________________")
        data = {
            "username":username
        }
        
        response = requests.get(url=exp,headers=token,json=data)
       
        
        response_qual = requests.get(url=qual,headers=token,json=data)

        find_qual = response_qual.json()
        # print(find_qual)
        
        if response.status_code==200 and response_qual.status_code==200 :
           return render(request,'jobpoint_user/expierence.html',{"username":username,"data":response.json(),"res":find_qual,"notify":request.session['view_notification']})
        else:
            return redirect('dashboarduser')
       
        

    else:
        return redirect('login')
    
##@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
    
def update(request,id):
    if 'username' in request.session:
        #print(id, "???")
        username=request.session['username']
        update = f'{url}userqualificationview/{id}'
        updateuser = f'{url}userqual/{id}'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        data={
        "username":request.session['username']
        }
        response=requests.get(url=update,headers=token,json=data)
       
        if response.status_code==200:   
            getdata = response.json()
            print(getdata,"hjhjhhjh")
            if request.method == 'POST':
                print("calleddddd")
                recent_degree=request.POST.get('degree')
                cpi=request.POST.get('cpi')
                passing_year=request.POST.get('passing_year')
                university=request.POST.get('university')
                about=request.POST.get('about')
                data = {
                    "recent_degree":recent_degree,
                    "cpi":cpi,
                    "passing_year":passing_year,
                    "university":university,
                    "about":about
                }
                print(data,"AAAAA")
                response_update = requests.put(url=updateuser,headers=token,json=data)
                print(response_update,"mmmmmmmmmm")
                if response_update.status_code==200:
                    return redirect('showexp')
                else:
                    return HttpResponse("no")
           
            return render(request,'jobpoint_user/updatequal.html',{"username":username,"data":getdata,"notify":request.session['view_notification']})
        else:
            return render(request,'jobpoint_user/updatequal.html',{"username":username,"data":getdata,"notify":request.session['view_notification']})
    else:
        return redirect('login')

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)    

def updateexp(request,id):
    if 'username' in request.session:
      
        username=request.session['username']
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        getpost = f'{url}user/{id}'
        updateuser = f'{url}userexp/{id}'
        data={
        "username":request.session['username']
        }
        response=requests.get(url=getpost,headers=token)
       
        if response.status_code==200:   
            getdata = response.json()
            print(getdata,"?????????????")
            if request.method == 'POST':
                print("calleddddd")
                Job=request.POST.get('pjob')
                compny=request.POST.get('pcomp')
                expirence=request.POST.get('eyear')
                
                about=request.POST.get('about')
                data = {
                    
                    "previous_job":Job,
                    "previous_compny":compny,
                    "experience_year":expirence,
                    "about":about
                }
                print(data,"AAAAA")
                response_update = requests.put(url=updateuser,headers=token,json=data)
                print(response_update,"mmmmmmmmmm")
                if response_update.status_code==200:
                    return redirect('showexp')
                else:
                    return HttpResponse("no")
           
            return render(request,'jobpoint_user/updateexp.html',{"username":username,"data":getdata,"notify":request.session['view_notification']})
        else:
            return redirect('dashboarduser')
    else:
        return redirect('login')
    



#@cache_control(no_cache=True, must_revalidate=True, no_store=True)    

def addexpirence(request):
    if 'username' in request.session:
        username=request.session['username']
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        exp = f'{url}userexp'

        if request.method == "POST":
            user = request.session['username']
            job = request.POST.get('pjob')
            compny = request.POST.get('pcomp')
            experience = request.POST.get('eyear')
            about = request.POST.get('about')
            data = {
                "username":user,
                "previous_job": job,
                "previous_compny": compny,
                "experience_year": experience,
                "about": about
            }
            print(data)
            response = requests.post(url=exp,headers=token,json=data)
            print(response)
            if response.status_code==200:
                return redirect('showexp')
            else:
                return redirect('dashboarduser')
        return render(request,'jobpoint_user/addexpirence.html',{"username":username,"notify":request.session['view_notification']})
    else:
        return redirect('login')

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
  
def makepraposal(request,id):
    if 'username' in request.session:
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        username=request.session['username']
        praposal = f'{url}make_proposal'
        get_price=f'{url}jobdetails'
        price_data={
                    "username":username,
                    "job":id
        }
        price_resposnse=requests.post(url=get_price,headers=token,json=price_data)
        price_resposnse=price_resposnse.json()['price']
        print(praposal,"----------")
        if request.method == "POST":
            print("ooooooooo")
            description = request.POST.get('description')
            print(description)
            price = request.POST.get('price')
            data = {
                "job":id,
                "username":username,
                "discription":description,
                "price":price,
                
            }
            print(data)
            response = requests.post(url=praposal,headers=token,json=data)
            print(response.status_code,"@@@@@@@@@@@@")
          
            if response.status_code==200:
                msg = "your proposal has been send"
                messages.info(request,msg)
                return redirect('dashboarduser')
                # return render(request,'jobpoint_user/praposal.html',{"username":username,"notify":request.session['view_notification'],"pro_price":price_resposnse})
            else:
                msg = "your proposal has not been send"
                messages.info(request,msg)
                return redirect('dashboarduser')
                # return render(request,'jobpoint_user/praposal.html',{"username":username,"notify":request.session['view_notification'],"pro_price":price_resposnse})
        return render(request,'jobpoint_user/praposal.html',{"username":username,"pro_price":price_resposnse})
    else:
        return redirect('login')

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)       
def editprofileuser(request):
    if 'username' in request.session:
        urls=f'{url}user_details'
        
        getskill = f'{url}skill_list'

        addskill = f'{url}add_user_skill'
        
        token={
            'Authorization': f"Token {request.session['user_token']}"
            
        }
        data={
                    "username":request.session['username']
                }
        response_skill = requests.get(url=getskill,headers=token)
        viewskill = response_skill.json()
        response=requests.post(urls,headers=token,json=data)
        response_data={
                    "first_name":response.json()["first_name"],
                    "img_link":response.json()["img_link"],
                    "last_name":response.json()['last_name'],
                    "username":response.json()['username'],
                    "about":response.json()['about'],
                    "email":response.json()['email'],
                    "notify":request.session['view_notification'],
                    "skill_data":viewskill,
                    "mobile":response.json()['mobile'],
                    "user_skill" : [i['name'] for i in response.json()['skill']]
        }
        print(response_data)
        if request.method=='POST':
            skill_list=request.POST.getlist('checks[]')
            skill_data={
                    "username":request.session['username'],
                    "skill_list":skill_list
            }
            add_skill_res=requests.post(url=addskill,headers=token,json=skill_data)
            print(viewskill,"?????????????")
            
            token={
                    'Authorization': f"Token {request.session['user_token']}"
                    
                }
            data={
                    "username":request.session['username']
                }
            response=requests.post(urls,headers=token,json=data)
            print(response.json(),"!!!!!")
            edit_url=f'{url}edit_profile'
            token={
                'Authorization': f"Token {request.session['user_token']}"
            }
            if response.status_code==401:
                return redirect("dashboarduser")
            else:
                first_name=request.POST.get('fs_name')
                last_name=request.POST.get('lastname')
                about=request.POST.get('about')
                mobile=request.POST.get('mobile')
                user_name = request.session['username']
                addskill = request.POST.getlist('check[]')
                edit_data={
                    "first_name":first_name,
                    "img_link":response.json()["img_link"],
                    "last_name":last_name,
                    "username":user_name,
                    "about":about,
                    "mobile":mobile
                    }
                edit_response=requests.put(url=edit_url,headers=token,json=edit_data)
                if edit_response.status_code==200:
                    messages.info(request,'Profile has been updated')
                    return redirect('editprofileuser')
                else:
                    print(edit_response.json()['msg'])
                    
        return render(request,"jobpoint_user/editprofile.html",response_data)
    else:
        return redirect("login")

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)    

def userupload(request):
    if 'username' in request.session:
        if request.method=="POST":
            filextension=['jpg','jpeg','png']
            urls=f'{url}edit_profile'
            token={
                    'Authorization': f"Token {request.session['user_token']}"
                }
            uploaded_filename = request.FILES['document']
            filename_new=uploaded_filename.name
            filename_new=filename_new.replace(" ","_")
            fs=FileSystemStorage()
            fs.save(uploaded_filename.name,uploaded_filename)
            if filename_new.split('.')[-1] in filextension:
                fs.save(filename_new,uploaded_filename)
                data={
                    "username":request.session['username'],
                    "img_link":f'/static/media/{filename_new}'
                }
                response=requests.put(url=urls,headers=token,json=data)
                return redirect('editprofileuser')
            else:
                messages.info(request,'Invalid Image Format')
                return redirect('upload')
        return render(request,'jobpoint_user/upload.html')
    else:
        return redirect('login')

def like(request,id):
    if 'username' in request.session:
        username=request.session['username']
        like_url=f'{url}like_job/{id}'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        print(like_url)
        data={
            
            "username":username
        }
        response=requests.post(url=like_url,headers=token,json=data)
        print(response,")()(())")
        if response.status_code==200:
            return redirect('dashboarduser')
        else:
            return redirect('showexp')
    else:
        return redirect("login")

def dislike(request,id):
    if 'username' in request.session:
        username=request.session['username']
        dislike_url=f'{url}dislike_job/{id}'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        print(dislike_url)
        data={
            
            "username":username
        }
        response=requests.post(url=dislike_url,headers=token,json=data)
        print(response,")()(())")
        if response.status_code==200:
            return redirect('dashboarduser')
        else:
            return redirect('showexp')
    else:
        return redirect('login')
        
def user_logout(request):
    if 'username' in request.session:
        urls=f'{url}logout'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        data={
                "username":request.session['username']
        }
        response=requests.post(url=urls,headers=token,json=data)
        print(response, "??")
        if response.status_code==200:
            del request.session['username']
            return redirect('login')
        else:
            messages.info(request,"could'nt logout")
            return redirect("dashboarduser")
    else:
        return redirect('login')

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)    

def notification_view(request):
    if 'username' in request.session:
        username=request.session['username']
        notify_url=f'{url}notification'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        print(notify_url)
        data={
             "token":request.session['user_token'],
            "username":username
        }
        print(data, ">>>>>")
        response = requests.get(url=notify_url,headers=token,json=data)
        print(response, "????")
        find_data = response.json()
        print(find_data,"kkkkkkk")
        if response.status_code==200:
            # msg = "this is template"    
            return render(request,'jobpoint_user/notification_details_show.html',{"username":username,"data":response.json(),"notify":find_data})
        else:
          
            return HttpResponse("did't get data")
            
    else:       
        return redirect('login')
    
   
                        
def deletenotification(request,id):
    if 'username' in request.session:
        notify_url= f"{url}delete_notify/{id}"
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        print(notify_url,")))))")
        response = requests.delete(url= notify_url,headers=token) #url= notify_url
        print(response)
        if response.status_code == 200:
            msg = "data deleted"
            return redirect('notify')
            
        else:
            msg = "not deleted"
            return HttpResponse(msg)
            
    else:       
        return redirect('login')
            
            

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)    

def project_status(request):
    if 'username' in request.session:
        username=request.session['username']
        status_url= f"{url}showstatus"
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        data = {
            
            "username":username
        }
        response = requests.get(url=status_url,headers=token,json=data)
        view_status = response.json()
        if response.status_code==200:
            # msg = "this is template"    
            return render(request,'jobpoint_user/project_status.html',{"username":username,"status":view_status,"notify":request.session['view_notification']})
        else:
          
            return HttpResponse("status not show")
            
    else:       
        return redirect('login')
#@cache_control(no_cache=True, must_revalidate=True, no_store=True)    

def  project_status_update(request,id):
    if 'username' in request.session:
        status_url= f"{url}showstatus/{id}"
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        if request.method=="POST":
            projectstatus  =  request.POST.get('status')
            data = {
                #  "token":request.session['user_token'],
                 "status":projectstatus
                }
                    

            response = requests.put(url= status_url,headers=token, json=data)

            print(response)

            if response.status_code ==200:
                return redirect('projectstatus')
            else:
                return HttpResponse("not updated")

        return render(request,'jobpoint_user/status_update.html',{"username":request.session['username']})                     
    else:
        return redirect('login')    



def deletestatus(request,id):
    if 'username' in request.session:
        delete_url= f"{ url}showstatus/{id}"
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        print(delete_url,")))))")
        response = requests.delete(url= delete_url,headers=token) #url= notify_url
        print(response)
        if response.status_code == 200:
            msg = "data deleted"
            return redirect('projectstatus')
            
        else:
            msg = "not deleted"
            return HttpResponse(msg)
            
    else:       
        return redirect('login')



#@cache_control(no_cache=True, must_revalidate=True, no_store=True)    

def userchatbox(request,id=None):
    if 'username' in request.session:
        if request.method == 'POST':
            msg = request.POST['msg']
            msg_post_url = f'{url}message_post'
            token={
                'Authorization': f"Token {request.session['user_token']}"
            }
            data={
                "msg":msg,
                "reciever":request.session['msg_reciever_id'],
                "username":request.session['username']
            }
            response=requests.post(url=msg_post_url,headers=token,json=data)
            if response.status_code == 200:
                pass
            else:
                print(response)
            id = request.session['msg_reciever_id']
            return redirect('userchatbox_id',id)    
        #chatlist
        urls=f'{url}chat_list'
        token={
                'Authorization': f"Token {request.session['user_token']}"
            }
        data={
            "username":request.session['username']
        }
        response=requests.post(url=urls,headers=token,json=data)

        #msg_counter
        msg_counter_url=f'{url}message_counter'
        token={
                'Authorization': f"Token {request.session['user_token']}"
            }
        data={
            "username":request.session['username']
        }
        msg_counter_response = requests.post(url=msg_counter_url,headers=token,json=data)

        sender_list=[]
        rec_list=[]
        for i in response.json():
            if i['sender']['username'] != request.session['username']:
                if i['sender'] not in sender_list:
                    sender_list.append(i['sender'])
            if i['reciever']['username'] != request.session['username']:
                if i['reciever'] not in rec_list:
                    rec_list.append(i['reciever'])
        join_list = sender_list+rec_list
        user_unique_list = [dict(y) for y in set(tuple(x.items()) for x in join_list)]
        if id == None:
            try:
                id = user_unique_list[0]['id']
                img_link = user_unique_list[0]['img_link']
                first_name = user_unique_list[0]['first_name']
                user_name=user_unique_list[0]['username']
                request.session['msg_reciever_id'] = id
            except:
                img_link=None
                first_name=None
                user_name=None

        else:

            temp_list = [i['id'] for i in user_unique_list]
            if id not in temp_list:
                request.session['msg_reciever_id'] = id
                get_user_detail_url = f'{url}user_details_id/{id}'
                token={
                    'Authorization': f"Token {request.session['user_token']}"
                    }
                data={
                    "username":request.session['username']
                    }                
                get_user_detail_response = requests.post(url=get_user_detail_url,headers=token,json=data)
                img_link = get_user_detail_response.json()['img_link']
                first_name = get_user_detail_response.json()['first_name']
                user_name = get_user_detail_response.json()['username']

            else:
                clear_msg_count_url =f'{url}clear_message_count'
                token={
                    'Authorization': f"Token {request.session['user_token']}"
                    }
                data={
                    "username":request.session['username'],
                    "sender":id
                    }
                clear_msg_count_response = requests.post(url=clear_msg_count_url,headers=token,json=data)
                request.session['msg_reciever_id'] = id
                
                for i in response.json():
                    if i['sender']['username'] == request.session['username']:
                        if i['reciever']['id'] == id:
                            img_link = i['reciever']['img_link']
                            first_name = i['reciever']['first_name']
                            user_name = i['reciever']['username']
                    else:
                        if i['sender']['id'] == id:
                            img_link = i['sender']['img_link']
                            first_name = i['sender']['first_name']
                            user_name = i['sender']['username']

        # print(msg_counter_response.json())
        for i in user_unique_list:
            for j in msg_counter_response.json():
                if j['sender'] == i['id']:
                    i['count'] = j['count']

        

        return render(request,"jobpoint_user/userchatbox.html",{"username":request.session['username'],"user_name":user_name,"user_unique_list":user_unique_list,"user_list":response.json(),"id":id,"img_link":img_link,"first_name":first_name,"msg_counter":msg_counter_response.json(),"notify":request.session['view_notification']})
    else:
        return redirect("login")



def deletequalification(request,id):
    if 'username' in request.session:
        qualifications_url= f"{url}userqualdel/{id}"
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        
        response = requests.delete(url=qualifications_url,headers=token) #url= notify_url
       
      
        if response.status_code == 200:
            msg = "data deleted"
            return redirect('showexp')
            
        else:
            msg = "not deleted"
            return HttpResponse(msg)
            
    else:       
        return redirect('login')




def deleteexp(request,id):
    if 'username' in request.session:
        exp_url= f"{url}userexpdel/{id}"
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        
        response = requests.delete(url=exp_url,headers=token) #url= notify_url
        
        if response.status_code == 200:
            msg = "data deleted"
            return redirect('showexp')
            
        else:
            msg = "not deleted"
            return HttpResponse(msg)
            
    else:       
        return redirect('login')
