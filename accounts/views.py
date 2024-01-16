from django.urls import reverse_lazy
from django.views import generic
from .forms import RegistrationForm, ProfileForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class TutorialView(generic.CreateView):
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy("login")
    template_name = "activities/tutorial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_name"] = "Nuevo usuario"
        context["button"] = "Crear"
        return context

class SignUp(generic.CreateView):
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy("login")
    template_name = "activities/generic_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_name"] = "Nuevo usuario"
        context["button"] = "Crear"
        return context


class ProfileUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy("activities_list")
    template_name = "activities/generic_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_name"] = "Completar información de usuario"
        context["button"] = "Completar"
        return context
