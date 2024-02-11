from django.db import models


class Clients(models.Model):
    """Модель клиентов."""
    username = models.CharField(
        max_length=100,
    )
    first_name = models.CharField(
        max_length=100,
    )
    last_name = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['id']
        app_label = 'admin_panel'


# class Broadcast(models.Model):
#     pass
