from features.address.models import Province, Municipality, Barangay
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm
from features.address.philippine_address_data import PhilippineAddressDataProcessor


class Command(BaseCommand):
    help = 'Populate the address models with data from the JSON file'

    def handle(self, *args, **kwargs):
        ph_address_data = PhilippineAddressDataProcessor()

        provinces = []
        municipalities = []
        barangays = []

        province_cache = {}
        municipality_cache = {}

        with transaction.atomic():
            regions = ph_address_data.get_data().items()
            for region_code, region_data in tqdm(regions, desc="Regions"):
                for province_name in tqdm(region_data['province_list'], desc="Provinces", leave=False):
                    if province_name not in province_cache:
                        province = Province(name=province_name)
                        provinces.append(province)
                        province_cache[province_name] = province
                    else:
                        province = province_cache[province_name]

                    for municipality_name in tqdm(region_data['province_list'][province_name]['municipality_list'],
                                                  desc="Municipalities", leave=False):
                        if municipality_name not in municipality_cache:
                            municipality = Municipality(name=municipality_name, province=province)
                            municipalities.append(municipality)
                            municipality_cache[municipality_name] = municipality
                        else:
                            municipality = municipality_cache[municipality_name]

                        barangay_list = ph_address_data.get_barangays_by_municipality(region_code, province_name,
                                                                                      municipality_name)
                        for barangay_name in tqdm(barangay_list, desc="Barangays", leave=False):
                            barangay = Barangay(name=barangay_name, municipality=municipality)
                            barangays.append(barangay)

            # Bulk create all objects
            Province.objects.bulk_create(provinces)
            Municipality.objects.bulk_create(municipalities)
            Barangay.objects.bulk_create(barangays)

        self.stdout.write(self.style.SUCCESS('Successfully populated address models'))
