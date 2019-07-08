from django.urls import path, re_path
from . import views

urlpatterns = [
    path('new/', views.NewActivity.as_view(), name='new_activity'),
    path('', views.ActivitiesList.as_view(), name='activities_list'),
    re_path(r'^delete/(?P<pk>\d+)/$', views.ActivityDelte.as_view(), name='delete_activity'),
]
