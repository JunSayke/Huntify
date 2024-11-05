from django.shortcuts import render

from features.authentication.forms import UserTypeForm


# Create your views here.
def test(request):
    form = UserTypeForm()
    return render(request, "html/form_tester.html", {'form': form})
