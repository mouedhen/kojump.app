"""kojump URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

# TODO create the home page
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

from equipments.views import (
    ActivityListView,
    ActivityDetailView,
    InstitutionDetailView,
    EquipmentDetailView,
    ActivityInstitutionsAPI,
    InstitutionEquipmentsAPI,
)
from accounts.views import UserRegistrationView
from django.views.decorators.cache import cache_page


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', ActivityListView.as_view(), name='activities'),
    url(r'^(?P<page>\d+)$', ActivityListView.as_view(), name='activities'),
    url(r'^activities/(?P<pk>[0-9]+)$', ActivityDetailView.as_view(), name='activity-detail'),
    url(r'^institutions/(?P<pk>[0-9]+)$', InstitutionDetailView.as_view(), name='institution-detail'),
    url(r'^equipments/(?P<pk>[0-9]+)$', EquipmentDetailView.as_view(), name='equipment-detail'),
    # accounts url
    url(r'^register/$', UserRegistrationView.as_view(), name='register'),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/login/'}, name='logout'),
    # APIs url
    url(r'^api/activities/(?P<activity_pk>\d+)/institutions', cache_page(60 * 15)(ActivityInstitutionsAPI.as_view()),
        name='api.activity.institutions'),
    url(r'^api/institutions/(?P<institution_pk>\d+)/equipments', cache_page(60 * 15)(InstitutionEquipmentsAPI.as_view()),
        name='api.activity.institutions'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)