from datetime import date
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from banco.models import *
from django.db import transaction
from decimal import Decimal


"""
    Verifica que el usuario haya inciado sesion, si es asi
    envia el nombre del usuario al archivo dashboard.html
"""
def dashboard_view(request):
    # verifica si el usuario esta autenticado
    if 'usuario' in request.session:
        nombre_usuario = request.session['usuario']
    else:
        return redirect('login')
    
    return render(request, 'banco/dashboard.html', {'nombre_completo': nombre_usuario})


"""
    Esta funcion es la que se encarga de hacer la consulta a
    la base de datos sobre el saldo del usuario y luego registra
    la consulta en la tabla de consultas.
"""
def consultar_saldo(request):
    if request.method == 'POST':
        try:
            nombre_usuario = request.session['usuario']
            usuario = Usuarios.objects.get(nombres=nombre_usuario)
            cuenta = Cuentas.objects.get(usuario_id=usuario.usuario_id)

            with transaction.atomic():
                Consultas.objects.create(usuario=usuario, fecha_consulta=date.today())

            return JsonResponse({'saldo': cuenta.saldo})
        except Cuentas.DoesNotExist:
            return JsonResponse({'error': 'Cuenta no encontrada'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al procesar la solicitud'}, status=405)
    

"""
    Esta funcion recibe datos del usuario para realizar una
    transferencia, recibe informacion del usuario que recibira
    el dinero, como su numero de tarjeta y su nombre, tambien
    recibe la cantidad a transferir.

    Valida si el usuario que ha iniciado sesion tiene la cantidad
    para transferir, si la tiene se realiza la transferencia y
    se actualizan los datos en la base de datos.
"""
def realizar_transferencia(request):
    if request.method == 'POST':
        try:
            nombre_usuario = request.session['usuario']

            data = json.loads(request.body)
            num_tarjeta_receptor = data['tarjeta_receptor']
            nombre_receptor = data['nombre_receptor']
            cantidad = Decimal(data['cantidad'])

            usuario = Usuarios.objects.get(nombres=nombre_usuario)
            cuenta_usuario = Cuentas.objects.get(usuario_id=usuario.usuario_id)

            num_tarj_receptor = Tarjetas.objects.get(numero=num_tarjeta_receptor)
            cuenta_receptor = Cuentas.objects.get(tarjeta_id=num_tarj_receptor.tarjeta_id)
            receptor = Usuarios.objects.get(nombres=nombre_receptor)

            if cuenta_usuario.saldo >= cantidad:
                # actualizar los datos
                cuenta_usuario.saldo -= cantidad
                cuenta_receptor.saldo += cantidad
                cuenta_usuario.save()
                cuenta_receptor.save()
                
                # registrar la transferencia
                Transferencias.objects.create(
                    usuario=usuario,
                    receptor=receptor,
                    fecha_transf=date.today(),
                    cantidad_transf=cantidad
                )
                return JsonResponse({"mensaje":"Transferencia realizada con exito"}, status=200)
            else:
                return JsonResponse({"mensaje": "Saldo insuficiente"}, status=400)
        except Cuentas.DoesNotExist:
            return JsonResponse({"mensaje": "Una de las cuentas no fue encontrada."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"mensaje": "Error al procesar la solicitud."}, status=400)
        
    return JsonResponse({"mensaje": "Método no permitido."}, status=405)
    

"""
    Esta funcion toma los datos del usuario a traves del inicio
    de sesion, recibe la cantidad a depositar y realiza el deposito
    en la base de datos.
"""
def realizar_deposito(request):
    if request.method == "POST":
        try:
            nombre_usuario = request.session['usuario']
            usuario = Usuarios.objects.get(nombres=nombre_usuario)

            data = json.loads(request.body)
            cantidad = Decimal(data['cantidad'])

            cuenta = Cuentas.objects.get(usuario_id=usuario.usuario_id)
            cuenta.saldo += cantidad
            cuenta.save()
            
            # registrar el deposito
            deposito = Depositos()
            deposito.usuario = usuario
            deposito.fecha_depo = date.today()
            deposito.cantidad_depo = cantidad
            deposito.save()

            return JsonResponse({"mensaje": "Depósito realizado con éxito."}, status=200)
        except Cuentas.DoesNotExist:
            return JsonResponse({"mensaje": "La cuenta no fue encontrada."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"mensaje": "Error al procesar la solicitud."}, status=400)

    return JsonResponse({"mensaje": "Método no permitido."}, status=405)
    

"""
    Esta funcion toma los datos del usuario a traves del inicio
    de sesion, recibe la cantidad a retirar y realiza el retiro
    en la base de datos.
"""
def realizar_retiro(request):
    if request.method == "POST":
        try:
            nombre_usuario = request.session['usuario']
            usuario = Usuarios.objects.get(nombres=nombre_usuario)

            data = json.loads(request.body)
            cantidad = Decimal(data['cantidad'])

            cuenta = Cuentas.objects.get(usuario_id=usuario.usuario_id)
            if cuenta.saldo >= cantidad:
                cuenta.saldo -= cantidad
                cuenta.save()
                
                # registrar el retiro
                Retiros.objects.create(
                    usuario=usuario,
                    fecha_retiro=date.today(),
                    cantidad_retiro=cantidad
                )
                return JsonResponse({"mensaje": "Retiro realizado con éxito."}, status=200)
            else:
                return JsonResponse({"mensaje": "Saldo insuficiente."}, status=400)
        except Cuentas.DoesNotExist:
            return JsonResponse({"mensaje": "La cuenta no fue encontrada."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"mensaje": "Error al procesar la solicitud."}, status=400)

    return JsonResponse({"mensaje": "Método no permitido."}, status=405)