from django.urls import path
from .views import generate_contracts_download

urlpatterns = [
    path('generate/', generate_contracts_download, name='generate_contracts'),
]
