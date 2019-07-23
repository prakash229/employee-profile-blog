from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView 
from django.urls import reverse
from django.urls import reverse_lazy
from employee.forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from ems.decorators import role_required,admin_only
# Create your views here.
import json

from rest_framework.views import APIView
from .serializers import LoginSerializer
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if  request.GET.get('next',None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            context['error'] = "provide valid credentials!"
            return render(request, "auth/login.html",context)
    else:
        return render(request,"auth/login.html", context)

@login_required(login_url="/login/")
def success(request):
    context = {}
    context['user'] = request.user
    return render(request,"auth/success.html",context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))

@login_required(login_url="/login/")
def employee_list(request):
    print(request.role)
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'Empolyee'
    return render(request,'employee/index.html',context)

@login_required(login_url="/login/")
def employee_details(request, id=None):
    context = {}
    context['user'] = get_object_or_404(User, id=id)
    return render(request,'employee/details.html',context)

@login_required(login_url="/login/")
@role_required(allowed_roles=["Admin","HR"])
@admin_only
def employee_add(request):
    if request.method == 'POST':
        context = {}
        user_form = UserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            user_form.save()    
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/add.html',context)
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        return render(request, 'employee/add.html',context)

@login_required(login_url="/login/")
def employee_edit(request,id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/edit.html',{"user_form":user_form})
    else:
        user_form = UserForm(instance=user)
        return render(request, 'employee/edit.html',{"user_form":user_form})

@login_required(login_url="/login/")
def employee_delete(request, id=None):
    user = get_object_or_404(User,id=id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context = {}
        context['user'] = user
        return render(request, 'employee/delete.html',context) 

class ProfileUpdate(UpdateView):
    fields = ['designation', 'salary', 'picture']
    template_name = 'auth/profile_update.html'
    success_url = reverse_lazy('my_profile')

    def get_object(self):
        return self.request.user.profile



class MyProfile(DetailView):
    template_name = 'auth/profile.html'
    def get_object(self):
        return self.request.user.profile
 
class LoginView(APIView):
    def post(self, request):
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )
    def post(self, request):
        django_logout(request)
        return Response(status=204)


@csrf_exempt
def Login(request):
    if request.method == "POST":
        print(json.loads(request.body))
        a=json.loads(request.body)
        serializer = LoginSerializer(data=a)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({"token": token.key})
