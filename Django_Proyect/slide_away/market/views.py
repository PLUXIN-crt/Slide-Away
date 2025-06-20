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

def guardar_venta_spring_boot(carrito_items, total, datos_cliente, numero_orden):
    """Función para guardar la venta en Spring Boot con mejor manejo de errores"""
    try:
        print(f"DEBUG - Iniciando guardado de venta: {numero_orden}")
        print(f"DEBUG - Total: {total}")
        print(f"DEBUG - Cliente: {datos_cliente}")
        print(f"DEBUG - Items carrito: {len(carrito_items)}")
        
        # Validar datos básicos
        if not numero_orden or not carrito_items or total <= 0:
            print("ERROR - Datos de venta incompletos")
            return False, None
            
        # Primero crear/verificar el cliente
        cliente_data = {
            "rut": datos_cliente.get('rut', '11111111-1'),
            "nombre": datos_cliente.get('nombre', 'Cliente'),
            "apellidos": datos_cliente.get('apellidos', 'Web'),
            "telefono": datos_cliente.get('telefono', '123456789'),
            "correo": datos_cliente.get('email', 'cliente@web.com'),
            "idComuna": 1  # Comuna por defecto
        }
        
        print(f"DEBUG - Datos cliente a enviar: {cliente_data}")
        
        # Crear cliente si no existe
        url_cliente = "http://127.0.0.1:8089/api/clientes"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response_cliente = requests.post(url_cliente, 
                                           data=json.dumps(cliente_data), 
                                           headers=headers, 
                                           timeout=10)
            print(f"DEBUG - Respuesta cliente: {response_cliente.status_code}")
            if response_cliente.status_code not in [200, 201, 409]:  # 409 = Ya existe
                print(f"ERROR - Error al crear cliente: {response_cliente.text}")
        except requests.exceptions.RequestException as e:
            print(f"ERROR - Conexión fallida con Spring Boot para cliente: {e}")
            # Continuar con la venta aunque falle el cliente
        
        # Generar número de documento válido
        try:
            # Extraer timestamp del numero_orden
            timestamp_str = numero_orden.split('_')[-1]
            numero_documento = int(timestamp_str) % 999999999  # Asegurar que no sea muy largo
        except (ValueError, IndexError):
            numero_documento = int(datetime.now().timestamp()) % 999999999
            
        print(f"DEBUG - Número documento generado: {numero_documento}")
        
        # Crear la venta con datos validados
        venta_data = {
            "numeroDocumento": numero_documento,
            "tipoDocumento": "BOLETA",
            "fechaVenta": datetime.now().strftime('%Y-%m-%d'),
            "totalVenta": float(total),
            "idTipoPago": 1,  # Webpay
            "rutCliente": datos_cliente.get('rut', '11111111-1'),
            "nombreCliente": datos_cliente.get('nombre', 'Cliente'),
            "apellidoCliente": datos_cliente.get('apellidos', 'Web'),
            "idSucursal": 1  # Sucursal por defecto
        }
        
        print(f"DEBUG - Datos venta a enviar: {venta_data}")
        
        url_venta = "http://127.0.0.1:8089/api/ventas"
        
        try:
            response_venta = requests.post(url_venta, 
                                         data=json.dumps(venta_data), 
                                         headers=headers, 
                                         timeout=10)
            
            print(f"DEBUG - Respuesta venta: {response_venta.status_code}")
            print(f"DEBUG - Contenido respuesta: {response_venta.text}")
            
            if response_venta.status_code == 201:
                print(f"SUCCESS - Venta guardada exitosamente: {numero_documento}")
                return True, numero_documento
            else:
                print(f"ERROR - Error al guardar venta: {response_venta.status_code}")
                print(f"ERROR - Detalle: {response_venta.text}")
                return False, numero_documento  # Retornar el número aunque falle
                
        except requests.exceptions.Timeout:
            print("ERROR - Timeout al conectar con Spring Boot para venta")
            return False, numero_documento
        except requests.exceptions.ConnectionError:
            print("ERROR - No se pudo conectar con Spring Boot para venta")
            return False, numero_documento
        except requests.exceptions.RequestException as e:
            print(f"ERROR - Error de conexión con Spring Boot: {e}")
            return False, numero_documento
            
    except Exception as e:
        print(f"ERROR GENERAL - Error al guardar venta: {e}")
        import traceback
        print(f"ERROR TRACEBACK: {traceback.format_exc()}")
        return False, None

def retorno_pago(request):
    """Vista que recibe el retorno después del pago - Versión Funcional"""
    if not TRANSBANK_AVAILABLE or transaction is None:
        return render(request, 'pago_resultado.html', {
            'success': False,
            'error': 'Transbank SDK no está configurado'
        })
    
    token = request.GET.get('token_ws') or request.POST.get('token_ws')
    
    if not token:
        return render(request, 'pago_resultado.html', {
            'success': False,
            'error': 'Token de pago no encontrado'
        })
    
    try:
        # Confirmar transacción con Transbank
        result = transaction.commit(token)
        
        print(f"DEBUG - Respuesta de confirmación: {result}")
        
        # Obtener datos de la orden desde la sesión
        orden_datos = request.session.get('orden_datos', {})
        
        # Verificar que la respuesta sea exitosa
        if result.get('status') == 'AUTHORIZED':
            # Pago exitoso - GUARDAR EN BASE DE DATOS
            carrito_items = orden_datos.get('carrito', [])
            total = result.get('amount', orden_datos.get('total', 0))
            datos_cliente = orden_datos.get('cliente', {})
            numero_orden = result.get('buy_order')
            
            print(f"DEBUG - Iniciando guardado de venta para orden: {numero_orden}")
            
            # Pre-calcular totales para cada item del carrito
            carrito_procesado = []
            for item in carrito_items:
                item_procesado = item.copy()
                subtotal = float(item.get('precio', 0)) * int(item.get('cantidad', 0))
                despacho = 5000 if item.get('modalidadEntrega') == 'despacho' else 0
                item_procesado['subtotal'] = subtotal
                item_procesado['despacho'] = despacho
                item_procesado['total_item'] = subtotal + despacho
                carrito_procesado.append(item_procesado)
            
            # Guardar venta en Spring Boot con mejor manejo de errores
            venta_guardada, numero_documento = guardar_venta_spring_boot(
                carrito_items, total, datos_cliente, numero_orden
            )
            
            print(f"DEBUG - Resultado guardado venta: {venta_guardada}, documento: {numero_documento}")
            
            contexto = {
                'success': True,
                'orden': numero_orden,
                'numero_documento': numero_documento,
                'total': total,
                'carrito': carrito_procesado,
                'cliente': datos_cliente,
                'venta_guardada': venta_guardada,
                'error_detalle': 'Verifique que Spring Boot esté ejecutándose en puerto 8089' if not venta_guardada else None,
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
            return render(request, 'pago_resultado.html', {
                'success': False,
                'error': f'Pago no autorizado. Estado: {result.get("status", "UNKNOWN")}'
            })
            
    except Exception as e:
        print(f"ERROR - Error al confirmar pago: {e}")
        import traceback
        print(f"ERROR TRACEBACK: {traceback.format_exc()}")
        return render(request, 'pago_resultado.html', {
            'success': False,
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

def admin_boleta(request):
    """Vista para renderizar el panel de administración de boletas"""
    return render(request, 'admin_boleta.html')

def admin_cliente(request):
    """Vista para renderizar el panel de administración de clientes"""
    return render(request, 'admin_cliente.html')

def obtener_boletas():
    """Función para obtener ventas desde Spring Boot"""
    url = "http://127.0.0.1:8089/api/ventas"  # Cambiar endpoint
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Ventas obtenidas: {len(data)}")
            return data
        else:
            print(f"Error en ventas: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al obtener ventas: {e}")
        return []

def obtener_clientes():
    """Función para obtener clientes desde Spring Boot"""
    url = "http://127.0.0.1:8089/api/clientes"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Clientes obtenidos: {len(data)}")
            return data
        else:
            print(f"Error en clientes: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al obtener clientes: {e}")
        return []

def obtener_comunas():
    """Función para obtener comunas desde Spring Boot"""
    url = "http://127.0.0.1:8089/api/comunas"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Comunas obtenidas: {len(data)}")
            return data
        else:
            print(f"Error en comunas: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al obtener comunas: {e}")
        return []

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

@api_view(['GET'])
def listar_boletas_api(request):
    """API para listar ventas desde Spring Boot"""
    try:
        boletas = obtener_boletas()
        return Response(boletas)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def crear_boleta_api(request):
    """API para crear venta en Spring Boot"""
    try:
        url = "http://127.0.0.1:8089/api/ventas"  # Cambiar endpoint
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, 
                               data=json.dumps(request.data), 
                               headers=headers, 
                               timeout=5)
        
        if response.status_code == 201:
            return Response(response.json(), status=201)
        else:
            return Response({'error': 'Error al crear venta'}, status=400)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def obtener_boleta_api(request, pk):
    """API para obtener una venta específica desde Spring Boot"""
    try:
        url = f"http://127.0.0.1:8089/api/ventas/{pk}"  # Cambiar endpoint
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Venta no encontrada'}, status=404)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['PUT'])
def actualizar_boleta_api(request, pk):
    """API para actualizar venta en Spring Boot"""
    try:
        url = f"http://127.0.0.1:8089/api/ventas/{pk}"  # Cambiar endpoint
        headers = {'Content-Type': 'application/json'}
        
        response = requests.put(url, 
                              data=json.dumps(request.data), 
                              headers=headers, 
                              timeout=5)
        
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Error al actualizar venta'}, status=400)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['DELETE'])
def eliminar_boleta_api(request, pk):
    """API para eliminar venta en Spring Boot"""
    try:
        url = f"http://127.0.0.1:8089/api/ventas/{pk}"  # Cambiar endpoint
        response = requests.delete(url, timeout=5)
        
        if response.status_code == 204:
            return Response(status=204)
        else:
            return Response({'error': 'Error al eliminar venta'}, status=400)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def listar_clientes_api(request):
    """API para listar clientes desde Spring Boot"""
    try:
        clientes = obtener_clientes()
        return Response(clientes)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def listar_comunas_api(request):
    """API para listar comunas desde Spring Boot"""
    try:
        comunas = obtener_comunas()
        return Response(comunas)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def crear_cliente_api(request):
    """API para crear cliente en Spring Boot"""
    try:
        url = "http://127.0.0.1:8089/api/clientes"
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, 
                               data=json.dumps(request.data), 
                               headers=headers, 
                               timeout=5)
        
        if response.status_code == 201:
            return Response(response.json(), status=201)
        else:
            return Response({'error': 'Error al crear cliente'}, status=400)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def obtener_cliente_api(request, pk):
    """API para obtener un cliente específico desde Spring Boot"""
    try:
        url = f"http://127.0.0.1:8089/api/clientes/{pk}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Cliente no encontrado'}, status=404)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['PUT'])
def actualizar_cliente_api(request, pk):
    """API para actualizar cliente en Spring Boot"""
    try:
        url = f"http://127.0.0.1:8089/api/clientes/{pk}"
        headers = {'Content-Type': 'application/json'}
        
        response = requests.put(url, 
                              data=json.dumps(request.data), 
                              headers=headers, 
                              timeout=5)
        
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Error al actualizar cliente'}, status=400)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['DELETE'])
def eliminar_cliente_api(request, pk):
    """API para eliminar cliente en Spring Boot"""
    try:
        url = f"http://127.0.0.1:8089/api/clientes/{pk}"
        response = requests.delete(url, timeout=5)
        
        if response.status_code == 204:
            return Response(status=204)
        else:
            return Response({'error': 'Error al eliminar cliente'}, status=400)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)

