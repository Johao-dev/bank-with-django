# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Consultas(models.Model):
    consulta_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    fecha_consulta = models.DateField()

    class Meta:
        managed = False
        db_table = 'consultas'


class Cuentas(models.Model):
    cuenta_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    tarjeta = models.ForeignKey('Tarjetas', models.DO_NOTHING, blank=True, null=True)
    numero_cuenta = models.CharField(max_length=20)
    clave_4digitos = models.CharField(max_length=4)
    clave_6digitos = models.CharField(max_length=6)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuentas'


class Depositos(models.Model):
    deposito_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    fecha_depo = models.DateField()
    cantidad_depo = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'depositos'


class Retiros(models.Model):
    retiro_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    fecha_retiro = models.DateField()
    cantidad_retiro = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'retiros'


class Tarjetas(models.Model):
    tarjeta_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    numero = models.CharField(max_length=20)
    cvv = models.CharField(max_length=4)
    tipo_tarjeta = models.CharField(max_length=7)
    fecha_caducidad = models.DateField()
    fecha_emision = models.DateField()

    class Meta:
        managed = False
        db_table = 'tarjetas'


class Transferencias(models.Model):
    transferencia_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)
    receptor = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='receptor', related_name='transferencias_receptor_set')
    fecha_transf = models.DateField()
    cantidad_transf = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'transferencias'


class Usuarios(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=15)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
