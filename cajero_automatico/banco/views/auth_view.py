from django.shortcuts import render, redirect
from django.http import HttpResponse
from banco.models import Usuarios, Tarjetas, Cuentas

"""
    Esta funcion verifica que el metodo de la peticion
    sea POST, si es asi recupera los datos del formulario
    login.html:

        - dni
        - numero_tarjeta
        - clave

    Luego de verificar que la peticion sea POST, recupera
    informacion de la base de datos. Valida que el usuario
    exista, si es asi registra al usuario en la sesion y
    redirecciona al dashboard.
"""
def login_view(request):
    if request.method == 'POST':
        # Procesa el login (validación de DNI, número de tarjeta y clave)
        dni = request.POST.get('dni')
        numero_tarjeta = request.POST.get('numero_tarjeta')
        clave = request.POST.get('clave')

        try:
            # valida los datos ingresados
            usuario = Usuarios.objects.get(dni=dni)
            tarjeta = Tarjetas.objects.get(usuario=usuario.usuario_id, numero=numero_tarjeta)
            cuenta = Cuentas.objects.get(usuario_id=usuario.usuario_id, clave_6digitos=clave)

            # si las credenciales son correctas, redirecciona al dashboard
            if cuenta.clave_6digitos == clave and tarjeta.numero == numero_tarjeta and usuario.dni == dni:
                request.session['usuario'] = usuario.nombres  # guarda el nombre del usuario en la sesión
                return redirect('dashboard')
            else:
                return HttpResponse("Credenciales invalidas", status=401)
            
        except Usuarios.DoesNotExist:
            return HttpResponse("Usuario no encontrado", status=404)
        except Tarjetas.DoesNotExist:
            return HttpResponse("Tarjeta no válida", status=403)

    return render(request, 'banco/login.html')



"""
    Esta funcion verifica que la peticion sea POST, si es asi
    elimina la sesion del usuario y redirecciona al archivo de login.html
"""
def logout_view(request):
    if request.method == 'POST':
        # Cierra la sesión
        del request.session['usuario']
        return redirect('login')