from django import forms
from activities.models import Activity
from activities.models import (Space, Equipment)
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (From, To, PlainTextContent, HtmlContent, Mail)
from django.conf import settings

class ActivityForm(forms.ModelForm):

    # special fields used for personalization
    space = forms.ModelChoiceField(
        Space.objects.all(),
        required=False,
        label='Espacio',
    )

    name = forms.CharField(label='Nombre de la actividad',
                           widget=forms.TextInput(attrs={'class': 'input'}),
                           required=True)

    description = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={'class': 'textarea'}),
        required=True)

    equipment = forms.ModelChoiceField(Equipment.objects.all(),
                                       required=False,
                                       label='Equipamiento',
                                       widget=forms.Select(attrs={'class': 'select'}))

    space = forms.ModelChoiceField(Space.objects.all(),
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

    def __init__(self, user=None, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
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

    subject = forms.CharField(label='Título del correo',
                              widget=forms.TextInput(attrs={'class': 'input'}))
    body = forms.CharField(label='Cuerpo',
                           widget=forms.Textarea(attrs={'class': 'textarea'}))

    @staticmethod
    def send_email(subject, body, mailer, emailed):
        html_content = render_to_string('emails/activity_status.html',
                                        {'body': body})
        text_content = strip_tags(html_content)

        # sendgrid_client = SendGridAPIClient(
        #     api_key=settings.SENDGRID_API_KEY)
        # from_email = From('cai@caiuc.cl')
        # to_email = To('rihanuch@uc.cl')
        # subject = 'Sending with Twilio SendGrid is Fun'
        # plain_text_content = PlainTextContent(
        #     'and easy to do anywhere, even with Python'
        # )
        # html_content = HtmlContent(
        #     '<strong>and easy to do anywhere, even with Python</strong>'
        # )
        # message = Mail(from_email, to_email, subject, plain_text_content, html_content)
        # response = sendgrid_client.send(message=message)

        send_mail(subject,
                  text_content,
                  mailer,
                  emailed,
                  fail_silently=False,
                  html_message=html_content)
