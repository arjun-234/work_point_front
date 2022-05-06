# jobpoint_client/urls.pyfrom django.urls import path
from django.urls import path
from jobpoint_client import views
urlpatterns = [
    path('login/',views.login,name='login'),
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path('dashboardclient/',views.dashboard_client,name='dashboardclient'),
    path('otp/',views.check_otp,name='otp'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('makepost/',views.makepost,name='makepost'),
    path('deletepost/<int:id>', views.deletepost, name='deletepost'),
    path('editpost/<int:id>',views.editpost,name='editpost'),
    path('logout/',views.logout,name='logout'),
    path('upload_file/',views.upload,name='upload_file'),
    path('chatbox/',views.chatbox,name='chatbox'),
    path('chatbox/<int:id>',views.chatbox,name='chatbox_id'),
    path('user_search_result',views.user_search_result,name='user_search_result'),
    path('user_profile/<int:id>',views.user_profile,name='user_profile'),
    path('proposal_notification/<str:userid_jobid>',views.proposal_notification,name='proposal_notification'),
    path('proposal_action/<str:pid_action>',views.proposal_action,name='proposal_action'),
    path('task_status',views.task_status,name='task_status'),
    path('proposal_history',views.proposal_history,name='proposal_history')
    
]   
