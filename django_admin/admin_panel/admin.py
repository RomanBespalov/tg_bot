from django.contrib import admin

from admin_panel.models import Clients


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
    )
