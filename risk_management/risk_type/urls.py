from django.conf.urls import url
from risk_type import views

urlpatterns = [
    url(r'^get/risk/(?P<risk_id>[0-9]+)/$', views.get_risk, name="GetRisk"),
    url(r'^get/risks/$', views.get_all_risk, name="GetAllRisk"),
]
