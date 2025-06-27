import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Staff, Cartridges


def get_staff_id(cookie):
    session_key = cookie
    session = Session.objects.get(pk=session_key)
    decoded_session = session.get_decoded()
    # staff = Staff.objects.get(account_id=decoded_session['_auth_user_id'])
    # return staff.pk

# Авторизация пользователей с получением session cookie
@csrf_exempt
def auth(request):
    data = json.loads(request.body)
    username = data.get('username', '')
    password = data.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # staff = Staff.objects.get(account_id=user.id)
            # log = Actions_Logs(key=None, type=0, staff_id=staff.pk, data=None)
            # log.save()
            return JsonResponse({"result": 'Авторизация прошла успешно!'})

# Получение данных пользователя на основе session cookie
@login_required
def get_user_data(request):
    session_key = request.COOKIES['sessionid']
    session = Session.objects.get(pk=session_key)
    decoded_session = session.get_decoded()
    # print(decoded_session)
    # print(decoded_session['_auth_user_id'])
    user = User.objects.get(pk=decoded_session['_auth_user_id'])
    response = [{
        "uid": user.id,
        "login": user.username,
        "post": user.staff.get_post_display(),
        "full_name": f'{user.last_name} {user.first_name} {user.staff.father_name}',
    }]
    return JsonResponse({"result": response})


# Выход пользователя из системы
@login_required
def logout_user(request):
    logout(request)
    return JsonResponse({"result": 'user logout'})


# Проверка авторизованного пользователя
@login_required()
def user_verify(request):
    return JsonResponse({"result": 'true'})

@login_required()
def get_cartridges_data(request):
    result = [{
        "id": i.pk,
        "model": i.model,
        "department": i.department.name,
    } for i in Cartridges.objects.all()]
    return JsonResponse({"result": sorted(result, key=lambda sort_by: sort_by['id'])})