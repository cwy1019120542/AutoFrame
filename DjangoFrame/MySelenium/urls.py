from django.conf.urls import url
from . import views
app_name='MySelenium'
urlpatterns=[
			url(r'^login/$',views.login,name='login'),
			url(r'^(?P<name>\w+)/add/$',views.add_table,name='add_table'),
				]