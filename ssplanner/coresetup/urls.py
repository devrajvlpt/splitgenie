# # URLconf
from django.conf.urls import url
from views.login import LoginView, LogoutView
from views.register import (
   RegisterView,
   RegisterDetailView,
)

urlpatterns = [
   # URL from Login View
   url('login', LoginView.as_view(), name='login'),
   url('logout', LogoutView.as_view(), name='login'),
   url('users', RegisterView.as_view(), name='users'),   
   url('userlist', RegisterDetailView.as_view(), name='userlist'),   
]
