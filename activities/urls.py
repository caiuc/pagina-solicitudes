from django.urls import path, re_path
from . import views

urlpatterns = [
    path('new/', views.NewActivity.as_view(), name='new_activity'),
    path('', views.ActivitiesList.as_view(), name='activities_list'),
    path('staff/',
         views.ActivitiesListStaff.as_view(),
         name='activities_list_staff'),
    re_path(r'^delete/(?P<pk>\d+)/$',
            views.ActivityDelte.as_view(),
            name='delete_activity'),
    re_path(r'^edit/(?P<pk>\d+)/$',
            views.ActivityUpdate.as_view(),
            name='update_activity'),
    re_path(r'^(?P<pk>\d+)/$',
            views.ActivityDetail.as_view(),
            name='activity_detail'),
    re_path(r'^status/(?P<pk>\d+)/$',
            views.ActivityChangeState.as_view(),
            name='update_activity_status'),
]
