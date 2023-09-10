from django.views.generic import ListView
from re import template
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.urls import reverse
from requests import request
from django.contrib import messages
from authentication.models import User
from main.models import Cart
from django.db.models import Q
from django.views.generic import UpdateView
from authentication.utils.check_login_state import check_login
from authentication.models import Expert


def login(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = "Fill out all of fields!"
        if username and password:
            username = username.strip()
            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    request.session['user_id'] = user.id
                    request.session['username'] = username
                    return redirect('main:index')
                else:
                    message = "Wrong password！"
            except:
                message = "Username doesn't exist！"
        return render(request, 'authentication/login.html', {"message": message})
    return render(request, 'authentication/login.html')


def expert(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        full_name = request.POST.get('full_name', None)
        email = request.POST.get('email', None)
        phone_number = request.POST.get('phone_number', None)
        expertise = request.POST.get('expertise', None)
        experience = request.POST.get('experience', None)
        availability = request.POST.get('availability', None)
        references = request.POST.get('references', None)

        if username.strip() == '':
            message = "The username cannot be empty!"
        elif password.strip() == '':
            message = "The password cannot be empty!"
        elif full_name.strip() == '':
            message = "The full name cannot be empty!" 
        elif email.strip() == '':
            message = "The email cannot be empty!"
        elif phone_number.strip() == '':
            message = "The phone number cannot be empty!"

        if username and password and email and full_name and phone_number:
            username = username.strip()
            user_list = User.objects.filter(Q(name=username) | Q(email=email))
            if user_list.exists():
                message = "Username or email exists！"
            else:
                user = User(name=username, password=password, email=email, phone_num=phone_number)
                user.save()
                request.session['user_id'] = user.id
                request.session['username'] = username
                expert = Expert(user = user, full_name=full_name, email=email, phone_number=phone_number,
                        expertise=expertise, experience=experience,
                        availability=availability, references=references)
                expert.save()
                return redirect('main:index')
        return render(request, 'authentication/expert.html', {"message": message})
    return render(request, 'authentication/expert.html')
    
def register(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        message = "Fill out all of fields!"
        if username and password and email:
            username = username.strip()
            user_list = User.objects.filter(Q(name=username) | Q(email=email))
            if user_list.exists():
                message = "Username or email exists！"
            else:
                user = User(name=username, password=password, email=email)
                user.save()
                request.session['user_id'] = user.id
                request.session['username'] = username
                return redirect('main:index')
        return render(request, 'authentication/register.html', {"message": message})
    return render(request, 'authentication/register.html')


@check_login
def update(request):
    id = request.session['user_id']
    user = User.objects.get(id=id)
    if request.method == "POST":
        message = "Fill out all of fields!"
        try:
            old_name = request.POST.get('old_name', None)
            new_name = request.POST.get('new_name', None)
            old_email = request.POST.get('old_email', None)
            new_email = request.POST.get('new_email', None)
            user = User.objects.get(name=old_name)
            
            if new_name and new_email:
                new_name = new_name.strip()
                user_list = User.objects.filter(Q(name=new_name) | Q(email=new_email))
                if user_list.exists():
                    message = 'New username or email exists!'
                if user.email == old_email:
                    user.name = new_name
                    user.email = new_email
                    user.save()
                    message = "Updated"
                    return redirect('authentication:login')
                else:
                    message = 'Old username and old email do not match!'
        except Exception as e:
            if old_email and old_name:
                message = "Old username or email not found！"
        return render(request, 'authentication/update.html', {"message": message}, {"user":user})
    return render(request, 'authentication/update.html', {"user":user})

@check_login
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'username' in request.session:
        del request.session['username']
    return redirect('main:index')


@check_login
def userinfo(request, username):
    user = get_object_or_404(User, pk=request.session['user_id'])
    return render(request, 'authentication/user.html', {'user': user})


@check_login
def check_cart(request):
    cart = {'empty': False}

    cart_list = Cart.objects.filter(Q(id=request.session['user_id']))
    if not cart_list.exists():
        cart['empty'] = True
        return HttpResponse(cart)
    # else:
    #     user = User(name=username, password=password, email=email)
    #     user.save()
    #     request.session['user_id'] = user.id
    #     request.session['username'] = username
    #     return redirect('main:index')

class update_profile(UpdateView):
    model = User
    template_name = 'authentication/update.html'
    fields = "__all__"
    #fields = ['name','password','email','profile','gender','birthday','phone_num']

class upgrade(ListView):
    model = User
    template_name = 'authentication/upgrade.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, pk=request.session['user_id'])
        self.status = self.user.status
        return super(upgrade, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(upgrade, self).get_context_data(**kwargs)
        if self.status == "Premium Free":
            context['plans'] = [('premium',100),('premium plus',200)]
        if self.status == "Premium":
            context['plans'] = [('premium plus',200)]
        if self.status == "Premium Plus":
            context['plans'] = []
        return context