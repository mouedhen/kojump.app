# -*- coding: utf-8 -*-
import os
import logging
from slugify import slugify

from django.conf import settings
from django.contrib.gis.geos import Point

from .core import ABSCoreCommandImporter
from equipments.models import Equipment, Institution, EquipmentCategory, ManagerCategory

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class EquipmentImporter(ABSCoreCommandImporter):

    def __init__(self, filename=None, model=None):
        """
        Class constructor.
        :param filename: str
        :param model: models.Model
        """
        if filename is None:
            filename = os.path.join(settings.BASE_DIR, '..', 'data', '15.equipments.csv')
        if model is None:
            model = Equipment
        super(EquipmentImporter, self).__init__(filename, model)

    # def prepare(self, reader):
    #     from multiprocessing import Process, Manager
    #     """
    #     Prepare a list of records.
    #     :param reader:
    #     :return: list
    #     """
    #     with Manager() as manager:
    #         L = manager.list()
    #         processes = []
    #         for row in reader:
    #             p = Process(target=self.append_records, args=(L, row))  # Passing the list
    #             p.start()
    #             processes.append(p)
    #         for p in processes:
    #             p.join()
    #         return L

    @staticmethod
    def fill_boolean(column):
        if column.isdigit():
            if int(column) >= 0:
                return True
        return False

    @staticmethod
    def get_institute(code):
        try:
            return Institution.objects.get(code=code)
        except Institution.DoesNotExist:
            return None

    @staticmethod
    def get_category(label):
        try:
            if label.encode('utf-8').isdigit():
                equipment = EquipmentCategory.objects.get(reference=label.encode('utf-8'))
            else:
                equipment = EquipmentCategory.objects.get(slug=slugify(label))
            return equipment
        except EquipmentCategory.DoesNotExist:
            return None

    @staticmethod
    def get_manager_category(label):
        if label == '':
            return None
        slug = slugify(label)
        try:
            manager_cat = ManagerCategory.objects.get(slug=slug)
            return manager_cat
        except ManagerCategory.DoesNotExist:
            return None

    def serialize(self, row):
        """
        Serialize row to model
        :param row:
        :return: models.Model
        """
        if row['DepCode'].isdecimal():
            if int(row['DepCode']) > 95:
                return None

        code = row['EquipementId'].encode('utf-8')

        if not row['EquipementId'].isdecimal():
            return None

        name = row['EquNom'].encode('utf-8')
        slug = slugify(row['EquNom'])
        institution = self.get_institute(row['InsNumeroInstall'].encode('utf-8'))
        if institution is None:
            return None
        # owner_category = self.get_manager_category(row['GestionTypeProprietairePrincLib'])
        # manager_category = self.get_manager_category(row['GestionTypeGestionnairePrincLib'])
        # category = self.get_category(row['EquipementTypeLib'])
        is_erp_cts = self.fill_boolean(row['EquErpCTS'].encode('utf-8'))
        is_erp_ref = self.fill_boolean(row['EquErpREF'].encode('utf-8'))
        is_erp_l = self.fill_boolean(row['EquErpL'].encode('utf-8'))
        is_erp_n = self.fill_boolean(row['EquErpN'].encode('utf-8'))
        is_erp_o = self.fill_boolean(row['EquErpO'].encode('utf-8'))
        is_erp_oa = self.fill_boolean(row['EquErpOA'].encode('utf-8'))
        is_erp_p = self.fill_boolean(row['EquErpP'].encode('utf-8'))
        is_erp_pa = self.fill_boolean(row['EquErpPA'].encode('utf-8'))
        is_erp_r = self.fill_boolean(row['EquErpR'].encode('utf-8'))
        is_erp_rpe = self.fill_boolean(row['EquErpRPE'].encode('utf-8'))
        is_erp_sg = self.fill_boolean(row['EquErpSG'].encode('utf-8'))
        is_erp_x = self.fill_boolean(row['EquErpX'].encode('utf-8'))
        have_showers = self.fill_boolean(row['EquDouche'].encode('utf-8'))
        have_lights = self.fill_boolean(row['EquEclairage'].encode('utf-8'))
        # tribune_places = row[''].encode('utf-8')
        # ground = row[''].encode('utf-8')
        # environment = row[''].encode('utf-8')
        # have_heated_cloakroom = row[''].encode('utf-8')
        # corridors_number = row[''].encode('utf-8')
        # is_always_open = row[''].encode('utf-8')
        # only_season = row[''].encode('utf-8')
        # for_schools_use = row[''].encode('utf-8')
        # for_clubs_use = row[''].encode('utf-8')
        # for_others_use = row[''].encode('utf-8')
        # for_individual_use = row[''].encode('utf-8')
        # accessible_handicapped_m = row[''].encode('utf-8')
        # accessible_handicapped_s = row[''].encode('utf-8')
        # evolution_area_access_hm = row[''].encode('utf-8')
        # evolution_area_access_hs = row[''].encode('utf-8')
        # is_active = row[''].encode('utf-8')

        logger.info('[SUCCESS][SERIALIZE] Institution {} : {} - {} ({} ; {})'.format(
            row['InsNumeroInstall'].encode('utf-8'),
            code,
            name,
            row['EquGpsX'].encode('utf-8').replace(',', '.'),
            row['EquGpsY'].encode('utf-8').replace(',', '.'),
        ))
        try:
            latitude = float(row['EquGpsX'].encode('utf-8').replace(',', '.'))
            longitude = float(row['EquGpsY'].encode('utf-8').replace(',', '.'))
        except ValueError:
            return None

        gps_coordinates = Point(latitude, longitude, srid=4326)
        # logger.info('[SUCCESS][SERIALIZE] Institution {} : {} - {}'.format(row['InsNumeroInstall'].encode('utf-8'),
        #                                                                    code, name))
        return self.model(code=code, name=name, slug=slug, is_erp_cts=is_erp_cts, is_erp_ref=is_erp_ref,
                          institution=institution,
                          is_erp_l=is_erp_l, is_erp_n=is_erp_n, is_erp_o=is_erp_o,
                          is_erp_oa=is_erp_oa, is_erp_p=is_erp_p, is_erp_pa=is_erp_pa,
                          is_erp_r=is_erp_r, is_erp_rpe=is_erp_rpe, is_erp_sg=is_erp_sg,
                          is_erp_x=is_erp_x, have_showers=have_showers, have_lights=have_lights,
                          gps_coordinates=gps_coordinates)
