from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

STUDENT = "S"
TEACHER = "T"
FUNCTIONARY = "F"
CAI = "C"

USER_TYPE = ((STUDENT, "Estudiante"), (TEACHER, "Profesor"), (FUNCTIONARY, "Funcionario"), (CAI, "CAi"))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=50, verbose_name="RUT")
    phone = models.CharField(max_length=50, verbose_name="Número telefónico")
    profile_type = models.CharField(max_length=2, choices=USER_TYPE, default=STUDENT, verbose_name="Tipo de usuario")
    administrative = models.BooleanField(default=False, verbose_name="¿Parte de administración?")
    objects = models.Manager()

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
