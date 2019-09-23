from django.db import models
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Budget(models.Model):
    """
    Deprecated.
    """

    required_people = models.PositiveIntegerField()
    directed_to = models.CharField(max_length=2000)
    directed_to_amount = models.PositiveIntegerField()
    required_money = models.PositiveIntegerField()


class Space(models.Model):
    """Physical space of activities
    """

    class Meta:
        verbose_name = 'Espacio'
        verbose_name_plural = 'Espacios'

    name = models.CharField(max_length=200, verbose_name='Nombre de espacio')
    description = models.CharField(max_length=2000,
                                   blank=True,
                                   null=True,
                                   verbose_name='Descripción de espacio')
    admin_required = models.BooleanField(
        verbose_name='¿Requiere de link de administración?')
    objects = models.Manager()

    def __str__(self):
        return self.name


class Equipment(models.Model):
    """Equipment to use in activities
    """

    class Meta:
        verbose_name = 'Equipamiento'
        verbose_name_plural = 'Equipamientos'

    name = models.CharField(max_length=200,
                            verbose_name='Nombre de equipamiento')
    objects = models.Manager()

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Space request of a space and objects
    """

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    APPROVED = 'A'
    REJECTED = 'R'
    PENDING = 'P'
    CANCELLED = 'C'
    PENDING_CAI = 'PC'
    PENDING_ADMIN = 'PA'

    VALID_STATES = ((APPROVED, 'Aprobada'), (REJECTED, 'Rechazada'),
                    (PENDING, 'Pendiente'), (CANCELLED, 'Cancelada'),
                    (PENDING_ADMIN, 'En revisión por Decanato'),
                    (PENDING_CAI, 'En revisión por CAi'))

    state = models.CharField(max_length=2,
                             choices=VALID_STATES,
                             default=PENDING_CAI,
                             verbose_name='Estado de la solicitud')
    name = models.CharField(max_length=200,
                            verbose_name='Nombre de la actividad')
    description = models.TextField(max_length=20000,
                                   verbose_name='Descripción de la actividad')
    space_1 = models.ForeignKey(Space,
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE,
                                related_name='space_1')
    space_2 = models.ForeignKey(Space,
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE,
                                related_name='space_2')
    space_3 = models.ForeignKey(Space,
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE,
                                related_name='space_3')
    equipment = models.ForeignKey(Equipment,
                                  blank=True,
                                  null=True,
                                  on_delete=models.CASCADE)
    date_start = models.DateTimeField(blank=False,
                                      verbose_name='Fecha de inicio')
    date_finish = models.DateTimeField(blank=False,
                                       verbose_name='Fecha de término')
    in_charge = models.CharField(max_length=200,
                                 verbose_name='Correo de encargado')
    admin_link = models.URLField(
        blank=True, null=True, verbose_name='Link a administración del campus')
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def valid_spaces(self):
        spaces = [self.space_1, self.space_2, self.space_3]
        spaces = list(
            map(lambda space: str(space),
                filter(lambda space: space is not None, spaces)))
        spaces = ', '.join(spaces)
        return spaces

    def __str__(self):
        return self.name
