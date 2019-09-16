from django import forms
from activities.models import Activity
from activities.models import (Space, Equipment)
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.validators import URLValidator


class ActivityForm(forms.ModelForm):

    # special fields used for personalization
    name = forms.CharField(label='Nombre de la actividad',
                           widget=forms.TextInput(attrs={'class': 'input'}),
                           required=True)

    description = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={'class': 'textarea'}),
        required=True)

    equipment = forms.ModelChoiceField(
        Equipment.objects.all(),
        required=False,
        label='Equipamiento',
        widget=forms.Select(attrs={'class': 'select'}))

    space = forms.ModelChoiceField(
        Space.objects.all(),
        required=False,
        label='Espacio',
        widget=forms.Select(attrs={'class': 'select'}))

    date_start = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        label='Fecha de inicio',
        widget=forms.DateInput(attrs={
            'class': 'input',
            'placeholder': 'dd/mm/aaaa hh:mm'
        }),
        required=True)

    date_finish = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        label='Fecha de término',
        widget=forms.DateInput(attrs={
            'class': 'input',
            'placeholder': 'dd/mm/aaaa hh:mm'
        }),
        required=True)

    in_charge = forms.EmailField(
        label='Correo del encargado',
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'ejemplo@correo.com'
        }),
        required=True)

    admin_link = forms.URLField(
        label='Link a solicitud de administración del campus.',
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'Este link es necesario para algunas áreas (detalladas más abajo).'
            }),
        required=False,
    )

    required_links = ['hola']

    def __init__(self, user=None, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['creator'] = forms.ModelChoiceField(
            User.objects.all(), widget=forms.HiddenInput(), initial=self.user)

    def clean_admin_link(self):
        validate = URLValidator(message='Se debe rellenar con un link válido.')

        space_instance = Space.objects.get(pk=int(self.data.get('space')))

        if space_instance.admin_required:
            validate(self.data.get('admin_link'))

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

    subject = forms.CharField(label='Título del correo',
                              widget=forms.TextInput(attrs={'class': 'input'}))
    body = forms.CharField(label='Cuerpo',
                           widget=forms.Textarea(attrs={'class': 'textarea'}))

    @staticmethod
    def send_email(subject, body, mailer, emailed):
        html_content = render_to_string('emails/activity_status.html',
                                        {'body': body})
        text_content = strip_tags(html_content)

        send_mail(subject,
                  text_content,
                  mailer,
                  emailed,
                  fail_silently=False,
                  html_message=html_content)
