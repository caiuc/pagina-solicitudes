from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.NewActivity.as_view(), name="new_activity"),
    path("", views.ActivitiesList.as_view(), name="activities_list"),
    path("staff/", views.ActivitiesListStaff.as_view(), name="activities_list_staff"),
    path("staffall/", views.ActivitiesListStaffAll.as_view(), name="activities_list_staff_all"),
    path("delete/<int:pk>/", views.ActivityDelete.as_view(), name="delete_activity"),
    path("edit/<int:pk>/", views.ActivityUpdate.as_view(), name="update_activity"),
    path("<int:pk>/", views.ActivityDetail.as_view(), name="activity_detail"),
    path("status/<int:pk>/", views.ActivityChangeState.as_view(), name="update_activity_status"),
    path("notify/<int:pk>/", views.ActivityStatusNotification.as_view(), name="send_email"),
    path("calendar/", views.Calendar.as_view(), name="calendar"),
]
