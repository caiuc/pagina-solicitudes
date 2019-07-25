from django.db import models
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Budget(models.Model):

    required_people = models.PositiveIntegerField()
    directed_to = models.CharField(max_length=2000)
    directed_to_amount = models.PositiveIntegerField()
    required_money = models.PositiveIntegerField()


class Space(models.Model):
    """Physical space of activities
    """

    name = models.CharField(max_length=200)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Equipment(models.Model):
    """Equipment to use in activities
    """

    name = models.CharField(max_length=200)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Space request of a space and objects
    """

    APPROVED = 'A'
    REJECTED = 'R'
    PENDING = 'P'
    CANCELLED = 'C'
    PENDING_CAI = 'PC'
    PENDING_ADMIN = 'PA'

    VALID_STATES = ((APPROVED, 'Aprobada'), (REJECTED, 'Rechazada'),
                    (PENDING, 'Pendiente'), (CANCELLED, 'Cancelada'),
                    (PENDING_ADMIN, 'Pendiente por administración'),
                    (PENDING_CAI, 'Pendiente por CAi'))

    state = models.CharField(max_length=2,
                             choices=VALID_STATES,
                             default=PENDING)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=20000)
    space = models.ForeignKey(Space,
                              blank=True,
                              null=True,
                              on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment,
                                  blank=True,
                                  null=True,
                                  on_delete=models.CASCADE)
    date_start = models.DateTimeField(blank=False)
    date_finish = models.DateTimeField(blank=False)
    in_charge = models.CharField(max_length=200)
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
