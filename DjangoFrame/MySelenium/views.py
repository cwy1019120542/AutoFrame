from django.shortcuts import render,redirect,reverse
from . import forms,models
def login(request):
	message=None
	form=forms.LoginForm()
	if request.method == 'POST':
		form=forms.LoginForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user_same=models.User.objects.filter(username=username)
			if user_same:
				if password == user_same[0].password:
					return redirect(reverse('MySelenium:add_table',kwargs={'name':username}))
				else:
					message = '密码不正确'
			else:
				message = '账号不存在'
	context_dict = {'form':form,'message':message}
	return render(request,'MySelenium/login.html',context_dict)
def add_table(request,name):
	message=''
	form=forms.AddForm()
	if request.method == 'POST':
		form=forms.AddForm(request.POST)
		if form.is_valid():
			table=models.Table.objects.create()
			table.name=form.cleaned_data['name']
			table.day_before=form.cleaned_data['day_before']
			for i in range(1,31):
				if form.cleaned_data['operate_name{}'.format(i)]:
					rough_lists=eval('[form.cleaned_data["operate_name{0}"],form.cleaned_data["element1_name{0}"],form.cleaned_data["element1_value{0}"],form.cleaned_data["element2_name{0}"],form.cleaned_data["element2_value{0}"],form.cleaned_data["extra{0}"],form.cleaned_data["wait_time{0}"]]'.format(i))
					exec('table.operate{}=str([k for k in rough_lists if k!=""])'.format(i))
			table.save()
			message='{}添加成功'.format(table.name)
	context_dict={'form':form,'message':message}
	return render(request,'MySelenium/addtable.html',context_dict)

