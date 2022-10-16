import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt
from .models import Post
import json
from functools import wraps
import os


# base_url = 'http://localhost:8001/'
base_url = 'https://backend95.pythonanywhere.com/'



def userLoginOrNot(function_name):
    @wraps(function_name)
    def wrapper(*args, **kwargs):
        if args[0].session.get('access_token'):
            return function_name(*args, **kwargs)
        else:
            return redirect(reverse('login-signup'))
    return wrapper

def set_session(request, setStatsToo=True):
    r = requests.get(base_url + 'core/get_profile/', headers={"Authorization": "JWT "+request.session['access_token']})
    print("User Detail is ", r.json())
    if r.status_code == 200:
        request.session['user_detail'] = r.json()[0]
    if setStatsToo:
        r = requests.get(base_url + 'core/profile_stats/', headers={"Authorization": "JWT "+request.session['access_token']})
        if r.status_code == 200:
            request.session['profile_stats'] = r.json()[0]




def reloadSession(request):
    set_session(request, False)
    return JsonResponse({'success':True}, status=200)

def logout_or_remove_session(request):
    if request.session.get('user_detail'):
        del request.session['user_detail']
        del request.session['access_token']
    return redirect(reverse('login-signup'))

@userLoginOrNot
def add_question(request):
    context = {}
    context['categories'] = []
    if request.method == 'POST':
        print(request.POST)
        data = request.POST.copy()
        data['created_by'] = request.session['user_detail'].get('id')
        json_data = json.dumps(data)
        post_url = base_url+'dev/question/'
        r = requests.post(post_url, data)
        print(r.status_code, r.json())
        if r.status_code == 201:
            print(r.json())
    else:
        if request.GET.get('question_id'):
            question_id = request.GET['question_id']
            question_url = base_url + 'dev/question/'+question_id+'/'
            r = requests.get(question_url, headers={"Authorization": "JWT "+request.session['access_token']})
            if r.status_code == 200:
                context['question_detail'] = r.json()

    return render(request, 'core/add_question.html', context)

@userLoginOrNot
def question_detail(request):
    context = {}
    if not request.GET.get('question_id'):
        return redirect(reverse('dashboard'))
    return render(request, 'core/question_detail.html', context)

@userLoginOrNot
def dashboard(request):
    print("base url ", base_url, os.environ.get('LIVE'))
    return render(request, 'core/dashboard.html', {'questions':[]})

def login_signup(request):
    if request.method == "POST":
        print("Form Post ", request.POST)
        form_name = request.POST.get('form_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if form_name == 'signup':
            r = requests.post(base_url + 'core/', data={'username': username,'email':email, 'password': password})
            if r.status_code != 201:
                error = r.json() if r.status_code != 500 else 'Something Went wrong, Please try later'
                return JsonResponse({'error': error}, status=400)

        r = requests.post(base_url + 'core/api/token/', data={'username': username, 'password': password}, headers={})
        print("Token ", r.json())
        if r.status_code == 200:
            request.session['access_token'] = r.json()['access']
            set_session(request)
            return JsonResponse({'redirect_url':reverse('dashboard')})
        else:
            return JsonResponse({'error': 'Something Went wrong, Please try later'}, status=400)
    request.session['base_url'] = base_url
    return render(request, 'core/login_signup.html', {'posts':''})

@userLoginOrNot
def profile(request):
    return render(request, 'core/profile.html', {'posts':''})

@userLoginOrNot
def question_requests(request):
    return render(request, 'core/requests.html', {'base_url':base_url})