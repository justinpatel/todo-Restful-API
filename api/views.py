from django.shortcuts import render
from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework.authtoken.views import ObtainAuthToken
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'api/index.html')

def login_view(request):
    if request.method == 'POST':
        btn = request.POST['btn']
        if btn == 'login':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                #token, created= Token.objects.get_or_create(user=user)
                #print(user.auth_token.key)
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, "api/login.html",{
                    "msg":"Invalid Credentials"
                })
        elif btn == 'signup':
            return render(request, 'api/register.html')
            
    return render(request, 'api/login.html')

def logout_view(request):
    logout(request)
    return render(request, "api/login.html",{
        "msg":"Loged out"
    })

def register(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            return render(request, 'api/register.html',{
                "msg": "Email is already in user"
            })
        elif User.objects.filter(username=username).exists():
            return render(request, 'api/register.html',{
                "msg": "username is already taken"
            })
        else:
            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()
            #token = Token.objects.get(user=user).key
            #user.token = token
            return render(request, 'api/login.html',{
                "msg": "successfully registered"
            })
    return render(request, 'api/register.html')

class TodoList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        todos = Todo.objects.all()
        todo_data = TodoSerializer(todos, many=True)
        return Response(todo_data.data, status=200)

    def post(self, request):
        todo = TodoSerializer(data=request.data)
        if todo.is_valid():
            item = todo.save()
            item.completed = False
            item.url = reverse('todo_one', args=[item.id])
            item.save()
            return Response(todo.data, status=201)
        return Response(None, status=400)

    def delete(self, request):
        Todo.objects.all().delete()
        return Response(None,status=204)

class TodoOne(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, todo_id):
        try:
            item = Todo.objects.get(pk=todo_id)
            todo_data = TodoSerializer(item)
            return Response(todo_data.data, status=200)
        except Todo.DoesNotExist:
            return Response(None, status=400)

    def patch(self, request, todo_id):
        try:
            item = Todo.objects.get(pk=todo_id)
            serializer = TodoSerializer(data=request.data, instance=item, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(None, status=400)
        except Todo.DoesNotExist:
            return Response(None, status=400)

    def delete(self, request, todo_id):
        try:
            item = Todo.objects.get(pk=todo_id)
            item.delete()

            return Response(None, status=200)
        except Todo.DoesNotExist:
            return Response(None, status=400)

'''class CustomAuthToken(ObtainAuthToken):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = authenticate(request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return render(request, "api/index.html",{
                'token':token
            })
        return render(request, "api/index.html",{
                'token':request.user
            })'''