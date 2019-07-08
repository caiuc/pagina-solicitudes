from activities.forms import ActivityFrom
from activities.models import Activity
from accounts.models import Profile
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


# limita permisos para el usuario creador
class PermissionMixin(object):
    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)
        if not obj.creator.id == self.request.user.id:
            raise PermissionDenied()
        else:
            return obj


# LoginRequiredMixin acts as a decorator to make a login required
# for certain pages
class NewActivity(LoginRequiredMixin, PermissionMixin, generic.CreateView):
    def get(self, request):
        template = loader.get_template('activities/new_activity.html')
        form = ActivityFrom(request.user)
        return HttpResponse(template.render({'form': form}, request))

    form_class = ActivityFrom
    success_url = reverse_lazy('home')
    template_name = 'activities/new_activity.html'


class ActivitiesList(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        creator = Profile.objects.get(pk=self.request.user.id)
        queryset = Activity.objects.filter(creator=creator)
        return queryset

    template_name = 'activities/activities_list.html'
    model = Activity


class ActivityDelte(LoginRequiredMixin, PermissionMixin, generic.DeleteView):

    model = Activity
    template_name = 'activities/activity_confirm_delete.html'
    success_url = reverse_lazy('activities_list')
