from service_requirement.views import CreateCashRequirementView, CreateNonCashRequirementView
from django.contrib.auth import views as auth_views
from django.urls import re_path

urlpatterns = [
    re_path(r'new/cash/$', CreateCashRequirementView.as_view(), name='create_cash_requirement'),
    re_path(r'new/non_cash/$', CreateNonCashRequirementView.as_view(), name='create_non_cash_requirement')
]
