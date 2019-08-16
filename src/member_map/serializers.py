from rest_framework import serializers

from .models import DiscordUser


class DiscordUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DiscordUser
        fields = ['id', 'discord_id', 'username', 'location']