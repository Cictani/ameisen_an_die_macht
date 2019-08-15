from django.contrib.gis import admin
from .models import DiscordUser


@admin.register(DiscordUser)
class ShopAdmin(admin.OSMGeoAdmin):
    list_display = ('discord_id', 'username', 'location')
