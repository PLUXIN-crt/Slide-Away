from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

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

def ver_clientes(request):
    datos = [
        {'nombre':'Diego Jeldrez', 'correo':'diego@gmail.com'},
        {'nombre':'Cristobal Fuentes', 'correo':'cristobal@gmail.com'},
        {'nombre':'Pablo Figueroa', 'correo':'pablo@gmail.com'},
        {'nombre':'Benjamin Reyes', 'correo':'benjamin@gmail.com'},
        {'nombre':'Alexander Sepulveda', 'correo':'alexander@gmail.com'},
        {'nombre':'Agustin Heinz', 'correo':'agustin@gmail.com'},
        {'nombre':'Mario Garcia', 'correo':'mario@gmail.com'},
    ]
    contexto = {
        'clientes':datos
    }
    return render(request,"ver_clientes.html", contexto)

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
    url="http://127.0.0.1:8089/api/productos/dto"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Productos obtenidos: {len(data)}")
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