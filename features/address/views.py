# views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from features.address.models import Province, Municipality, Barangay


def get_provinces(request):
    provinces = Province.objects.all().order_by('name')
    return JsonResponse(list(provinces.values('id', 'name')), safe=False)


def get_province_municipalities(request, province_id):
    municipalities = Municipality.objects.filter(province_id=province_id).order_by('name')
    return JsonResponse(list(municipalities.values('id', 'name')), safe=False)


def get_municipality_barangays(request, municipality_id):
    barangays = Barangay.objects.filter(municipality_id=municipality_id).order_by('name')
    return JsonResponse(list(barangays.values('id', 'name')), safe=False)
