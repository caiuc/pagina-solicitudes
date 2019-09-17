from django.urls import path, re_path
from . import views

urlpatterns = [
    path('new/', views.NewActivity.as_view(), name='new_activity'),
    path('', views.ActivitiesList.as_view(), name='activities_list'),
    path('staff/',
         views.ActivitiesListStaff.as_view(),
         name='activities_list_staff'),
    path('staffall/',
         views.ActivitiesListStaffAll.as_view(),
         name='activities_list_staff_all'),
    re_path(r'^delete/(?P<pk>\d+)/$',
            views.ActivityDelete.as_view(),
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
    re_path(r'^notify/(?P<pk>\d+)/$',
            views.ActivityStatusNotification.as_view(),
            name='send_email'),
]
