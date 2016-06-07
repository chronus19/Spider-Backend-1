from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
      #url(r'^$', views.loginpage , name='LoginPage'),
      #url(r'^register/$', views.register),
      url(r'^$', TemplateView.as_view(template_name="select.html")),
      url(r'^add/$', views.add_student),
      url(r'^view/$', views.view_student),
      url(r'^edit/$', views.edit_student),
      ]
