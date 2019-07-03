from .forms import ActivityFrom
from django.views import generic
from django.urls import reverse_lazy


class NewActivity(generic.CreateView):
    form_class = ActivityFrom
    success_url = reverse_lazy('home')
    template_name = 'new_activity.html'