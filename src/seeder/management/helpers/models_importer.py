# -*- coding: utf-8 -*-
import os
import logging
from slugify import slugify

from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

from .core import ABSCoreCommandImporter
from equipments.models import ManagerCategory, Department, Commune, Institution, SpecialInstitution

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ManagerImporter(ABSCoreCommandImporter):

    def __init__(self, filename=None, model=None):
        """
        Class constructor.
        :param filename: str
        :param model: models.Model
        """
        if filename is None:
            filename = os.path.join(settings.BASE_DIR, '..', 'data', '10.managers_categories.csv')
        if model is None:
            model = ManagerCategory
        super(ManagerImporter, self).__init__(filename, model)

    def serialize(self, row):
        """
        Serialize row to model
        :param row:
        :return: models.Model
        """
        label = row['label'].encode('utf-8')
        slug = slugify(row['label'])
        is_public = 'NOT_DEFINED'

        if int(row['is_public'].encode('utf-8')) == 1:
            is_public = 'IS_PUBLIC'
        elif int(row['is_public'].encode('utf-8')) == 0:
            is_public = 'NOT_PUBLIC'

        logger.info('[SUCCESS][SERIALIZE] {} - {}'.format(label, is_public))
        return self.model(label=label, slug=slug, is_public=is_public)


class DepartmentImporter(ABSCoreCommandImporter):

    def __init__(self, filename=None, model=None):
        """
        Class constructor.
        :param filename: str
        :param model: models.Model
        """
        if filename is None:
            filename = os.path.join(settings.BASE_DIR, '..', 'data', '12.departments.csv')
        if model is None:
            model = Department
        super(DepartmentImporter, self).__init__(filename, model)

    def serialize(self, row):
        """
        Serialize row to model
        :param row:
        :return: models.Model
        """
        if row['code'].isdecimal():
            if int(row['code'].encode('utf-8')) > 95:
                return None
        code = row['code'].encode('utf-8')
        label = row['label'].encode('utf-8')
        slug = slugify(row['label'])

        logger.info('[SUCCESS][SERIALIZE] {} - {}'.format(code, label))
        return self.model(code=code, label=label, slug=slug)


class CommuneImporter(ABSCoreCommandImporter):

    def __init__(self, filename=None, model=None):
        """
        Class constructor.
        :param filename: str
        :param model: models.Model
        """
        if filename is None:
            filename = os.path.join(settings.BASE_DIR, '..', 'data', '13.communes.csv')
        if model is None:
            model = Commune
        super(CommuneImporter, self).__init__(filename, model)

    def serialize(self, row):
        """
        Serialize row to model
        :param row:
        :return: models.Model
        """
        if row['department'].isdecimal():
            if int(row['department'].encode('utf-8')) > 95:
                return None
        code_insee = row['code_insee'].encode('utf-8')
        label = row['label'].encode('utf-8')
        slug = slugify(row['label'])
        department_id = row['department'].encode('utf-8')
        logger.info('[SUCCESS][SERIALIZE] {} - {}'.format(code_insee, label))
        return self.model(code_insee=code_insee, label=label, slug=slug, department_id=department_id)


class InstitutionImporter(ABSCoreCommandImporter):

    def __init__(self, filename=None, model=None):
        """
        Class constructor.
        :param filename: str
        :param model: models.Model
        """
        if filename is None:
            filename = os.path.join(settings.BASE_DIR, '..', 'data', '14.institutions.csv')
        if model is None:
            model = Institution
        super(InstitutionImporter, self).__init__(filename, model)

    def serialize(self, row):
        """
        Serialize row to model
        :param row:
        :return: models.Model
        """
        if row['DepCode'].isdecimal():
            if int(row['DepCode']) > 95:
                return None

        code = row['InsNumeroInstall']
        if code.isdecimal():
            if int(code) == 110050002 \
                    or int(code) == 130010002\
                    or int(code) == 130550026\
                    or int(code) == 191230007\
                    or int(code) == 341870016\
                    or int(code) == 591830020:
                return None

        name = row['InsNom'].encode('utf-8')
        slug = slugify(row['InsNom'])

        try:
            slug_special_institution = 'non' \
                if (slugify(row['InsPartLibelle']) == 'null') or \
                   (slugify(row['InsPartLibelle']).isdecimal()) or \
                   (slugify(row['InsPartLibelle']) == '') else slugify(row['InsPartLibelle'])
            special_institution = SpecialInstitution.objects.get(slug=slug_special_institution)
        except ValueError as error:
            # logger.debug(error)
            # label_special_institution = row['InsPartLibelle'].encode('utf-8')
            # special_institution = SpecialInstitution(
            #     label=label_special_institution,
            #     slug=slugify(row['InsPartLibelle']))
            # special_institution.save()
            logger.error(
                '[ValueError] {} : special institution does not exist'.format(slugify(row['InsPartLibelle'])))
            return None
        except ObjectDoesNotExist as error:
            logger.error(
                '[ObjectDoesNotExist] {} : special institution does not exist'.format(slugify(row['InsPartLibelle'])))
            # logger.debug(error)
            # label_special_institution = row['InsPartLibelle'].encode('utf-8')
            # special_institution = SpecialInstitution(
            #     label=label_special_institution,
            #     slug=slugify(row['InsPartLibelle']))
            # special_institution.save()
            # logger.warning(
            #     '[ObjectDoesNotExist] {} : special institution created'.format(slugify(row['InsPartLibelle'])))
            return None

        street_number = row['InsNoVoie'].encode('utf-8')
        street_name = row['InsLibelleVoie'].encode('utf-8')
        common_name = row['InsLieuDit'].encode('utf-8')
        postal_code = row['InsCodePostal'].encode('utf-8')

        try:
            commune = Commune.objects.get(code_insee=row['ComInsee'])
        except ValueError as error:
            logger.error(
                '[ValueError] {} {} : Commune does not exist'.format(row['ComInsee'], row['ComLib'].encode('utf-8')))
            # logger.debug(error)
            # code_commune = row['ComInsee'].encode('utf-8')
            # label_commune = row['ComLib'].encode('utf-8')
            # commune = Commune(code_insee=code_commune, label=label_commune, slug=slugify(row['ComLib']))
            # commune.save()
            # logger.warning(
            #     '[ValueError] {} {} : Commune created'.format(row['ComInsee'], row['ComLib'].encode('utf-8')))
            return None
        except ObjectDoesNotExist as error:
            logger.error(
                '[ObjectDoesNotExist] {} {} : Commune does not exist'.format(
                    row['ComInsee'], row['ComLib'].encode('utf-8')))
            # logger.debug(error)
            # code_commune = row['ComInsee'].encode('utf-8')
            # label_commune = row['ComLib'].encode('utf-8')
            # dep_code = row['DepCode']
            # dep_label = row['DepLib'].encode('utf-8')
            # dep_slug = slugify(row['DepLib'])
            # department, dep_created = Department.objects.get_or_create(code=dep_code, label=dep_label, slug=dep_slug)
            # commune = Commune(code_insee=code_commune, label=label_commune,
            #                   slug=slugify(row['ComLib']), department=department)
            # commune.save()
            # logger.warning(
            #     '[ObjectDoesNotExist] {} {} : Commune created'.format(row['ComInsee'], row['ComLib'].encode('utf-8')))
            return None

        if (not row['InsInternat'].encode('utf-8').isdigit()) \
                or (int(row['InsInternat'].encode('utf-8')) > 1):
            have_internet = False
        else:
            have_internet = row['InsInternat'].encode('utf-8')

        if not row['InsNbCouvert'].encode('utf-8').isdigit():
            number_covers = 0
        else:
            number_covers = row['InsNbCouvert'].encode('utf-8')

        if not row['InsNbLit'].encode('utf-8').isdigit():
            number_beds = 0
        else:
            number_beds = row['InsNbLit'].encode('utf-8')

        if not row['InsNbPlaceParking'].encode('utf-8').isdigit():
            number_parking_spaces = 0
        else:
            number_parking_spaces = row['InsNbPlaceParking'].encode('utf-8')

        if (not row['InsAccessibiliteHandiMoteur'].encode('utf-8').isdigit()) \
                or (int(row['InsAccessibiliteHandiMoteur'].encode('utf-8')) > 1):
            is_accessible_for_hand_m = False
        else:
            is_accessible_for_hand_m = row['InsAccessibiliteHandiMoteur'].encode('utf-8')

        if (not row['InsAccessibiliteHandiSens'].encode('utf-8').isdigit()) \
                or (int(row['InsAccessibiliteHandiSens'].encode('utf-8')) > 1):
            is_accessible_for_hand_s = False
        else:
            is_accessible_for_hand_s = row['InsAccessibiliteHandiSens'].encode('utf-8')

        if not row['InsNbPlaceParkingHandi'].encode('utf-8').isdigit():
            number_parking_hn_spaces = 0
        else:
            number_parking_hn_spaces = row['InsNbPlaceParkingHandi'].encode('utf-8')

        if (not row['InsTransportMetro'].encode('utf-8').isdigit()) \
                or (int(row['InsTransportMetro'].encode('utf-8')) > 1):
            have_metro = False
        else:
            have_metro = row['InsTransportMetro'].encode('utf-8')

        if (not row['InsTransportBus'].encode('utf-8').isdigit()) \
                or (int(row['InsTransportBus'].encode('utf-8')) > 1):
            have_bus = False
        else:
            have_bus = row['InsTransportBus'].encode('utf-8')

        if (not row['InsTransportTram'].encode('utf-8').isdigit()) \
                or (int(row['InsTransportTram'].encode('utf-8')) > 1):
            have_tramway = False
        else:
            have_tramway = row['InsTransportTram'].encode('utf-8')

        if (not row['InsTransportTrain'].encode('utf-8').isdigit()) \
                or (int(row['InsTransportTrain'].encode('utf-8')) > 1):
            have_train = False
        else:
            have_train = row['InsTransportTrain'].encode('utf-8')

        if (not row['InsTransportBateau'].encode('utf-8').isdigit()) \
                or (int(row['InsTransportBateau'].encode('utf-8')) > 1):
            have_boat = False
        else:
            have_boat = row['InsTransportBateau'].encode('utf-8')

        if (not row['InsTransportAutre'].encode('utf-8').isdigit()) \
                or (int(row['InsTransportAutre'].encode('utf-8')) > 1):
            have_other_transport = False
        else:
            have_other_transport = row['InsTransportAutre'].encode('utf-8')

        logger.info('[SUCCESS][SERIALIZE] {} - {}'.format(code, name))
        # return None
        return self.model(
            code=code,
            name=name,
            slug=slug,
            special_institution=special_institution,
            street_number=street_number,
            street_name=street_name,
            common_name=common_name,
            postal_code=postal_code,
            commune=commune,
            have_internet=have_internet,
            number_covers=number_covers,
            number_beds=number_beds,
            number_parking_spaces=number_parking_spaces,
            is_accessible_for_hand_m=is_accessible_for_hand_m,
            is_accessible_for_hand_s=is_accessible_for_hand_s,
            number_parking_hn_spaces=number_parking_hn_spaces,
            have_metro=have_metro,
            have_bus=have_bus,
            have_tramway=have_tramway,
            have_train=have_train,
            have_boat=have_boat,
            have_other_transport=have_other_transport
        )
