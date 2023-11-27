from django.core.mail import send_mail

send_mail(
    "Test de Plataforma de Solicitudes",
    "Mensaje de prueba.",
    "solicitudes@cai.cl",
    ["soctest@agucova.dev"],
    fail_silently=False,
)