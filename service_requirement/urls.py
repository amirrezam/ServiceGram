from service_requirement.views import CreateCashRequirementView, CreateNonCashRequirementView, \
    CashRequirementProfileView, NonCashRequirementProfileView, RequestHelpBenefactorView, ShowRequestsRequirementView, \
    AcceptRequestFromBenefactorView, ShowNonCashRequirementsView
from django.contrib.auth import views as auth_views
from django.urls import re_path

urlpatterns = [
    re_path(r'info/cash/(?P<pk>[a-zA-Z0-9]+)$', CashRequirementProfileView.as_view(), name='cash_requirement_profile'),
    re_path(r'info/non_cash/(?P<pk>[a-zA-Z0-9]+)$', NonCashRequirementProfileView.as_view(), name='non_cash_requirement_profile'),
    re_path(r'request/(?P<pk>[a-zA-Z0-9]+)/$', RequestHelpBenefactorView.as_view(), name='request_help_benefactor'),
    re_path(r'requests/accept/(?P<pk>[a-zA-Z0-9]+)$', AcceptRequestFromBenefactorView.as_view(), name='accept_request_help_benefactor'),
    re_path(r'requests/(?P<pk>[a-zA-Z0-9]+)$', ShowRequestsRequirementView.as_view(), name='show_request_help_benefactor'),
    re_path(r'new/cash/$', CreateCashRequirementView.as_view(), name='create_cash_requirement'),
    re_path(r'new/non_cash/$', CreateNonCashRequirementView.as_view(), name='create_non_cash_requirement'),
    re_path(r'search/non_cash/$', ShowNonCashRequirementsView.as_view(), name='show_non_cash_requirements')
]
