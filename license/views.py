import json
import time
import os
from random import randint
import names
import datetime
from django.conf import settings
from django.shortcuts import render
from .models import Customer, License
from django.db.models import Count, Sum
from django.db.models import Max
from django.shortcuts import get_object_or_404
from sendmail import Send_MAIL
from django.urls import resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


def home(request):
	dates = License.objects.aggregate(max_date=Max('date'))
	itm = License.objects.filter(date=dates['max_date']).values('pk','customer__company', 'license', 'red', 'green', 'date', 'customer__firstname', 'customer__lastname', 'customer__email', 'grey', proc=(Sum('red') / Sum('license') * '100') )
	print(itm)
	data = {"itm": itm}
	return render(request, "home.html", context=data)

def infocomp(request, company):
	infocompurl = get_object_or_404(Customer, company=company)
	infocomp = License.objects.filter(customer__company=company).values('pk','customer__company', 'license', 'red', 'green','grey' , 'date').order_by('-date')
	dates = License.objects.aggregate(max_date=Max('date'))
	tiket = License.objects.filter(date=dates['max_date'], customer__company=company).values('pk','customer__company', 'license', 'red', 'green', 'grey', 'date', 'customer__email', proc=(Sum('red') / Sum('license') * '100') )
	print(infocompurl)
	cont =  Customer.objects.filter(company=company).values('firstname', 'lastname', 'email')
	print(cont)
	data = {"infocompurl": infocompurl,"infocomp": infocomp, "tiket": tiket, "cont": cont}
	return render(request, "infocomp.html", context=data)

@login_required(login_url='/admin/')	
def addcustomer(request):
	with open('comp.json', 'r') as f:
		company = json.load(f)
		for i in company:
			if Customer.objects.filter(company=i['customer']):
				continue
				# massage = "Заказчик уже добавлен", i['customer']
			else:
				# massage = "Добавить", i['customer']
				cre = Customer.objects.create(company=i['customer'], firstname=i['first name'], lastname=i['last name'], email=i['email'])
	data = {"company": company}
	return render(request, "addcustomer.html", context=data)

@login_required(login_url='/admin/')
def addlic(request):
	with open('lic.json', 'r') as f:
		lic = json.load(f)
		for i in lic:
			for m in range(len(i['data'])):
				dt = time.strptime(i['date'][14:], '%d.%m.%y')
				test = Customer.objects.filter(company=i['data'][m]['customer']).values('pk')
				dates = i['date'][14:]
				id_pk = test[0]['pk']
				grey = i['data'][m]['counts']['license'] - (i['data'][m]['counts']['green'] + i['data'][m]['counts']['red']) 
				if License.objects.filter(date=time.strftime('%Y-%m-%d', dt), customer_id=id_pk):
					continue
					# massage = "Информация уже добавлена"
				else:
					crelic = License.objects.create(customer_id=id_pk, license=i['data'][m]['counts']['license'], red=i['data'][m]['counts']['red'], green=i['data'][m]['counts']['green'], grey=grey, date=time.strftime('%Y-%m-%d', dt))
					# massage = "Добавить"
	data = {"lic": lic}
	return render(request, "addlic.html", context=data)

@login_required(login_url='/admin/')	
def sendmail(request, company):
	url = settings.PROTOCOL[0] + settings.ALLOWED_HOSTS[0] + '/list/' + company
	sendmailurl = get_object_or_404(Customer, company=company)
	emailinfo = Customer.objects.filter(company=company).values('firstname','lastname','email')
	listmail = [emailinfo[0]['email']]
	data = {"emailinfo": emailinfo}
	my_send = Send_MAIL(listmail, '[customer] problem with service', url)
	return render(request, "sendmail.html", context=data)

@login_required(login_url='/admin/')	
def delete(request):
	Customer.objects.all().delete()
	License.objects.all().delete()
	return redirect('home')

def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required(login_url='/admin/')
def create(request):
	custfile = 'comp.json'
	try:
		os.remove(custfile)
	except OSError:
		pass
		
	cust = {}
	cust_list = []
	for i in range(10):
		rand_last = names.get_last_name()
		rand_first = names.get_first_name()
		rand_email = (rand_first + "@gmail.com")
		customer = ("Customer" + str(i))
		cust = {"customer": customer, "first name": rand_first, "last name": rand_last, "email": rand_email}
		cust_list.append(cust)
	
	with open(custfile, 'a', encoding='utf8') as f:
		json.dump(cust_list, f, indent=4)
		
	list_read = []
	with open('comp.json') as f:
		company = json.load(f)
		for i in company:
			comp = i['customer']
			list_read.append(comp)
			
	licfile = 'lic.json'
	try:
		os.remove(licfile)
	except OSError:
		pass
	
	start = datetime.datetime.today().strftime('%d.%m.%Y')
	start = datetime.datetime.strptime(start, "%d.%m.%Y")
	end = start + datetime.timedelta(days=7)
	date_generated = [start - datetime.timedelta(days=x) for x in range(0, (end-start).days)]
	
	tests = {}
	list =[]
	for date in date_generated:
		tests = {}
		dates = ('date, format: ' + date.strftime("%d.%m.%y"))
		tests['date'] = ('date, format: ' + date.strftime("%d.%m.%y"))
		data = {}
		lists = []
		for e in range(len(list_read)):
			rand =  randint(100, 200)
			rand1 = rand - randint(0, 120)
			rand3 = rand2 - randint(0, rand2)
			data = {'customer': list_read[e], 'counts': {'license': rand, 'red': rand1, 'green': rand3}}
			lists.append(data)
		tests['data'] = lists		
		list.append(tests)
	
	with open(licfile, 'a', encoding='utf8') as f:
		json.dump(list, f, indent=4)
	return redirect('home')