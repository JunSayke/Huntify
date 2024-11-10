import json
import os


class PhilippineAddressDataProcessor:
    def __init__(self):
        file_path = os.path.join(os.path.dirname(__file__),
                                 './static/address_data'
                                 '/philippine_provinces_cities_municipalities_and_barangays_2019v2.json')
        with open(file_path, 'r') as file:
            self._data = json.load(file)

    def get_data(self):
        return self._data

    def get_all_regions(self):
        return [region['region_name'] for region in self._data.values()]

    def get_provinces_by_region(self, region_code):
        if region_code in self._data:
            return list(self._data[region_code]['province_list'].keys())
        return []

    def get_municipalities_by_province(self, region_code, province_name):
        if region_code in self._data and province_name in self._data[region_code]['province_list']:
            return list(self._data[region_code]['province_list'][province_name]['municipality_list'].keys())
        return []

    def get_barangays_by_municipality(self, region_code, province_name, municipality_name):
        if (region_code in self._data and
                province_name in self._data[region_code]['province_list'] and
                municipality_name in self._data[region_code]['province_list'][province_name]['municipality_list']):
            return self._data[region_code]['province_list'][province_name]['municipality_list'][municipality_name].get(
                'barangay_list', [])
        return []

    def get_all_barangays(self):
        barangays = []
        for region_code, region_data in self._data.items():
            for province_name, province_data in region_data['province_list'].items():
                for municipality_name, municipality_data in province_data['municipality_list'].items():
                    barangays.extend(municipality_data.get('barangay_list', []))
        return barangays
