from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    STUDENT = 'S'
    TEACHER = 'T'
    FUNCTIONARY = 'F'
    CAI = 'C'

    USER_TYPE = ((STUDENT, 'Estudiante'), (TEACHER, 'Profesor'),
                 (FUNCTIONARY, 'Funcionario'), (CAI, 'CAi'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    profile_type = models.CharField(max_length=2,
                                    choices=USER_TYPE,
                                    default=STUDENT)
    administrative = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()