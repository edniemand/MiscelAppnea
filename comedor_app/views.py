from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponse,HttpResponseRedirect
from django.db import connections,transaction
from django.db.models import Sum
from comedor_app.models import Comedor,ComedorDetalle,Opcion
from comedor_app.forms import ComedorForm,ComedorDetalleForm,OpcionForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

# Create your views here.
class ComedorView(LoginRequiredMixin,TemplateView):
    template_name = 'comedor_app/comedor.html'

class Consumos(LoginRequiredMixin,TemplateView):
    template_name = 'comedor_app/consumos.html'

    empresa = ''
    ejercicio = ''
    semana = ''

    def get_current_week_sql(self):
        week = datetime.today().isocalendar()[1] + 1
        year = datetime.today().isocalendar()[0]
        #print('YEAR: ',year,' WEEK: ', week)
        return week,year

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.empresa == '':
            self.semana,self.ejercicio = self.get_current_week_sql()
            context_dit = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Seleccione una empresa...'}
            return context_dit
        else:
            comedor = Comedor.objects.filter(empresa=self.empresa,ejercicio=self.ejercicio,semana=self.semana)
            if comedor:
                emp_list = ComedorDetalle.objects.filter(id_comedor=comedor[0]).order_by('codigo_empleado')
                departamentos = ComedorDetalle.objects.values('depto_empleado').annotate(suma_depto = Sum('total')).filter(id_comedor=comedor[0])
                print(departamentos)
                #
                emp_dict = {"empleados":emp_list,"empresa":self.empresa,"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Exitoso!','departamentos':departamentos}
                return emp_dict
            else:
                contexto = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'No se encontraron resultados con los parametros utilizados,verifiquelos e intente nuevamente!'}
                return contexto

    def post(self, request, **kwargs):

        if request.method == 'POST':
            my_data = request.POST

            self.empresa = my_data['empresa']
            self.ejercicio = my_data['ejercicio']
            self.semana = my_data['semana']

            context = self.get_context_data(**kwargs)

        return render(request,'comedor_app/consumos.html',context)

class GenerarListas(LoginRequiredMixin,TemplateView):
    template_name = 'comedor_app/generar_listas.html'

    empresa = ''
    ejercicio = ''
    semana = ''

    def get_current_week_sql(self):
        week = datetime.today().isocalendar()[1] + 1
        year = datetime.today().isocalendar()[0]
        #print('YEAR: ',year,' WEEK: ', week)
        return week,year

    def my_custom_sql(self):
        if self.empresa == 'INNOVACIONES':
            connec = 'nominasInnova'
            nombreEmpr = 'Innovaciones Constructivas S.A. de C.V.'
        elif self.empresa == 'PRESTADORA':
            connec = 'nominasPrestadora'
            nombreEmpr = 'Prestadora de Servicios S.A. de C.V.'
        elif self.empresa == 'PREFABRICADOS':
            connec = 'nominasPresol'
            nombreEmpr = 'Prefabricados y Soluciones S.A. de C.V.'

        with connections[connec].cursor() as cursor:

            cursor.execute("SELECT t1.idempleado,t1.codigoempleado,t1.nombrelargo,t3.descripcion \
                            FROM dbo.nom10001 t1 \
                            INNER JOIN dbo.nom10003 t3 ON t3.iddepartamento = t1.iddepartamento \
                            WHERE t1.estadoempleado != 'B' ORDER BY t1.nombrelargo")

            list = cursor.fetchall()

            objEmpleado=''
            listEmp = []
            for item in list:
                objEmpleado = {'id_empleado':item[0],'codigo_empleado':item[1],'nombre_empleado':item[2],'depto_empleado':item[3],
                            'lunes':0,'martes':0,'miercoles':0,'jueves':0,'viernes':0,'sabado':0,'domingo':0,
                            'total':0}

                listEmp.append(objEmpleado)

        return listEmp

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.empresa == '':
            # self.empresa = 'INNOVACIONES'
            self.semana,self.ejercicio = self.get_current_week_sql()
            context_dit = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Seleccione una empresa...'}
            return context_dit
        else:
            # emp_list = ComedorDetalle.objects.order_by('codigo_empleado')
            # emp_dict = {"empleados":emp_list}
            #context['empleados'] = self.my_custom_sql()
            empleados = self.my_custom_sql()
            context_dit = {"empleados":empleados,"empresa":self.empresa,"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Exitoso!'}
            return context_dit


    def post(self, request, **kwargs):
        if request.method == 'POST':
            if 'buscar' in request.POST:
                #print("SE DIO CLICK EN EL BOTON BUSCAR")
                my_data = request.POST

                self.empresa = my_data['empresa']
                self.ejercicio = my_data['ejercicio']
                self.semana = my_data['semana']

                context = self.get_context_data(**kwargs)

                return render(request,'comedor_app/generar_listas.html',context)
            else:
                #print("SE DIO CLICK EN EL BOTON GUARDAR")
                my_data = request.POST

                self.empresa = my_data['empresa']
                self.ejercicio = my_data['ejercicio']
                self.semana = my_data['semana']

                context = self.get_context_data(**kwargs)

                formC = ComedorForm(request.POST)
                if formC.is_valid():
                    comedor = formC.save(commit=False)
                    comedor.save()

                    for emp in context['empleados']:
                        comedorDet = ComedorDetalle(id_comedor = comedor,id_empleado = emp['id_empleado'],codigo_empleado = emp['codigo_empleado'],nombre_empleado = emp['nombre_empleado'], \
                                            depto_empleado = emp['depto_empleado'],lunes = emp['lunes'],martes = emp['martes'],miercoles = emp['miercoles'],jueves = emp['jueves'],
                                            viernes = emp['viernes'],sabado = emp['sabado'],domingo = emp['domingo'],total = emp['total'])
                        comedorDet.save()

                        context_dit = {"empresa":self.empresa,"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Se guardó con éxito!'}
                return render(request,'comedor_app/generar_listas.html',context_dit)

class Opciones(LoginRequiredMixin,TemplateView):
    template_name = 'comedor_app/opciones.html'

    empresa = ''
    ejercicio = ''
    semana = ''

    def get_current_week_sql(self):
        week = datetime.today().isocalendar()[1] + 1
        year = datetime.today().isocalendar()[0]

        return week,year

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = OpcionForm()
        if self.empresa == '':
            self.semana,self.ejercicio = self.get_current_week_sql()
            context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Seleccione una empresa...','form':form}
            return context_dict
        else:
            opcion_list = Opcion.objects.filter(empresa=self.empresa,ejercicio=self.ejercicio,semana=self.semana)
            if len(opcion_list):
                opc_dict = {"opciones":opcion_list,"empresa":self.empresa,"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Exitoso!','form':form}
                return opc_dict
            else:
                context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'No se encontraron resultados con los parametros utilizados,verifiquelos e intente nuevamente!','form':form}
                return context_dict

    def post(self, request, **kwargs):
        if request.method == 'POST':
            if 'buscar' in request.POST:
                #print("SE DIO CLICK EN EL BOTON BUSCAR")
                my_data = request.POST

                self.empresa = my_data['empresa']
                self.ejercicio = my_data['ejercicio']
                self.semana = my_data['semana']

                context = self.get_context_data(**kwargs)

                return render(request,'comedor_app/opciones.html',context)
            else:
                #print("SE DIO CLICK EN EL BOTON GUARDAR")
                my_data = request.POST
                #print('MY_DATA: ',my_data)
                comedor = Comedor.objects.filter(pk=my_data['id_comedor'])[0]
                #print('EMPRESA: ',comedor.empresa)
                self.empresa = comedor.empresa
                self.ejercicio = my_data['ejercicio']
                self.semana = my_data['semana']

                context = self.get_context_data(**kwargs)

                form = OpcionForm(request.POST)
                if form.is_valid():
                    opcion = form.save(commit=False)
                    opcion.save()

                context_dict = {"empresa":self.empresa,"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Se guardó con éxito!','form':form}
                return render(request,'comedor_app/opciones.html',context_dict)

def load_empleados(request):
    id_comedor = request.GET.get('id_comedor')
    detalle_comedor = ComedorDetalle.objects.filter(id_comedor=id_comedor).order_by('codigo_empleado')
    return render(request, 'comedor_app/change_form.html', {'empleados': detalle_comedor})
