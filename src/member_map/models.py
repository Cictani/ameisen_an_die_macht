from django.contrib.gis.db import models

# Create your models here.


class DiscordUser(models.Model):
    discord_id = models.CharField(
        db_index=True,
        max_length=50,
        unique=True,

    )
    username = models.CharField(
        max_length=100
    )
    location = models.PointField()
