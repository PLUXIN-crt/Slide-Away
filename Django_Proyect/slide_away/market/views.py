from django.shortcuts import render
from django.http import HttpResponse
import requests

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
    contexto = {"datos": empleados}
    return render(request, "ver_empleados.html", contexto)

def ver_menu_principal(request):
    productos = obtener_productos()
    categorias = obtener_categorias()
    marcas = obtener_marcas()
    
    # Limitar a 6 productos para la página principal
    productos_destacados = productos[:6] if productos else []
    
    print(f"Productos destacados: {len(productos_destacados)}")
    print(f"Categorías: {len(categorias)}")
    print(f"Marcas: {len(marcas)}")
    
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
    
    print(f"DEBUG - Catálogo - Productos: {len(productos)}")
    print(f"DEBUG - Catálogo - Categorías: {len(categorias)}")
    print(f"DEBUG - Catálogo - Marcas: {len(marcas)}")
    
    contexto = {
        'productos': productos,  # Todos los productos, no limitados
        'categorias': categorias,
        'marcas': marcas
    }
    return render(request, "catalogo.html", contexto)

def ver_carrito(request):
    return render(request, "carrito.html")