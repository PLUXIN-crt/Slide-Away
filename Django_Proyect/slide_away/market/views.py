from django.shortcuts import render
from django.http import HttpResponse
import requests
def ver_inicio(request):
    return render(request,"inicio.html")
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
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return None

def ver_empleados(request):
    empleados = obtener_empleados()
    contexto = { "datos":empleados}
    return render (request, "ver_empleados.html", contexto)