#MAP-extended urls to the specific view
from django.urls import path
from .import views

urlpatterns=[
    
    path('', views.home, name='home'),
    #path('home/',views.home),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('users/', views.get_all_users, name='get_all_users'),
    path('user/<str:email>/', views.get_user_by_email, name='get_user_by_email'),
    path('user/update/<str:email>/', views.update_user, name='update_user'),
    path('user/delete/<str:email>/', views.delete_user, name='delete_user'),
]