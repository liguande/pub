# coding:utf-8
from django.shortcuts import render,redirect
from eduOpinion.models import User

def home(request):
	if request.session.get('username'):
		return redirect('/index/')
	else:
		return render(request, 'home.html')

def createUser(request):
	if request.session.get('username'):
		return redirect('/index/')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		password_confirm = request.POST['password_confirm']
		if password == password_confirm:
			user = User.objects.create(username=username,password=password)
			request.session['username'] = user.username
			return redirect('/index/')

def login(request):
	if request.session.get('username'):
		return redirect('/index/')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		if User.objects.filter(username=request.POST['username']).exists():
			user = User.objects.get(username=request.POST['username'])
			if user.password == request.POST['password']:
				request.session['username'] = user.username
				return redirect('/index/')
			else:
				return redirect('/')
		else:
			return redirect('/')
def logOut(request):
	try:
		del request.session['username']
	except Exception as e:
		pass
	return redirect('/')

def index(request):
    return render(request, 'index.html')

