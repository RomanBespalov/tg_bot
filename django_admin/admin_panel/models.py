from django.db import models


class Clients(models.Model):
    """Модель клиентов."""
    user_id = models.PositiveIntegerField(
        verbose_name='ID пользователя в телеграмм',
        blank=True,
        null=True,
    )
    username = models.CharField(
        max_length=100,
        verbose_name='Ник пользователя',
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя пользователя',
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия пользователя',
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['id']
        app_label = 'admin_panel'


class BroadcastMessage(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='название рассылки',
    )
    text = models.TextField(
        verbose_name='текст рассылки',
    )
    recipients = models.ManyToManyField(
        Clients,
        verbose_name='получатели',
        related_name='recipients',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата отправки',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['-id']

    def __str__(self):
        return self.name
