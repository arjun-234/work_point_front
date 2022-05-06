from django.contrib import messages
import requests
from django.core.files.storage import FileSystemStorage
from freelance.local_settings import url
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
import datetime
from django.views.decorators.cache import cache_control

def index(request):
    return redirect('login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
   
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        urls=f'{url}login'
        request.session['username']=username
        data={
            "username":username,
            "password":password,
        }
        response=requests.post(url=urls,json=data)
        # print(response.status_code)
        if response.status_code==200:
            request.session['user_token']=response.json()['token']
            request.session['username']=response.json()['username']
            verify_url=f'{url}verify_token'
            data_token={
                "token":request.session['user_token'],
                "username":request.session['username']
            }
            response_token=requests.post(url=verify_url,json=data_token)
            if response_token.json()['matched']:
                if response.json()["is_client"]:
                    request.session['img_link']= response.json()["img_link"]
                    request.session['first_name'] = response.json()['first_name']
                    return redirect('dashboardclient')
                  
                else:
                    return redirect("dashboarduser")
            else:
                messages.info(request,response_token.json()['msg'])
                return redirect("login")
        else:
            messages.info(request, response.json()['msg'])
            return redirect("login")

    return render(request,'login_client.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        gender=request.POST['gender']
        mobile=request.POST['mobile_number']
        country=request.POST['country']
        role=request.POST['role']
        
        urls=f'{url}register'
        data={
                "first_name":first_name,
                "last_name":last_name,
                "username":username,
                "email":email,
                "password":password,
                "gender":gender ,
                "mobile":mobile,
                "country":country,
                "is_client":role

            }
        response =  requests.post(url=urls,json=data)

        if response.status_code==200:
            request.session['username']=username
            msg=response.json()['msg']
            messages.info(request, msg)
            return redirect("login")
        else:
            msg=response.json()['msg']
            messages.info(request, msg)
            return redirect('register')
            
    return render(request,'Register_client.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard_client(request):
    if 'username' in request.session:
        notification_list_url=f'{url}client_n'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        notification_data={
            "username":request.session['username']
            }
        notification_response=requests.post(url=notification_list_url,headers=token,json=notification_data)

        notification_list=notification_response.json()

        username = request.session['username']
        urls=f'{url}client_job_list'
        
        token={
            'Authorization': f"Token {request.session['user_token']}"
            
        }
        data={
            "username":request.session['username']
        }
        response=requests.post(url=urls,headers=token,json=data)
        response_data=response.json()[::-1]
        return render(request,"client_dashboard.html",{"data":response_data,"username":username,"notification_list":notification_list})
    else:
        return redirect("login")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgotPassword(request):
    if request.method=='POST':
        username=request.POST['username']
        request.session['forgot_password_user']=username     
        urls=f'{url}forgot_password'
        data={
            "username":username
        }
        try:
            response=requests.post(url=urls,json=data)
            if response.status_code==200:
                request.session["user_email"]=response.json()['email'][5:]
                request.session['username']=username
                return redirect("otp")
            else:
                messages.info(request,response.json()['msg'])
                return redirect('forgotPassword')
        except Exception as e: 
            print("err",e)
    return render(request,'forgot_password.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def check_otp(request):
    dic={
            "email":request.session["user_email"],
            "message":"********"
        }
    if request.method=='POST':
        otp = request.POST['otp']
        urls = f'{url}verify_otp'
        data = {
            'user_otp':int(otp),
            'username':request.session['forgot_password_user']
            }
        response=requests.post(url=urls,json=data)
        print(urls,'!!!!!!!!!!!!!!!!!!!!!')
        if response.json()["matched"]:
            messages.info(request,response.json()['msg'])
            return redirect("changepassword")
        else:
            messages.info(request,response.json()['msg'])
            return redirect("login")
    return render(request,"otp.html",dic)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changepassword(request):
    if request.method=="POST":
        username=request.session['username']
        change_password=request.POST['change_password']
        confirm_change_password=request.POST['confirm_change_password']
        if change_password==confirm_change_password:
            urls=f'{url}set_password'
            data={
                "username":username,
                "password":confirm_change_password
             }
            response=requests.post(url=urls,json=data)
            if response.status_code==200:
                return redirect("login")
            else:
                messages.info(request,response.json()['msg'])
                return redirect('changepassword')   
        else:
            messages.info(request,"Password does not match !!!!!!")
            return redirect('changepassword')

    return render(request,'change_password.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editprofile(request):
    if 'username' in request.session:
        urls=f'{url}user_details'
        token={
                'Authorization': f"Token {request.session['user_token']}"
                }
        data={
                "username":request.session['username']
            }
        response=requests.post(url=urls,headers=token,json=data)
        response_data={
                    "first_name":response.json()["first_name"],
                    "img_link":response.json()["img_link"],
                    "last_name":response.json()['last_name'],
                    "username":response.json()['username'],
                    "about":response.json()['about'],
                    "email":response.json()['email']
        }
        if request.method=='POST':
            edit_url=f'{url}edit_profile'
            if response.status_code==401:
                return redirect("dashboardclient")
            else:
                first_name=request.POST.get('fs_name')
                last_name=request.POST.get('lastname')
                about=request.POST.get('about')
                user_name = request.session['username']
                
                edit_data={
                    "first_name":first_name,
                    "img_link":response.json()["img_link"],
                    "last_name":last_name,
                    "username":user_name,
                    "about":about
                    }
                edit_response=requests.put(url=edit_url,headers=token,json=edit_data)
                response=requests.post(urls,headers=token,json=data)
                request.session['img_link']=response.json()["img_link"]
                # request.session['img_link']=edit_response.json()["img_link"]
                if edit_response.status_code==200:
                    token={
                            'Authorization': f"Token {request.session['user_token']}"
                                    
                            }
                    data={
                                    "username":request.session['username']
                        }
                    updated_response=requests.post(urls,headers=token,json=data)
                    updated_data={
                        "first_name":updated_response.json()["first_name"],
                        "img_link":updated_response.json()["img_link"],
                        "last_name":updated_response.json()['last_name'],
                        "username":updated_response.json()['username'],
                        "about":updated_response.json()['about'],
                        "email":response.json()['email']
                    }
                    # request.session['img_link']=updated_response.json()["img_link"]
                    # request.session['first_name']=updated_response.json()["first_name"]
                    request.session['img_link']=updated_response.json()["img_link"]
                    return render(request,"edit_profile.html", updated_data)
                    # return redirect('dashboardclient')
                else:
                    print(edit_response.json()['msg'])
        return render(request,"edit_profile.html",response_data)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def makepost(request):
    if 'username' in request.session:
        view_skill=f'{url}skill_list'
        skill_url=f'{url}add_job_skill'
        urls=f'{url}job_post'
        token={
            'Authorization': f"Token {request.session['user_token']}"
            
            }
        skill_response=requests.get(url=view_skill,headers=token)
        skill_view_data=skill_response.json()
        if request.method=="POST":
            title=request.POST['job_title']
            job_desc=request.POST['job_desc']
            price=request.POST['price']
            
            skill_list=request.POST.getlist('checks[]')
            
            data={
                "username":request.session['username'],
                "title":title,
                "description":job_desc,
                "posted_date":datetime.datetime.now().strftime("%d/%m/%Y"),
                "price":float(price)
            }
            
            response=requests.post(url=urls,headers=token,json=data)
            if response.status_code==200:
                request.session['post_id']=response.json()['job_id']
                skill_data={
                "job":request.session['post_id'],
                "skill_list":skill_list
                        }
                response=requests.post(url=skill_url,headers=token,json=skill_data)
                messages.info(request,"Job has been posted")
                return redirect('dashboardclient')
            else:
                # messages.info(request,response.json()['msg'])
                return redirect('makepost')

        return render(request,"make_post.html",{"data":skill_view_data,"username":request.session['username']})



def logout(request):
    if 'username' in request.session:
        urls=f'{url}logout'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        data={
            "username":request.session['username']
        }
        response=requests.post(url=urls,headers=token,json=data)
        if response.status_code==200:
            del request.session['username']          
        else:
            return HttpResponse("Couldn't logout",response.status_code)
    return redirect('login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload(request):
    if request.method=="POST":
        urls=f'{url}edit_profile'
      
        uploaded_filename = request.FILES['document']
        fs=FileSystemStorage()
        fs.save(uploaded_filename.name,uploaded_filename)
        print("AAAA",uploaded_filename)
        data={
            "username":request.session['username'],
            "img_link":f'/static/media/{uploaded_filename}'
        }
        response=requests.put(url=urls,json=data)
        return redirect('editprofile')
    return render(request,'upload_file.html',{"username":request.session['username']})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editpost(request,id):
    if 'username' in request.session:
        skill_url=f'{url}add_job_skill'
        view_skill=f'{url}skill_list'
        token={
            'Authorization': f"Token {request.session['user_token']}"
            
            }
        skill_response=requests.get(url=view_skill,headers=token)
        skill_view_data=skill_response.json()
        view_data_url=f'{url}get_job_detail/{id}'
        token={
                'Authorization': f"Token {request.session['user_token']}"
                
        }
        data={
            "username":request.session['username']
        }
        response=requests.post(url=view_data_url,headers=token,json=data)
        get_edit_post=response.json()
        if request.method=='POST':
            edit_post_url=f'{url}edit_job/{id}'
            token={
                'Authorization': f"Token {request.session['user_token']}"
                
            }
            title=request.POST.get('job_title')
            desc=request.POST.get('job_desc')
            posted_date=request.POST.get('posted_date')
            username=request.session['username']
            price=request.POST.get('price')
            skill_list=request.POST.getlist('checks[]')
            edit_data={
                    "title":title,
                    "description":desc,
                    "posted_date":posted_date,
                    "username":username,
                    "price":price
                }
                
            view_response=requests.put(url=edit_post_url,headers=token,json=edit_data)
            if view_response.status_code==200:
                skill_data={
                "job":id,
                "skill_list":skill_list
                        }
                response=requests.post(url=skill_url,json=skill_data)
                return redirect('dashboardclient')
            else:
                messages.info(request,view_response.json()['msg'])
                return redirect('dashboardclient')     
        return render(request,"edit_post.html",{"view_data":get_edit_post,"username":request.session['username'],"data":skill_view_data})

def deletepost(request,id):
    if 'username' in request.session:
        delete_url=f'{url}delete_job/{id}'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        data={
            "username":request.session['username']
        }
        response=requests.delete(url=delete_url,headers=token,json=data)
        if response.status_code==200:
            return redirect('dashboardclient')
        else:
            messages.info(request,response.json()['msg'])
            return redirect('dashboardclient')
            
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def chatbox(request,id=None):
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
            return redirect('chatbox_id',id)
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
                request.session['msg_reciever_id'] = id
            except:
                img_link=None
                first_name=None

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
                    else:
                        if i['sender']['id'] == id:
                            img_link = i['sender']['img_link']
                            first_name = i['sender']['first_name']

        # print(msg_counter_response.json())
        for i in user_unique_list:
            for j in msg_counter_response.json():
                if j['sender'] == i['id']:
                    i['count'] = j['count']

        

        return render(request,"chatbox.html",{"username":request.session['username'],"user_unique_list":user_unique_list,"user_list":response.json(),"id":id,"img_link":img_link,"first_name":first_name,"msg_counter":msg_counter_response.json()})
    else:
        return redirect("login")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_search_result(request):
    if 'username' in request.session:
        if request.method=='POST':
            urls=f'{url}user_profile_search'
            search_input=request.POST['input']

            if len(search_input.strip())==0:
                messages.info(request,"Enter a valid input")
                return redirect('dashboardclient')

            token={
                    'Authorization': f"Token {request.session['user_token']}"
                }

            data={
                "username":request.session['username'],
                "input":search_input
            }

            response=requests.post(url=urls,headers=token,json=data)
            if response.status_code!=200:
                messages.info(request,response.json()['msg'])
                return redirect('dashboardclient')

            return render(request,"user_search_result.html",{"user_data":response.json(),"username":request.session['username'],"id":id})
        return redirect('dashboardclient')
    else:
        return redirect("login")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)         
def user_profile(request,id):
    if 'username' in request.session:
        urls=f'{url}user_profile_details/{id}'
        token={
                    'Authorization': f"Token {request.session['user_token']}"
                }

        data={
                "username":request.session['username']
            }
        response=requests.post(url=urls,headers=token,json=data)
        if response.status_code==200:
            profile_data=response.json()
            
        else:
            messages.info(request,response.json()['msg'])
            return redirect('dashboardclient')
        return render(request,"user_profile.html",{"data":profile_data,"username":request.session['username']})
    else:
        return redirect('login')


def accept_reject_proposal(request,id):
    if 'username' in request.session:
        urls=f'{url}proposal_action/{id}'

        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        data={
            "username":request.session['username']
        }
        return redirect('dashboardclient')
    else:
        return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def proposal_notification(request,userid_jobid):
    proposer_id = int(userid_jobid.split('_')[0])
    job_id = int(userid_jobid.split('_')[1])
    if 'username' in request.session:
        urls=f'{url}proposal_detail/{job_id}'
        token={
                'Authorization': f"Token {request.session['user_token']}"  
              }
        data={
            "username":request.session['username'],
            "proposer_id":proposer_id        
        }
        response=requests.post(url=urls,headers=token,json=data)
        details_data=response.json()
        return render(request,"proposal_notification.html",{"username":request.session['username'],"data":details_data})
    else:
        return redirect('login')

def proposal_action(request,pid_action):
    if 'username' in request.session:
        p_id = int(pid_action.split('_')[0])
        action = pid_action.split('_')[1]
        if action == "True":
            is_accepted = True
        if action == "False":
            is_accepted = False

        urls=f'{url}proposal_action/{p_id}'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        data={
            "username":request.session['username'],
            "is_accepted":is_accepted
            }
        response = requests.put(url=urls,headers=token,json=data)
        if response.status_code == 200:
            if is_accepted:
                messages.info(request,"Proposal Has been accepted")
            if not is_accepted:
                messages.info(request,"Proposal has been rejected!!")
            return redirect("dashboardclient")
        else:
            print(response.status_code)
            return redirect("dashboardclient")
    else:
        return redirect('login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def task_status(request):
    if 'username' in request.session:
        urls = f'{url}client_status'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        data={
            "username":request.session['username'],
            }   

        response = requests.post(url=urls,headers=token,json=data)
        print(response.status_code,"@@@@@@@@@@@@@@")
        if response.status_code == 200:
            return render(request,'task_status.html',{'status':response.json()[::-1],'username':request.session['username']})
        else:
            return redirect('dashboardclient')
    else:
        return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def proposal_history(request):
    if 'username' in request.session:
        urls = f'{url}proposal_history'
        token={
                'Authorization': f"Token {request.session['user_token']}"
              }
        data={
            "username":request.session['username'],
            }
        response = requests.post(url=urls,headers=token,json=data)

        print(response,"######")
        if response.status_code == 200:
            return render(request,'proposal_history.html',{'history':response.json()[::-1],'username':request.session['username']})
        else:
            return redirect('dashboardclient')
    else:
        return redirect('login')
