"""kirja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

sub_patterns = [
    # Djangon ylläpitosivusto
    path('yllapito/', admin.site.urls),
    # django-wikin tarvitsemat polut
    path('notifications/', include('django_nyt.urls')),
    path('', include('wiki.urls')),
]

urlpatterns = [
    # Yksinkertaistetaan konfiguraatiota pistämällä kaikki sovelluksen polut URL_PREFIX alle
    # include-funktion avulla.
    path(r'' + settings.URL_PREFIX, include(sub_patterns)),
]
