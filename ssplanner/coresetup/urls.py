# # URLconf
from django.conf.urls import url
from views.login import LoginView, LogoutView
from views.register import (
   RegisterView,
   RegisterDetailView,
)
from views.topic import (
   TopicView
)
from views.splitz import (
   SplitzView
)
from views.friends import (
   FriendView
)

# from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
   # URL from Login View
   url('login',      LoginView.as_view(), name='login'),
   url('logout',     LogoutView.as_view(), name='login'),
   url('users',      RegisterView.as_view(), name='users'),
   url('userlist',   RegisterDetailView.as_view(), name='userlist'),
   url('topic',      TopicView.as_view(), name='topic'),
   url('splitz',     SplitzView.as_view(), name='splitz'),
   url('listfriend', FriendView.as_view(), name='listfriend'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)