from django import forms
from activities.models import Activity
from activities.models import (Space, Equipment)
from accounts.models import Profile


class ActivityFrom(forms.ModelForm):

    space = forms.ModelMultipleChoiceField(Space.objects.all())
    equipment = forms.ModelMultipleChoiceField(Equipment.objects.all())
    date_start = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    date_finish = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    in_charge = forms.EmailField()

    def __init__(self, user=None, *args, **kwargs):
        super(ActivityFrom, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['creator'] = forms.ModelChoiceField(
            Profile.objects.all(),
            widget=forms.HiddenInput(),
            initial=self.user)

    class Meta:
        model = Activity
        fields = [
            'name', 'description', 'space', 'equipment', 'date_start',
            'date_finish', 'in_charge', 'creator'
        ]
