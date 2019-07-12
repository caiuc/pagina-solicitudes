from activities.forms import ActivityFrom
from activities.models import Activity
from accounts.models import Profile
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


# Limits the permissions of viewing and modifying any of the activities that
# the user is not the owner
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

    form_class = ActivityFrom
    success_url = reverse_lazy('home')
    template_name = 'activities/new_activity.html'

    def get(self, request):
        template = loader.get_template('activities/new_activity.html')
        form = ActivityFrom(request.user)
        return HttpResponse(template.render({'form': form}, request))


class ActivitiesList(LoginRequiredMixin, generic.ListView):

    template_name = 'activities/activities_list.html'
    model = Activity

    def get_queryset(self):
        creator = self.request.user
        queryset = Activity.objects.filter(creator=creator)
        return queryset


class ActivityDelte(LoginRequiredMixin, PermissionMixin, generic.DeleteView):

    model = Activity
    template_name = 'activities/activity_confirm_delete.html'
    success_url = reverse_lazy('activities_list')


class ActivityUpdate(LoginRequiredMixin, PermissionMixin, generic.UpdateView):

    model = Activity
    fields = [
        'name', 'description', 'space', 'equipment', 'date_start',
        'date_finish', 'in_charge'
    ]
    template_name = 'activities/new_activity.html'
    success_url = reverse_lazy('activities_list')


class ActivityDetail(LoginRequiredMixin, PermissionMixin, generic.DetailView):

    model = Activity
    template_name = 'activities/detailed_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context