from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^submit/kharj/$',views.sabte_kharj, name= 'sabte_kharj'),
url(r'^submit/daramad/$',views.sabte_daramad, name= 'sabte_daramad'),
]
