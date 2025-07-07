import json

import pytz
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Staff, Cartridges, Departments, Cartridge_Models
from reportlab.graphics.barcode import code128, code39
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from io import BytesIO


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
    data = json.loads(request.body.decode())
    cartridges = Cartridges.objects.all()
    if data['model_id'] is not None or '':
        cartridges = cartridges.filter(model_id=data['model_id'])
    if data['department_id'] is not None or '':
        cartridges = cartridges.filter(department_id=data['department_id'])

    result = [{
        "id": c.pk,
        "model": c.model.name,
        "department": c.department.name,
        "date_of_last_location": f'{c.date_of_last_location.astimezone(pytz.timezone("Asia/Irkutsk")).date().strftime("%d.%m.%Y")} '
                     f'{c.date_of_last_location.astimezone(pytz.timezone("Asia/Irkutsk")).time().strftime("%H:%M:%S")}',
    } for c in cartridges.select_related('model', 'department')]
    return JsonResponse({"result": sorted(result, key=lambda sort_by: sort_by['id'])})

@login_required()
def get_cartridge_data_to_edit(request):
    data = json.loads(request.body.decode())
    result = [{
        "model_id": c.model_id,
        "department_id": c.department_id,
        "description": c.description,
    } for c in Cartridges.objects.all().filter(pk=data['id'])]
    return JsonResponse({"result": result})

@login_required()
def get_departments(request):
    result = [{
        "id": d.pk,
        "name": d.name,
    } for d in Departments.objects.all()]
    return JsonResponse({"result": sorted(result, key=lambda sort_by: sort_by['id'])})

@login_required()
def get_cartridge_models(request):
    result = [{
        "id": cm.pk,
        "name": cm.name,
    } for cm in Cartridge_Models.objects.all()]
    return JsonResponse({"result": sorted(result, key=lambda sort_by: sort_by['id'])})


@login_required()
def add_new_cartridge(request):
    data = json.loads(request.body.decode())
    created_items = []

    with transaction.atomic():
        for item in data:
            for _ in range(item['count']):
                cartridge = Cartridges(
                    model_id=item['model_id'],
                    department_id=item['department_id'],
                    description=item['description'] if 'description' in item is not None or '' else None,
                    date_of_last_location=timezone.now(),
                )
                cartridge.save()
                created_items.append({"cartridge": f"{cartridge.model.name} ID_{cartridge.pk}"})

    return JsonResponse({"result": created_items})

@login_required()
def update_cartridge_data(request):
    data = json.loads(request.body.decode())
    cartridge = Cartridges.objects.get(pk=data['id'])
    cartridge.model_id = data['model_id']
    cartridge.department_id = data['department_id']
    cartridge.description = data['description']
    cartridge.date_of_last_location = timezone.now()
    cartridge.save()
    return JsonResponse({"result": f'Данные о картридже №{data['id']} успешно изменены!'})

@login_required()
def generate_barcode_pdf(request):
    data = json.loads(request.body.decode())
    # print(data['model'], data['id'])
    # Устанавливаем размер страницы 43x25 мм
    page_width = 43 * mm
    page_height = 25 * mm

    # Создаем буфер для PDF
    buffer = BytesIO()

    # Создаем PDF документ с нужным размером
    p = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    # Настройки шрифтов
    p.setFont("Helvetica", 6)

    # 1. Добавляем заголовок сверху
    title = data['model']
    title_width = p.stringWidth(title, "Helvetica", 6)
    p.drawString((page_width - title_width) / 2, page_height - 4 * mm, title)

    # 2. Генерируем штрихкод Code128
    barcode_value = data['id']  # Можно получать из параметров

    # Создаем штрихкод с подходящими размерами для маленькой этикетки
    barcode = code128.Code128(
        barcode_value,
        barHeight=14 * mm,  # Высота штрихов
        barWidth=0.45 * mm,  # Толщина штрихов
        humanReadable=False  # Текст будем выводить отдельно
    )

    # Центрируем штрихкод по горизонтали
    barcode_x = (page_width - barcode.width) / 2
    barcode_y = page_height - 20 * mm

    # Рисуем штрихкод
    barcode.drawOn(p, barcode_x, barcode_y)

    # 3. Добавляем значение штрихкода снизу
    p.setFont("Helvetica", 5)  # Меньший шрифт для значения
    value_width = p.stringWidth(barcode_value, "Helvetica", 5)
    p.drawString((page_width - value_width) / 2, 2 * mm, barcode_value)

    # Завершаем создание PDF
    p.showPage()
    p.save()

    # Получаем содержимое буфера
    pdf = buffer.getvalue()
    buffer.close()

    # Создаем ответ с PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="example.pdf"'

    return response