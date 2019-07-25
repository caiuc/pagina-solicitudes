from django import forms
from activities.models import Activity
from activities.models import (Space, Equipment)
from accounts.models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class ActivityFrom(forms.ModelForm):

    # special fields used for personalization
    space = forms.ModelChoiceField(Space.objects.all(),
                                   required=False,
                                   label='Espacio')
    equipment = forms.ModelChoiceField(Equipment.objects.all(),
                                       required=False,
                                       label='Equipamiento')
    date_start = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
                                     label='Fecha de inicio')
    date_finish = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
                                      label='Fecha de término')
    in_charge = forms.EmailField(label='Correo del encargado')

    def __init__(self, user=None, *args, **kwargs):
        super(ActivityFrom, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['creator'] = forms.ModelChoiceField(
            User.objects.all(), widget=forms.HiddenInput(), initial=self.user)

    class Meta:
        model = Activity
        fields = [
            'name', 'description', 'space', 'equipment', 'date_start',
            'date_finish', 'in_charge', 'creator'
        ]
        labels = {
            'name': 'Nombre de la actividad',
            'description': 'Descripción',
            'date_start': 'Fecha de inicio',
            'date_finish': 'Fecha de término',
            'in_charge': 'Correo del encargado',
            'space': 'Espacio',
            'equipment': 'Equipamiento'
        }


class NotificationForm(forms.Form):

    subject = forms.CharField(label='Título del correo')
    body = forms.CharField(label='Cuerpo', widget=forms.Textarea)

    @staticmethod
    def send_email(subject, body, mailer, emailed):
        html_content = render_to_string('emails/activity_status.html',
                                        {'body': body})
        text_content = strip_tags(html_content)
        send_mail(subject, text_content, mailer, emailed, html_message=html_content)