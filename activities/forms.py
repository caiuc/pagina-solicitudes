from django import forms
from activities.models import Activity
from activities.models import (Space, Equipment)


class ActivityFrom(forms.ModelForm):

    print(Space.objects.all())

    space = forms.ModelMultipleChoiceField(Space.objects.all())
    equipment = forms.ModelMultipleChoiceField(Equipment.objects.all())

    class Meta:
        model = Activity
        fields = [
            'name', 'description', 'space', 'equipment', 'date_start',
            'date_finish', 'in_charge'
        ]
