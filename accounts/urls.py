from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("update/<int:pk>/", views.ProfileUpdate.as_view(), name="update_profile"),
    path("tutorial/", views.TutorialView.as_view(),name="tutorial"),
]
