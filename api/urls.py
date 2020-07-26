from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name="getToken"),
    path('', views.TodoList.as_view(), name='apiview'),
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('<todo_id>/', views.TodoOne.as_view(), name='todo_one'),
    
]
