from django.urls import path
from . import views
urlpatterns = [
   path('index', views.index, name='index'),
#    path('signup', views.signup, name='signup'),
#    path('login', views.login, name='login'),
   path('logout', views.logout, name='logout'),
   path('qualificaton', views.qualificaton, name='qualificaton'),
   path('showexp', views.showexp, name='showexp'),
   path('update/<int:id>/', views.update, name='update'),
    path('updateexp/<int:id>/', views.updateexp, name='updateexp'),
   path('makepraposal/<int:id>', views.makepraposal, name='makepraposal'),
   path('addexpirence', views.addexpirence, name='addexpirence'),
   path('dashboarduser', views.dashboarduser, name='dashboarduser'),
   path('editprofileuser/',views.editprofileuser,name='editprofileuser'),
   path('upload',views.userupload,name='upload'),
   path('like/<int:id>',views.like,name='like'),
   path('dislike/<int:id>',views.dislike,name='dislike'),
   path('notify',views.notification_view,name='notify'),
   path('notify/<int:id>',views.deletenotification,name='notify'),
   path('projectstatus',views.project_status,name='projectstatus'),
   path('updatestatus/<int:id>',views.project_status_update,name='updatestatus'),
   path('deletestatus/<int:id>',views.deletestatus,name='deletestatus'),
    path('userchatbox/',views.userchatbox,name='userchatbox'),
    path('userchatbox/<int:id>',views.userchatbox,name='userchatbox_id'),

]