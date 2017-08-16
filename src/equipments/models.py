# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

from core.models import SluggedModel, DescribedModel, TimeStampedModel, ActivatedModel
from schedule.models import TimeInterval
from geolocations.models import GeoLocation


@python_2_unicode_compatible
class EquipmentCategoryFamily(SluggedModel, TimeStampedModel):

    class Meta:
        verbose_name = _('famille d\'équipements')
        verbose_name_plural = _('famille d\'équipements')
        unique_together = ('label', 'slug',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class EquipmentCategory(SluggedModel, TimeStampedModel):

    family = models.ForeignKey(EquipmentCategoryFamily, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        verbose_name = _('catégorie d\'équipements')
        verbose_name_plural = _('catégories d\'équipements')
        unique_together = ('label', 'slug',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class Activity(SluggedModel, DescribedModel, TimeStampedModel, ActivatedModel):

    thumbnail = models.ImageField(_('image'), blank=True, null=True,
                                  default='default-activity-thumbnail.png',
                                  upload_to='activity/thumbnail')
    # TODO set a logo foreach activity
    # map_logo = models.ImageField(_('map logo'), blank=True, null=True,
    #                              default='default-activity-map-logo.png',
    #                              upload_to='activity/map_logo')

    class Meta:
        verbose_name = _('activité sportive')
        verbose_name_plural = _('activités sportives')
        unique_together = ('label', 'slug',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class SportDiscipline(SluggedModel, TimeStampedModel, ActivatedModel):

    reference = models.PositiveIntegerField(_('reférence unique'), primary_key=True, default=0)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='sports_disciplines')

    class Meta:
        verbose_name = _('discipline sportive')
        verbose_name_plural = _('disciplines sportives')
        unique_together = ('label', 'slug',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class ActivityLevel(SluggedModel):

    class Meta:
        verbose_name = _('level de l\'activité')
        verbose_name_plural = _('levels des activités')
        unique_together = ('label', 'slug',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class SiteEnvironment(SluggedModel):

    class Meta:
        verbose_name = _('environnement du site')
        verbose_name_plural = _('environnements des sites')
        unique_together = ('label', 'slug',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class SiteGround(SluggedModel):

    class Meta:
        verbose_name = _('type du sol')
        verbose_name_plural = _('types des sols')
        unique_together = ('label', 'slug',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class UsageType(SluggedModel):

    class Meta:
        verbose_name = _('type d\'utilisation')
        verbose_name_plural = _('types d\'utilisation')
        unique_together = ('label', 'slug',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class EquipmentTarget(SluggedModel):

    class Meta:
        verbose_name = _('publique cible')
        verbose_name_plural = _('publique cibles')
        unique_together = ('label', 'slug',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class ManagerCategory(SluggedModel):

    IS_PUBLIC_CHOICES = (
        ('NOT_DEFINED', _('non définie')),
        ('IS_PUBLIC', _('oui')),
        ('NOT_PUBLIC', _('non')),
    )

    is_public = models.CharField(_('est publique ?'), max_length=15, choices=IS_PUBLIC_CHOICES, default='NOT_DEFINED')

    class Meta:
        verbose_name = _('categorie du gestionnaire')
        verbose_name_plural = _('categories des gestionnaires')
        unique_together = ('label', 'slug',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class SpecialInstitution(SluggedModel):

    class Meta:
        verbose_name = _('institution spéciale')
        verbose_name_plural = _('institutions spéciales')
        unique_together = ('label', 'slug',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class Department(SluggedModel):
    code = models.CharField(_('code'), max_length=15, primary_key=True)

    class Meta:
        verbose_name = _('département')
        verbose_name_plural = _('départements')

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class Commune(SluggedModel):
    code_insee = models.CharField(_('code INSEE'), max_length=15, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='communes', blank=True)

    class Meta:
        verbose_name = _('commune')
        verbose_name_plural = _('communes')

    def __str__(self):
        return self.label


# TODO never repeat your self
@python_2_unicode_compatible
class Institution(models.Model):
    # General
    code = models.CharField(_('code'), max_length=20, primary_key=True)
    name = models.CharField(_('nom'), max_length=254)
    slug = models.SlugField(_('slug'), max_length=254)
    thumbnail = models.ImageField(_('thumbnail'), blank=True, null=True,
                                  default='default-institution-thumbnail.png',
                                  upload_to='institutions/thumbnail')
    special_institution = models.ForeignKey(SpecialInstitution, on_delete=models.CASCADE, related_name='institutions',
                                            blank=True)
    # Address
    street_number = models.CharField(_('num. rue'), max_length=10, blank=True, null=True)
    street_name = models.CharField(_('nom rue'), max_length=100, blank=True)
    common_name = models.CharField(_('nom commun'), max_length=80, blank=True)
    postal_code = models.CharField(_('code postal'), max_length=10, blank=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='institution', blank=True)
    # Additional information
    have_internet = models.BooleanField(_('a internet ?'), blank=True, default=False)
    number_covers = models.IntegerField(_('nombre de couvers'), blank=True, default=0, null=True)
    number_beds = models.IntegerField(_('nombre de lits'), blank=True, default=0, null=True)
    number_parking_spaces = models.IntegerField(_('nombre de places de parking'), blank=True, default=0, null=True)
    # Disabled person accessibility information
    is_accessible_for_hand_m = models.BooleanField(_('accéssible aux handicapés à mobilité réduite ?'),
                                                   default=False)
    is_accessible_for_hand_s = models.BooleanField(_('accéssible aux handicapés sensoriaux ?'), default=False)
    number_parking_hn_spaces = models.IntegerField(_('nombre de places de parking pour les personnes handicapés'),
                                                   blank=True, default=0, null=True)
    # Transport information
    have_metro = models.BooleanField(_('a métro ?'), blank=True, default=False)
    have_bus = models.BooleanField(_('a autobus ?'), blank=True, default=False)
    have_tramway = models.BooleanField(_('a tramway ?'), blank=True, default=False)
    have_train = models.BooleanField(_('a train ?'), blank=True, default=False)
    have_boat = models.BooleanField(_('a bateau ?'), blank=True, default=False)
    have_other_transport = models.BooleanField(_('a transport (autre) ?'), blank=True, default=False)
    # Administration
    is_active = models.BooleanField(_('est actif ?'), default=False)
    # Important dates
    created = models.DateTimeField(_('date de création'), auto_now_add=True)
    modified = models.DateTimeField(_('date de modification'), auto_now=True)

    class Meta:
        verbose_name = _('institution')
        verbose_name_plural = _('institutions')

    def __str__(self):
        return self.name

    @property
    def coordinates(self):
        return self.equipments.first().gps_coordinates

    @property
    def address(self):
        return '{} {} - {} {}'.format(self.street_number, self.street_name, self.postal_code, self.commune.department)


# TODO never repeat your self
@python_2_unicode_compatible
class Equipment(GeoLocation):
    # General
    code = models.CharField(_('code'), max_length=12)
    name = models.CharField(_('nom'), max_length=254)
    slug = models.CharField(_('slug'), max_length=254)
    thumbnail = models.ImageField(_('thumbnail'), blank=True, null=True,
                                  default='default-equipment-thumbnail.png',
                                  upload_to='equipments/thumbnail')
    description = models.TextField(_('description'), blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE,
                                    related_name='equipments', blank=True, null=True)
    # Management
    owner_category = models.ForeignKey(ManagerCategory, on_delete=models.SET_NULL,
                                       related_name='owned_equipment', blank=True, null=True)
    manager_category = models.ForeignKey(ManagerCategory, on_delete=models.SET_NULL,
                                         related_name='managed_equipment', blank=True, null=True)
    # Category
    category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL,
                                 related_name='equipments', blank=True, null=True)
    # Additional category information
    is_erp_cts = models.BooleanField(_('Chapitau tente ?'), default=False, blank=True)
    is_erp_ref = models.BooleanField(_('Etablissement flottant ?'), default=False, blank=True)
    is_erp_l = models.BooleanField(_('Salle polyvalente ?'), default=False, blank=True)
    is_erp_n = models.BooleanField(_('Restaurant et débit de boisson ?'), default=False, blank=True)
    is_erp_o = models.BooleanField(_('Hôtel ?'), default=False, blank=True)
    is_erp_oa = models.BooleanField(_('Hôtel restaurant d\'altitude ?'), default=False, blank=True)
    is_erp_p = models.BooleanField(_('Salle de danse et jeux ?'), default=False, blank=True)
    is_erp_pa = models.BooleanField(_('Etablissement en plein air ?'), default=False, blank=True)
    is_erp_r = models.BooleanField(_('Enseignement et colo ?'), default=False, blank=True)
    is_erp_rpe = models.BooleanField(_('PE ?'), default=False, blank=True)
    is_erp_sg = models.BooleanField(_('Structure gonflable ?'), default=False, blank=True)
    is_erp_x = models.BooleanField(_('Etablissement sportif couvert ?'), default=False, blank=True)
    # Specification
    have_showers = models.BooleanField(_('a douche ?'), default=False, blank=True)
    have_lights = models.BooleanField(_('a lumière ?'), default=False, blank=True)
    tribune_places = models.IntegerField(_('nombre de places dans la tribune'), default=0, blank=True)
    ground = models.ForeignKey(SiteGround, on_delete=models.SET_NULL,
                               related_name='equipments', blank=True, null=True)
    environment = models.ForeignKey(SiteEnvironment, on_delete=models.SET_NULL,
                                    blank=True, null=True)
    have_heated_cloakroom = models.BooleanField(_('a vestiaires chauffées ?'), default=False, blank=True)
    corridors_number = models.IntegerField(_('nombre de coulloir'), default=0, blank=True, null=True)
    # Utils
    is_always_open = models.BooleanField(_('7d/7d - 24h/24h ?'), default=False, blank=True)
    only_season = models.BooleanField(_('ouvert selement dans les saisons ?'), default=False, blank=True)
    # Target
    for_schools_use = models.BooleanField(_('pour utilisation scolaire ?'), default=False, blank=True)
    for_clubs_use = models.BooleanField(_('pour utilisation des clubs ?'), default=False, blank=True)
    for_others_use = models.BooleanField(_('pour utilisation autre ?'), default=False, blank=True)
    for_individual_use = models.BooleanField(_('pour utilisation individuelle ?'), default=False, blank=True)
    # Disabled person accessibility information
    accessible_handicapped_m = models.BooleanField(_('accéssible aux handicapés à mobilité réduite ?'),
                                                   default=False, blank=True)
    accessible_handicapped_s = models.BooleanField(_('accéssible aux handicapés sensoriaux ?'),
                                                   default=False, blank=True)
    evolution_area_access_hm = models.BooleanField(
        _('Zone d\'évolution accéssible aux handicapés à mobilité réduite ?'),
        default=False, blank=True)
    evolution_area_access_hs = models.BooleanField(
        _('Zone d\'évolution accéssible aux handicapés sensoriaux ?'),
        default=False, blank=True)
    # Additional information
    is_public = models.BooleanField(_('est publique ?'), default=False, blank=True)
    work_timetable = models.ManyToManyField(TimeInterval, blank=True, related_name='equipments')
    price = models.TextField(_('liste des prix'), blank=True, null=True)
    overview = models.TextField(_('vue d\'ensemble'), blank=True, null=True)
    phone_number = models.CharField(_('numéro de téléphone'), max_length=20, blank=True, null=True)
    mail = models.EmailField(_('adresse e-mail'), max_length=50, blank=True, null=True)
    website_url = models.URLField(_('site web'), max_length=80, blank=True, null=True)
    facebook_url = models.URLField(_('facebook'), max_length=80, blank=True, null=True)
    twitter_url = models.URLField(_('twitter'), max_length=80, blank=True, null=True)
    google_plus_url = models.URLField(_('google plus'), max_length=80, blank=True, null=True)
    # activities
    disciplines = models.ManyToManyField(SportDiscipline, blank=True, related_name='equipments')
    # Promotions & events
    promo_event = models.TextField(_('promos & évênements'), blank=True, null=True)
    # Administration
    is_active = models.BooleanField(_('est actif ?'), default=False)
    # Important dates
    created = models.DateTimeField(_('date de création'), auto_now_add=True)
    modified = models.DateTimeField(_('date de modification'), auto_now=True)

    class Meta:
        verbose_name = _('site sportif')
        verbose_name_plural = _('sites sportifs')

    def __str__(self):
        return self.name


class EquipmentImage(models.Model):
    equipment = models.ForeignKey(Equipment, related_name='equipments')
    image = models.ImageField(_('image'), 'default-equipment.png',
                              upload_to='equipments/images')


class InstitutionImage(models.Model):
    institution = models.ForeignKey(Institution, related_name='institutions')
    image = models.ImageField(_('image'), 'default-institution.png',
                              upload_to='institutions/images')
