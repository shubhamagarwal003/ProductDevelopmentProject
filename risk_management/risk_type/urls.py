from django.conf.urls import url
from risk_type import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^get/risk/(?P<risk_id>[0-9]+)/$', views.get_risk, name="GetRisk"),
    url(r'^get/risks/$', views.get_all_risk, name="GetAllRisk"),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="GetPage"),
]
