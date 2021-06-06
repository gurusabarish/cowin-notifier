from django.shortcuts import render
from . import models
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.core.mail import send_mail

from django.http import JsonResponse, HttpResponse
import requests
import json
import re
import time


def home(req):
    if req.POST:
        if req.POST:
            email = req.POST['gmail']
            age = req.POST['age']
            state = req.POST['state']
            district = req.POST['district']

            state_name = models.States.objects.get(api_id=state)
            district_name = models.Districts.objects.get(api_id=district)
            if valid_user(email, district):
                user = models.Email_users()
                user.email = email
                user.age = age
                user.state_id = state
                user.state_name = state_name.name
                user.district_id = district
                user.district_name = district_name.name
                user.save()
                welcome_mail(email)

            if valid_district_id(district):
                id = models.District_ID()
                id.api_id = district
                id.save()

            context = {}
            context['state'] = models.States.objects.all()
            districts = models.Districts.objects.all()
            return redirect('home')

    context = {}
    context['state'] = models.States.objects.all()
    districts = models.Districts.objects.all()
    return render(req, 'home.html', context)


def getdistrict(req):
    state_id = req.GET.get('val')
    state = models.States.objects.get(api_id=state_id)
    district = models.Districts.objects.filter(
        state=state).values('name', 'api_id')

    district_list = []
    for i in district:
        district_list.append(i)

    data = {'district': district_list}
    return JsonResponse(data)


@login_required(login_url='/admin/login/')
def states_districts(req):
    URL = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    }

    result = requests.get(URL ,headers = header)

    if result.ok:
        json_data = result.json()
        for i in json_data['states']:
            state = models.States()
            state.name = i['state_name']
            state.api_id = i['state_id']
            state.save()

            url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(
                i['state_id'])
            district_data = requests.get(url, headers=header)
            d_data = district_data.json()
            for j in d_data['districts']:
                district = models.Districts()
                district.name = j['district_name']
                district.api_id = j['district_id']
                district.state = state
                district.save()
    else:
        return HttpResponse(result)
   
    return HttpResponse(result)


@login_required(login_url='/admin/login/')
def runscript(req):
    script()
    return HttpResponse("Script running")


def script():
    starttime = time.time()
    while True:
        try:
            district_id = models.District_ID.objects.all()
            for i in district_id:
                mail_list = []
                mail = False
                URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(
                    i.api_id, datetime.today().strftime('%d-%m-%y'))
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
                }

                result = requests.get(URL, headers=header)
                if result.ok:
                    json_data = result.json()
                    oc_set = set()
                    res = []
                    for idx, j in enumerate(json_data['sessions']):
                        if j['center_id'] not in oc_set:
                            oc_set.add(j['center_id'])
                            try:
                                hos = models.District_data.objects.get(
                                    hos_id=j['center_id'])
                                if hos.avail != j['available_capacity'] and j['available_capacity'] != 0:
                                    mail = True

                                if ((hos.min_age != j['min_age_limit']) or (hos.date.strftime('%d-%m-%Y') != j['date'])) or \
                                        (hos.avail != j['available_capacity']):
                                    hos.min_age = j['min_age_limit']
                                    hos.date = change_date_format(j['date'])
                                    hos.avail = j['available_capacity']
                                    hos.dose1 = j['available_capacity_dose1']
                                    hos.dose2 = j['available_capacity_dose2']
                                    hos.save()

                                if mail:
                                    mail_list.append(hos)

                            except ObjectDoesNotExist:
                                hos = models.District_data()
                                hos.hos_id = j['center_id']
                                hos.hos_name = j['name']
                                hos.hos_address = j['address']
                                hos.hos_district = j['district_name']
                                hos.hos_state = j['state_name']
                                hos.block = j['block_name']
                                hos.pin = j['pincode']
                                hos.min_age = j['min_age_limit']
                                hos.date = change_date_format(j['date'])
                                hos.dose1 = j['available_capacity_dose1']
                                hos.dose2 = j['available_capacity_dose2']
                                hos.avail = j['available_capacity']
                                hos.district = i
                                hos.save()
                        else:
                            res.append(idx)
                if not mail_list:
                    pass
                else:
                    alert_mail(i.api_id, mail_list)
        except Exception as e:
            server_error(e)
        print("end", time.time())
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))


def valid_user(email, district_id):
    try:
        user = models.Email_users.objects.get(
            email=email, district_id=district_id)
        return False
    except ObjectDoesNotExist:
        return True


def valid_district_id(id):
    try:
        id = models.District_ID.objects.get(api_id=id)
        return False
    except ObjectDoesNotExist:
        return True


def change_date_format(date):
    return re.sub(r'(\d{1,2})-(\d{1,2})-(\d{4})', '\\3-\\2-\\1', date)


def alert_mail(id, centers):
    email = models.Email_users.objects.filter(district_id=id).values('email')
    mail_list = []
    for i in email:
        mail_list.append(i['email'])
    subject = 'vaccine available'
    message = ''
    for j in centers:
        message += f'''Hospital: {j.hos_name}, \nAvailable capacity: {j.avail}, \nAvailable capacity dose1: {j.dose1}, \nAvailable capacity dose2: {j.dose2}, \nState: {j.hos_state}, \nDistrict: {j.hos_district}, \nBlock: {j.block}, \nPIN code: {j.pin}, \n\n-----------------------------------------\n'''
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, mail_list)


def welcome_mail(email):
    subject = 'You are registered on vaccine notifier'
    message = f'Hi, \n\nYou will get a mail when vaccine available. \n\nThank you,'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from,
              recipient_list)
    return True


def server_error(e):
    subject = f'Server not responding {e}'
    message = f'{e}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['gurusabarisha@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
