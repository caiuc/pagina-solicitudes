from django.conf import settings
from django.db import models

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class Space(models.Model):
    """Physical space of activities"""

    name = models.CharField(max_length=200, verbose_name="Nombre de espacio")
    description = models.CharField(
        max_length=2000, blank=True, null=False, verbose_name="Descripción de espacio", default=""
    )
    admin_required = models.BooleanField(verbose_name="¿Requiere de link de administración?")
    color = models.CharField(max_length=20, default="rgb(0,0,0)")
    objects = models.Manager()

    class Meta:
        verbose_name = "Espacio"
        verbose_name_plural = "Espacios"

    def __str__(self):
        return self.name


class Equipment(models.Model):
    """Equipment to use in activities"""

    name = models.CharField(max_length=200, verbose_name="Nombre de equipamiento")
    objects = models.Manager()

    class Meta:
        verbose_name = "Equipamiento"
        verbose_name_plural = "Equipamientos"

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Space request of a space and objects"""

    APPROVED = "A"
    REJECTED = "R"
    PENDING = "P"
    CANCELLED = "C"
    PENDING_CAI = "PC"
    PENDING_ADMIN = "PA"

    VALID_STATES = (
        (APPROVED, "Aprobada"),
        (REJECTED, "Rechazada"),
        (PENDING, "Pendiente"),
        (CANCELLED, "Cancelada"),
        (PENDING_ADMIN, "En revisión por Decanato"),
        (PENDING_CAI, "En revisión por CAi"),
    )

    state = models.CharField(
        max_length=2,
        choices=VALID_STATES,
        default=PENDING_CAI,
        verbose_name="Estado de la solicitud",
    )
    name = models.CharField(max_length=200, verbose_name="Nombre de la actividad")
    description = models.TextField(max_length=20000, verbose_name="Descripción de la actividad", blank=True, null=False)
    space_1 = models.ForeignKey(Space, blank=True, null=True, on_delete=models.CASCADE, related_name="space_1")
    space_2 = models.ForeignKey(Space, blank=True, null=True, on_delete=models.CASCADE, related_name="space_2")
    space_3 = models.ForeignKey(Space, blank=True, null=True, on_delete=models.CASCADE, related_name="space_3")
    equipment = models.ForeignKey(Equipment, blank=True, null=True, on_delete=models.CASCADE)
    date_start = models.DateTimeField(blank=False, verbose_name="Fecha de inicio")
    date_finish = models.DateTimeField(blank=False, verbose_name="Fecha de término")
    in_charge = models.EmailField(max_length=200, verbose_name="Correo de encargado")
    participants_amount = models.PositiveIntegerField(default=0, verbose_name="Número de participantes")
    admin_link = models.URLField(blank=True, null=False, verbose_name="Link a administración del campus", default="")
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"

    def __str__(self):
        return self.name

    @staticmethod
    def format_time_calendar(datetime_instance):
        # 2019-09-16T16:00:00
        return datetime_instance.strftime("%Y-%m-%dT%H:%M:%S")

    @property
    def activity_format_calendar(self):
        activities = []
        for space in [self.space_1, self.space_2, self.space_3]:
            if space != "" and space is not None:
                event = {
                    "title": str(self.name),
                    "start": Activity.format_time_calendar(self.date_start),
                    "end": Activity.format_time_calendar(self.date_finish),
                    "space": space,
                }
                activities.append(event)
        return activities

    @property
    def valid_spaces(self):
        spaces = [self.space_1, self.space_2, self.space_3]
        spaces = list(
            map(
                str,
                filter(lambda space: space is not None, spaces),
            )
        )
        spaces = ", ".join(spaces)
        return spaces


class Coordinator(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    objects = models.Manager()

    class Meta:
        verbose_name = "Coordinador CAi"
        verbose_name_plural = "Coordinador CAi (solo tener 1)"

    def __str__(self):
        return self.name
