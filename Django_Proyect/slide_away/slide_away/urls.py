from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from market import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.ver_login, name='login'),
    path('uf/', views.leer_uf_actual, name='uf'),
    path('empleados/', views.ver_empleados, name='empleados'),
    path('', views.ver_menu_principal, name='menu_principal'),
    path('menu/', views.ver_menu_principal, name='menu_principal'),
    path('catalogo/', views.ver_catalogo, name='catalogo'),  # Nueva URL
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)