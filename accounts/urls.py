from django.urls import path, re_path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    re_path(r'^update/(?P<pk>\d+)/$',
            views.ProfileUpdate.as_view(),
            name='update_profile'),
]