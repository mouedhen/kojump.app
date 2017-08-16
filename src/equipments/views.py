# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render
from django.views import generic
from .models import Activity, SportDiscipline, Equipment, Institution
from django.http import HttpResponse, Http404
from django.core.serializers import serialize


class ActivityListView(generic.ListView):
    model = Activity
    context_object_name = 'activities'
    queryset = Activity.objects.filter(is_active=True)
    paginate_by = 6
    template_name = 'equipments/activity/list.html'


class ActivityDetailView(generic.DetailView):
    model = Activity
    template_name = 'equipments/activity/detail.html'
    context_object_name = 'activity'


class InstitutionDetailView(generic.DetailView):
    model = Institution
    template_name = 'equipments/institution/detail.html'
    context_object_name = 'institution'


class EquipmentDetailView(generic.DetailView):
    model = Equipment
    template_name = 'equipments/equipment/detail.html'
    context_object_name = 'equipment'


class ActivityInstitutionsAPI(generic.View):

    def get(self, request, activity_pk=1):
        activity = Activity.objects.get(id=activity_pk)
        if not activity.is_active:
            raise Http404('Activity don\'t exist')
        institutions = Institution.objects\
            .filter(equipments__disciplines__activity_id=activity_pk).distinct()
        geojson_data = {}
        results = []
        palette = ['#556270', '#4ECDC4', '#C7F464', '#FF6B6B', '#C44D58']
        icon = ['star', 'swimming', 'marker', 'golf', 'basketball']
        import random
        for institution in institutions:
            r = random.randint(0, 4)
            institution_json = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [institution.coordinates.x, institution.coordinates.y]
                },
                'properties': {
                    'id': institution.pk,
                    'thumbnail': institution.thumbnail.url,
                    'name': institution.name,
                    'slug': institution.slug,
                    'address': institution.address,
                    "marker-color": palette[r],
                    # "marker-size": "large",
                    "marker-symbol": icon[r]
                }
            }
            results.append(institution_json)
            geojson_data = {
                'type': 'FeatureCollection',
                'crs': {
                    'type': 'name',
                    'properties': {'name': 'EPSG:4326'}
                },
                'features': results
            }
        data = json.dumps(geojson_data)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


class InstitutionEquipmentsAPI(generic.View):

    def get(self, request, institution_pk):
        data = serialize('geojson', Equipment.objects.filter(institution__code=institution_pk),
                  geometry_field='gps_coordinates',
                  fields=('pk', 'code', 'name', 'slug', 'thumbnail', 'description'))

        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
