"""
URL configuration for amaliyotdocx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home_redirect

urlpatterns = [
    path('', home_redirect),
    path('admin/', admin.site.urls),
    path('excel/', include('app_excel.urls')),
    path('shartnoma/', include('app_shartnoma.urls')),
]


handler401 = 'app_excel.views.handler401'
handler403 = 'app_excel.views.handler403'
handler404 = 'app_excel.views.handler404'
handler500 = 'app_excel.views.handler500'
