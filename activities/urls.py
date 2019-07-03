from django.urls import path

from . import views

urlpatterns = [
    path('new_activity/', views.NewActivity.as_view(), name='new_activity'),
]
