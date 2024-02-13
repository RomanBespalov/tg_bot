from django.contrib import admin

from admin_panel.models import Clients, BroadcastMessage


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'username',
        'first_name',
        'last_name',
    )


@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'text',
        'get_recipients_display',
        'pub_date',
    )

    def get_recipients_display(self, obj):
        return ', '.join(
            [recipients.username for recipients in obj.recipients.all()]
        )
    get_recipients_display.short_description = 'Пользователи'
