from django.shortcuts import render
from django.views.generic import CreateView
from service_member.forms import SignUpInstituteForm, SignUpBenefactorForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from service_member.models import Benefactor, Institute, Member


# Create your views here.


class SignUpInstituteView(CreateView):
    form_class = SignUpInstituteForm
    success_url = '/signup/benefactor/'
    template_name = 'SignUp.html'


class SignUpBenefactorView(CreateView):
    form_class = SignUpBenefactorForm
    success_url = '/signup/benefactor/'
    template_name = 'SignUp.html'


def home_view(request):
    if request.user.is_benefactor:
        raise Http404
    return render(request, 'home.html')
