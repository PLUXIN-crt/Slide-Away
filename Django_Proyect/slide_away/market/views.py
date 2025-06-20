from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import json
import uuid
from datetime import datetime

# Configuración de Transbank FUNCIONAL
try:
    from transbank.webpay.webpay_plus.transaction import Transaction
    from transbank.common.options import WebpayOptions
    
    # Configuración de integración (solo para pruebas)
    commerce_code = '597055555532'
    api_key = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
    options = WebpayOptions(commerce_code, api_key, integration_type='TEST')
    transaction = Transaction(options)
    
    TRANSBANK_AVAILABLE = True
    print("Transbank SDK configurado exitosamente para pruebas con WebpayOptions")
except ImportError as e:
    print(f"Transbank SDK no está disponible: {e}")
    TRANSBANK_AVAILABLE = False
    transaction = None
except Exception as e:
    print(f"Error al configurar Transbank: {e}")
    TRANSBANK_AVAILABLE = False
    transaction = None

def ver_login(request):
    return render(request, "login.html")

def obtener_uf_actual():
    url="https://www.mindicador.cl/api/uf/15-05-2025"
    try:
        response = requests.get(url)
        data = response.json()
        uf = data['serie'][0]['valor']
        fecha = data['serie'][0]['fecha']
        return uf, fecha
    except Exception as e:
        return None, str(e)

def leer_uf_actual(request):
    uf, fecha = obtener_uf_actual()
    contexto = {
            'uf':uf,
            'fecha':fecha
        }
    return render(request,"api_uf.html", contexto)

def obtener_empleados():
    url="http://127.0.0.1:8089/api/empleados/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Empleados obtenidos: {len(data)}")
            return data
        else:
            print(f"Error en empleados: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al obtener empleados: {e}")
        return []

def obtener_productos():
    url="http://127.0.0.1:8089/api/productos/dto"  # Usar el nuevo endpoint DTO
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Productos obtenidos: {len(data)}")
            # Los datos ahora incluyen nombreCategoria, nombreMarca, nombreProveedor
            return data
        else:
            print(f"Error en productos: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []
def obtener_categorias():
    url="http://127.0.0.1:8089/api/categorias"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Categorías obtenidas: {len(data)}")
            return data
        else:
            print(f"Error en categorías: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al obtener categorías: {e}")
        return []

def obtener_marcas():
    url="http://127.0.0.1:8089/api/marcas"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Marcas obtenidas: {len(data)}")
            return data
        else:
            print(f"Error en marcas: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al obtener marcas: {e}")
        return []

def ver_empleados(request):
    empleados = obtener_empleados()
    contexto = { "datos":empleados}
    return render (request, "ver_empleados.html", contexto)

def ver_menu_principal(request):
    productos = obtener_productos()
    categorias = obtener_categorias()
    marcas = obtener_marcas()
    
    # Limitar a 6 productos para la página principal
    productos_destacados = productos[:6] if productos else []
    
    print(f"DEBUG - Productos destacados: {len(productos_destacados)}")
    print(f"DEBUG - Categorías: {len(categorias)}")
    print(f"DEBUG - Marcas: {len(marcas)}")
    
    contexto = {
        'productos': productos_destacados,
        'categorias': categorias,
        'marcas': marcas
    }
    return render(request, "menu_principal.html", contexto)

def ver_catalogo(request):
    productos = obtener_productos()
    categorias = obtener_categorias()
    marcas = obtener_marcas()
    
    contexto = {
        'productos': productos,
        'categorias': categorias,
        'marcas': marcas
    }
    return render(request, "catalogo.html", contexto)

def ver_carrito(request):
    return render(request, "carrito.html")

# Nuevas APIs para el carrito
@csrf_exempt
@require_http_methods(["POST"])
def obtener_productos_carrito(request):
    """Endpoint para obtener productos del carrito desde Spring Boot"""
    try:
        data = json.loads(request.body)
        ids_productos = data.get('ids', [])
        
        if not ids_productos:
            return JsonResponse({'error': 'No se proporcionaron IDs de productos'}, status=400)
        
        # Obtener productos individualmente desde Spring Boot
        productos = []
        for producto_id in ids_productos:
            url = f"http://127.0.0.1:8089/api/productos/{producto_id}/dto"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    producto = response.json()
                    productos.append(producto)
                else:
                    print(f"Error al obtener producto {producto_id}: {response.status_code}")
            except Exception as e:
                print(f"Error al obtener producto {producto_id}: {e}")
        
        return JsonResponse({'productos': productos})
            
    except Exception as e:
        print(f"Error al obtener productos del carrito: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def obtener_producto_por_id(request, producto_id):
    """Endpoint para obtener un producto específico por ID"""
    try:
        url = f"http://127.0.0.1:8089/api/productos/{producto_id}/dto"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            producto = response.json()
            return JsonResponse(producto)
        else:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
            
    except Exception as e:
        print(f"Error al obtener producto {producto_id}: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def ver_pago(request):
    """Vista para mostrar el formulario de pago"""
    return render(request, "pago.html")



@csrf_exempt
def iniciar_pago(request):
    """Iniciar el proceso de pago con Transbank - Versión Funcional"""
    if not TRANSBANK_AVAILABLE or transaction is None:
        return JsonResponse({'error': 'Transbank SDK no está configurado'}, status=500)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Obtener datos del carrito
            carrito_items = data.get('carrito', [])
            total = float(data.get('total', 0))
            datos_cliente = data.get('cliente', {})
            
            if not carrito_items or total <= 0:
                return JsonResponse({'error': 'Carrito vacío o total inválido'}, status=400)
            
            # Generar un ID único para la orden
            buy_order = f"orden_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"
            session_id = f"session_{uuid.uuid4().hex[:8]}"
            amount = int(total)  # Transbank requiere monto como entero
            
            # URL de retorno después del pago
            return_url = request.build_absolute_uri(reverse('retorno_pago'))
            
            print(f"Iniciando pago - Orden: {buy_order}, Total: {amount}, Return URL: {return_url}")
            
            # Guardar datos de la orden en sesión ANTES de crear la transacción
            request.session['orden_datos'] = {
                'buy_order': buy_order,
                'session_id': session_id,
                'carrito': carrito_items,
                'total': total,
                'cliente': datos_cliente
            }
            
            # Crear transacción con Transbank usando tu método funcional
            response = transaction.create(buy_order, session_id, amount, return_url)
            
            print(f"Transacción creada exitosamente - Token: {response['token']}")
            
            # Actualizar sesión con el token
            request.session['orden_datos']['token'] = response['token']
            
            return JsonResponse({
                'success': True,
                'token': response['token'],
                'url': response['url']
            })
            
        except Exception as e:
            print(f"Error al iniciar pago: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def retorno_pago(request):
    """Vista que recibe el retorno después del pago - Versión Funcional"""
    if not TRANSBANK_AVAILABLE or transaction is None:
        return render(request, 'pago_error.html', {
            'error': 'Transbank SDK no está configurado'
        })
    
    token = request.GET.get('token_ws') or request.POST.get('token_ws')
    
    if not token:
        return render(request, 'pago_error.html', {
            'error': 'Token de pago no encontrado'
        })
    
    try:
        # Confirmar transacción con Transbank usando tu método funcional
        result = transaction.commit(token)
        
        print(f"Respuesta de confirmación: {result}")
        
        # Obtener datos de la orden desde la sesión
        orden_datos = request.session.get('orden_datos', {})
        
        # Verificar que la respuesta sea exitosa
        if result.get('status') == 'AUTHORIZED':  # Transacción autorizada
            # Pago exitoso
            contexto = {
                'success': True,
                'orden': result.get('buy_order'),
                'total': result.get('amount'),
                'carrito': orden_datos.get('carrito', []),
                'cliente': orden_datos.get('cliente', {}),
                'transaccion': {
                    'authorization_code': result.get('authorization_code'),
                    'transaction_date': result.get('transaction_date'),
                    'card_number': result.get('card_detail', {}).get('card_number', 'N/A') if result.get('card_detail') else 'N/A',
                    'amount': result.get('amount'),
                    'status': result.get('status')
                }
            }
            
            # Limpiar sesión
            if 'orden_datos' in request.session:
                del request.session['orden_datos']
            
            return render(request, 'pago_resultado.html', contexto)
        else:
            # Pago rechazado o fallido
            return render(request, 'pago_error.html', {
                'error': f'Pago no autorizado. Estado: {result.get("status", "UNKNOWN")}'
            })
            
    except Exception as e:
        print(f"Error al confirmar pago: {e}")
        return render(request, 'pago_error.html', {
            'error': f'Error al procesar el pago: {str(e)}'
        })

def pago_anulado(request):
    """Vista cuando el usuario cancela el pago"""
    # Limpiar sesión
    if 'orden_datos' in request.session:
        del request.session['orden_datos']
    
    return render(request, 'pago_anulado.html')

# Mantener las funciones anteriores para compatibilidad
def confirmar_pago(request):
    """Redirect a la nueva función retorno_pago"""
    return retorno_pago(request)

def admin_panel(request):
    """Vista para renderizar el panel de administración"""
    return render(request, 'admin_panel.html')

@api_view(['GET'])
def listar_productos_api(request):
    """API para listar productos desde Spring Boot"""
    try:
        productos = obtener_productos()
        return Response(productos)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def crear_producto_api(request):
    """API para crear producto en Spring Boot"""
    try:
        url = "http://127.0.0.1:8089/api/productos"
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, 
                               data=json.dumps(request.data), 
                               headers=headers, 
                               timeout=5)
        
        if response.status_code == 201:
            return Response(response.json(), status=201)
        else:
            return Response({'error': 'Error al crear producto'}, status=400)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def obtener_producto_api(request, pk):
    """API para obtener un producto específico desde Spring Boot"""
    try:
        url = f"http://127.0.0.1:8089/api/productos/{pk}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Producto no encontrado'}, status=404)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['PUT'])
def actualizar_producto_api(request, pk):
    """API para actualizar producto en Spring Boot"""
    try:
        url = f"http://127.0.0.1:8089/api/productos/{pk}"
        headers = {'Content-Type': 'application/json'}
        
        response = requests.put(url, 
                              data=json.dumps(request.data), 
                              headers=headers, 
                              timeout=5)
        
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Error al actualizar producto'}, status=400)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['DELETE'])
def eliminar_producto_api(request, pk):
    """API para eliminar producto en Spring Boot"""
    try:
        url = f"http://127.0.0.1:8089/api/productos/{pk}"
        response = requests.delete(url, timeout=5)
        
        if response.status_code == 204:
            return Response(status=204)
        else:
            return Response({'error': 'Error al eliminar producto'}, status=400)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

