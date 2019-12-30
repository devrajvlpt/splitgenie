# # URLconf
from django.conf.urls import url
from coresetup.views.login import LoginView, LogoutView
from coresetup.views.register import (
   RegisterView,
   RegisterDetailView,
)
from coresetup.views.topic import (
   TopicView
)
from coresetup.views.splitz import (
   SplitzView,
   SplitzDetailView
)
from coresetup.views.friends import (
   FriendView
)
from coresetup.views.login import (
   ApplicationListView,
   SocialAuthAssociationView
)
from coresetup.views.payments import (
   OrderInterfaceView
)
# from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

urlpatterns = [
   # URL from Login View
   url('login',      LoginView.as_view(), name='login'),
   url('logout',     LogoutView.as_view(), name='login'),
   url('users',      RegisterView.as_view(), name='users'),
   url('userlist',   RegisterDetailView.as_view(), name='userlist'),
   url('topic',      TopicView.as_view(), name='topic'),
   path('splitz',     SplitzView.as_view(), name='splitz'),
   path('splitz/<int:pk>',     SplitzDetailView.as_view(), name='splitzdetail'),
   url('listfriend', FriendView.as_view(), name='listfriend'),
   url('createorder', OrderInterfaceView.as_view(), name='listfriend'),
   url(r'^applications', ApplicationListView.as_view()),
   url(r'^socialauth', SocialAuthAssociationView.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
