"""
URL configuration for slide_away project.

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
from django.urls import path
from market import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ver_inicio),#(Agregar la pagina principal de la tienda, que es la pagina de inicio del sitio web, donde se muestran los productos disponibles y se pueden realizar compras. Esto se puede hacer utilizando la vista principal de la tienda, que se puede definir en el archivo views.py de la aplicación de la tienda. También se pueden agregar otras vistas para mostrar detalles de productos individuales, categorías de productos, etc.)
    path('inicio/', views.ver_inicio),  # Página de inicio de la tienda
    path('uf/', views.leer_uf_actual),  # Página para ver productos
    path('empleados/', views.ver_empleados),
]
