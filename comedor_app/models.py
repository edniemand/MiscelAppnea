from django.db import models

# Create your models here.
class Comedor(models.Model):
    empresa = models.CharField(max_length=128)
    ejercicio = models.IntegerField(blank=True, null=True)
    semana = models.IntegerField(blank=True, null=True)
    aplicado = models.BooleanField()
    validado = models.BooleanField()
    bloqueado = models.BooleanField()

    def __str__(self):
        return self.empresa + ' semana ' + str(self.semana)

class ComedorDetalle(models.Model):
    id_comedor = models.ForeignKey(Comedor,on_delete=models.PROTECT,related_name="lineas")
    id_empleado = models.IntegerField(blank=True, null=True)
    codigo_empleado = models.CharField(max_length=128)
    nombre_empleado = models.CharField(max_length=128)
    depto_empleado = models.CharField(max_length=128)
    lunes = models.IntegerField(blank=True, null=True)
    martes = models.IntegerField(blank=True, null=True)
    miercoles = models.IntegerField(blank=True, null=True)
    jueves = models.IntegerField(blank=True, null=True)
    viernes = models.IntegerField(blank=True, null=True)
    sabado = models.IntegerField(blank=True, null=True)
    domingo = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre_empleado

class Opcion(models.Model):
    empresa = models.CharField(max_length=128)
    ejercicio = models.IntegerField(blank=True, null=True)
    semana = models.IntegerField(blank=True, null=True)
    id_comedor = models.ForeignKey(Comedor,on_delete=models.PROTECT, null=True)
    id_comedor_detalle = models.ForeignKey(ComedorDetalle,on_delete=models.PROTECT, null=True)
    dia = models.CharField(max_length=10)
    comida = models.TextField(null=True)

    def __str__(self):
        return str(self.semana)
