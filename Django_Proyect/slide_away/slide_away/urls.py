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
    path('catalogo/', views.ver_catalogo, name='catalogo'),
    path('carrito/', views.ver_carrito, name='carrito'),
    
    # URLs para carrito
    path('api/carrito/productos/', views.obtener_productos_carrito, name='api_carrito_productos'),
    path('api/producto/<int:producto_id>/', views.obtener_producto_por_id, name='api_producto_id'),
    
    # URLs para pagos con Transbank - VERSIÓN FUNCIONAL
    path('pago/', views.ver_pago, name='pago'),
    path('api/pago/iniciar/', views.iniciar_pago, name='iniciar_pago'),
    path('retorno/', views.retorno_pago, name='retorno_pago'),  # Esta es la URL que faltaba
    path('pago/confirmar/', views.confirmar_pago, name='confirmar_pago'),
    path('pago/anulado/', views.pago_anulado, name='pago_anulado'),
    
    # URLs para panel de administración
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    # APIs para panel de administración
    path('api/productos/', views.listar_productos_api, name='api_productos_list'),
    path('api/productos/crear/', views.crear_producto_api, name='api_productos_create'),
    path('api/productos/<int:pk>/', views.obtener_producto_api, name='api_productos_detail'),
    path('api/productos/<int:pk>/actualizar/', views.actualizar_producto_api, name='api_productos_update'),
    path('api/productos/<int:pk>/eliminar/', views.eliminar_producto_api, name='api_productos_delete'),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)