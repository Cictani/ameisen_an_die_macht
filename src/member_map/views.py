from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import django_filters.rest_framework as rest_framework_filters
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D

from .models import DiscordUser
from .serializers import DiscordUserSerializer


class IDFilter(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        location = request.GET.get('location')
        distance = request.GET.get('distance')
        if distance is None:
            distance = 80
        if location is not None:
            location_array = location.split(',')
            x = location_array[0].strip()
            y = location_array[1].strip()
            pnt = GEOSGeometry('POINT({} {})'.format(x, y), srid=4326)
            return queryset.filter(location__distance_lte=(pnt, D(km=distance)))
        return queryset


# ViewSets define the view behavior.
class DiscordUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DiscordUser.objects.all()
    serializer_class = DiscordUserSerializer
    filter_backends = [rest_framework_filters.DjangoFilterBackend, IDFilter]
    filterset_fields = ['discord_id', 'username']


class UserMapView(TemplateView):
    template_name = "member_map/member_map.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['BING_API_KEY'] = settings.BING_API_KEY_CLIENT

        return context_data
