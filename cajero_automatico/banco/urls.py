from django.urls import path
from .views.auth_view import login_view, logout_view
from .views.operations_view import *

# create your urls here
urlpatterns = [
    path('', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('consultar/', consultar_saldo, name='consultar'),
    path('depositar/', realizar_deposito, name='depositar'),
    path('transferir/', realizar_transferencia, name='transferir'),
    path('retirar/', realizar_retiro, name='retirar'),
    path('logout/', logout_view, name='logout'),
]