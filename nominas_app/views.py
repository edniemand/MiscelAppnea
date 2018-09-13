from django.shortcuts import render
from django.views.generic import TemplateView
from django.db import connections,transaction
from datetime import datetime,timedelta
#from comedor_app.models import Comedor,ComedorDetalle,Opcion
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
# Create your views here.
class Nominas(LoginRequiredMixin,TemplateView):
    template_name = 'nominas_app/nominas.html'

class Alimentos(LoginRequiredMixin,TemplateView):
    template_name = 'nominas_app/alimentos.html'

    empresa = ''
    ejercicio = ''
    semana = ''
    acumulado = ''

    def get_current_week_sql(self):
        week = datetime.today().isocalendar()[1] -1
        year = datetime.today().isocalendar()[0]
        #print('YEAR: ',year,' WEEK: ', week)
        return week,year

    def my_custom_sql(self):

        if self.empresa == 'INNOVACIONES':
            connec = 'nominasInnova'
            concepto = 135
        elif self.empresa == 'PRESTADORA':
            connec = 'nominasPrestadora'
            concepto = 149
        elif self.empresa == 'PREFABRICADOS':
            connec = 'nominasPresol'
            concepto = 135

        if self.acumulado:
            dbase = 8
        else:
            dbase = 7

        with connections[connec].cursor() as cursor:

            cursor.execute("SELECT t3.descripcion AS Departamento, sum(t7.valor) AS Total,(sum(t7.valor)*36) AS Importe \
                            FROM dbo.nom1000{} t7 \
                            INNER JOIN dbo.nom10001 t1 ON t1.idempleado = t7.idempleado \
                            INNER JOIN dbo.nom10003 t3 ON t3.iddepartamento = t1.iddepartamento \
                            INNER JOIN dbo.nom10002 t2 ON t2.idperiodo = t7.idperiodo \
                            WHERE t7.idconcepto={} AND t7.valor!=0 AND t2.numeroperiodo={} AND t2.ejercicio={} \
                            GROUP BY t3.descripcion \
                            ORDER BY Total".\
                            format(dbase,concepto,self.semana,self.ejercicio))

            list = cursor.fetchall()
            #print(list)
            objDepto = ''
            listDepto = []
            for item in list:
                depto = item[0]
                total = item[1]
                importe = item[2]

                cursor.execute("SELECT t1.codigoempleado Codigo, \
                                t1.nombrelargo Empleado, \
                                t7.valor, \
                                (t7.valor * 36)AS Descuento, \
                                t2.fechainicio AS FechaInicio, \
                                t2.fechafin AS FechaFin  \
                                FROM dbo.nom1000{} t7 \
                                INNER JOIN dbo.nom10001 t1 ON t1.idempleado = t7.idempleado \
                                INNER JOIN dbo.nom10003 t3 ON t3.iddepartamento = t1.iddepartamento \
                                INNER JOIN dbo.nom10002 t2 ON t2.idperiodo = t7.idperiodo \
                                WHERE t7.idconcepto={} AND t7.valor!=0 AND t2.numeroperiodo={} AND t2.ejercicio={} AND t3.descripcion = '{}'".\
                                format(dbase,concepto,self.semana,self.ejercicio,depto))
                list2 = cursor.fetchall()
                #print(list2)
                objEmpleado=''
                listEmp = []
                for item2 in list2:
                    date_ini = item2[4].strftime('%d')
                    date_fin = item2[5].strftime('%d-%m-%Y')
                    objEmpleado = {'num_emp':item2[0],'nombre_emp':item2[1],'total':item2[2],
                                'importe':item2[3],'fecha_inicio':date_ini,'fecha_fin':date_fin}

                    listEmp.append(objEmpleado)

                objDepto = {'depto':depto,'total':total,'importe':importe,'empleados':listEmp}

                listDepto.append(objDepto)


        return listDepto

    def get_context_data(self, **kwargs):
        # print('ENTRO : get_context_data')
        context = super().get_context_data(**kwargs)
        if self.empresa == '':
            self.semana,self.ejercicio = self.get_current_week_sql()
            context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Seleccione una empresa...'}
            return context_dict
        else:
            #context['empleados'] = self.my_custom_sql()
            empleados = self.my_custom_sql()
            if len(empleados)>0:
                #context['departamentos'] = self.my_custom_sql()[1]
                context_dict = {'empleados':empleados,"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'Exitoso!'}
                return context_dict
            else:
                context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'No se encontraron resultados con los parámetros utilizados, verifíquelos e intente nuevamente!'}
                return context_dict

    def post(self, request, **kwargs):
        #print(request.POST)
        if request.method == 'POST':
            #if 'buscar' in request.POST
            my_data = request.POST
            acumul = request.POST.get('acumulado', False)

            self.empresa = my_data['empresa']
            self.ejercicio = my_data['ejercicio']
            self.semana = my_data['semana']
            self.acumulado = acumul

            context = self.get_context_data(**kwargs)

        return render(request,'nominas_app/alimentos.html',context)

class Bancos(LoginRequiredMixin,TemplateView):
    template_name = 'nominas_app/bancos.html'

    empresa = ''
    ejercicio = ''
    semana = ''
    acumulado = ''
    tipo_periodo = ''

    def get_current_week_sql(self):
        week = datetime.today().isocalendar()[1] -1
        year = datetime.today().isocalendar()[0]
        #print('YEAR: ',year,' WEEK: ', week)
        return week,year

    def my_custom_sql(self):

        if self.empresa == 'INNOVACIONES':
            connec = 'nominasInnova'
        elif self.empresa == 'PRESTADORA':
            connec = 'nominasPrestadora'
        elif self.empresa == 'PREFABRICADOS':
            connec = 'nominasPresol'


        if self.acumulado:
            dbase = 8
        else:
            dbase = 7

        if self.tipo_periodo:
            tipo = 1
        else:
            tipo = 2


        with connections[connec].cursor() as cursor:

            cursor.execute("SELECT  \
                t1.codigoempleado Codigo,  \
                t1.nombrelargo Nombre,  \
                t3.descripcion Departamento,  \
                t1.cuentapagoelectronico Cuenta,  \
                t7.importetotal Total,  \
                t2.fechainicio AS FechaInicio,  \
                t2.fechafin AS FechaFin  \
                FROM dbo.nom1000{} t7  \
                INNER JOIN dbo.nom10001 t1 ON t1.idempleado = t7.idempleado  \
                INNER JOIN dbo.nom10003 t3 ON t3.iddepartamento = t1.iddepartamento  \
                INNER JOIN dbo.nom10002 t2 ON t2.idperiodo = t7.idperiodo  \
                WHERE t7.idconcepto=1 AND t2.idtipoperiodo={} AND t2.numeroperiodo={} AND t2.ejercicio={}".format(dbase,tipo,self.semana,self.ejercicio))

            list = cursor.fetchall()
            #print(list)
            objBancos=''
            listBancos = []
            for item in list:
                date_ini = item[5].strftime('%d')
                date_fin = item[6].strftime('%d-%m-%Y')
                if self.tipo_periodo:
                    textperiod = str(self.semana) + ' Ext'
                else:
                    textperiod = self.semana

                objBancos = {'codigoempleado':item[0],'nombrelargo':item[1],'depto':item[2],'cuentapagoelectronico':item[3],
                            'importetotal':"{:,}".format(round(item[4],2)),'fecha_inicio':date_ini,'fecha_fin':date_fin,'empresa':self.empresa,'ejercicio':self.ejercicio,'semana':textperiod}
                listBancos.append(objBancos)

            cursor.execute("SELECT t3.descripcion AS depto, sum(t7.importetotal) AS total \
                FROM dbo.nom1000{} t7 \
                INNER JOIN dbo.nom10001 t1 ON t1.idempleado = t7.idempleado \
                INNER JOIN dbo.nom10003 t3 ON t3.iddepartamento = t1.iddepartamento \
                INNER JOIN dbo.nom10002 t2 ON t2.idperiodo = t7.idperiodo \
                WHERE  t7.idconcepto=1 AND t2.idtipoperiodo={} AND t2.numeroperiodo={} AND t2.ejercicio={} \
                GROUP BY t3.descripcion  \
                ORDER BY total".format(dbase,tipo,self.semana,self.ejercicio))

            list = cursor.fetchall()
            #print(list)
            objDeptos=''
            listDeptos = []
            for item in list:
                objDeptos = {'depto':item[0],'total':format(round(item[1],2))}
                listDeptos.append(objDeptos)

        return listBancos,listDeptos

    def get_context_data(self, **kwargs):
        # print('ENTRO : get_context_data')
        context = super().get_context_data(**kwargs)
        if self.empresa == '':
            self.semana,self.ejercicio = self.get_current_week_sql()
            context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Seleccione una empresa...'}
            return context_dict
        else:
            bancos = self.my_custom_sql()[0]
            departamentos = self.my_custom_sql()[1]
            if len(bancos)>0:
                context_dict = {'bancos':bancos,'departamentos':departamentos,"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'Exitoso!'}
                return context_dict
            else:
                context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'No se encontraron resultados con los parámetros utilizados, verifíquelos e intente nuevamente!'}
                return context_dict

        return context

    def post(self, request, **kwargs):

        if request.method == 'POST':
            my_data = request.POST
            acumul = request.POST.get('acumulado', False)
            tipo = request.POST.get('tipo', False)

            self.empresa = my_data['empresa']
            self.ejercicio = my_data['ejercicio']
            self.semana = my_data['semana']
            self.acumulado = acumul
            self.tipo_periodo = tipo

            context = self.get_context_data(**kwargs)

        return render(request,'nominas_app/bancos.html',context)

class Dispersion(LoginRequiredMixin,TemplateView):
    template_name = 'nominas_app/dispersion.html'

    empresa = ''
    ejercicio = ''
    semana = ''
    acumulado = ''
    tipo_periodo = ''

    def get_current_week_sql(self):
        week = datetime.today().isocalendar()[1] -1
        year = datetime.today().isocalendar()[0]
        #print('YEAR: ',year,' WEEK: ', week)
        return week,year

    def my_custom_sql(self):

        if self.empresa == 'SERA':
            connec = 'nominasSERA'
        elif self.empresa == 'COMPLEMENTO':
            connec = 'nominasComplem'


        if self.acumulado:
            dbase = 8
        else:
            dbase = 7

        if self.tipo_periodo:
            tipo = 1
        else:
            tipo = 2


        with connections[connec].cursor() as cursor:

            cursor.execute("SELECT  \
                t1.codigoempleado Codigo,  \
                t1.nombrelargo Nombre,  \
                t3.descripcion Departamento,  \
                t1.cuentapagoelectronico Cuenta,  \
                t7.importetotal Total,  \
                t2.fechainicio AS FechaInicio,  \
                t2.fechafin AS FechaFin  \
                FROM dbo.nom1000{} t7  \
                INNER JOIN dbo.nom10001 t1 ON t1.idempleado = t7.idempleado  \
                INNER JOIN dbo.nom10003 t3 ON t3.iddepartamento = t1.iddepartamento  \
                INNER JOIN dbo.nom10002 t2 ON t2.idperiodo = t7.idperiodo  \
                WHERE t7.idconcepto=1 AND t2.idtipoperiodo={} AND t2.numeroperiodo={} AND t2.ejercicio={}".format(dbase,tipo,self.semana,self.ejercicio))

            list = cursor.fetchall()
            #print(list)
            objDispersion=''
            listDispersion = []
            for item in list:
                date_ini = item[5].strftime('%d')
                date_fin = item[6].strftime('%d-%m-%Y')
                if self.tipo_periodo:
                    textperiod = str(self.semana) + ' Ext'
                else:
                    textperiod = self.semana

                objDispersion = {'codigoempleado':item[0],'nombrelargo':item[1],'depto':item[2],'cuentapagoelectronico':item[3],
                            'importetotal':"{:,}".format(round(item[4],2)),'fecha_inicio':date_ini,'fecha_fin':date_fin,'empresa':self.empresa,'ejercicio':self.ejercicio,'semana':textperiod}
                listDispersion.append(objDispersion)

            cursor.execute("SELECT t3.descripcion AS depto, sum(t7.importetotal) AS total \
                FROM dbo.nom1000{} t7 \
                INNER JOIN dbo.nom10001 t1 ON t1.idempleado = t7.idempleado \
                INNER JOIN dbo.nom10003 t3 ON t3.iddepartamento = t1.iddepartamento \
                INNER JOIN dbo.nom10002 t2 ON t2.idperiodo = t7.idperiodo \
                WHERE  t7.idconcepto=1 AND t2.idtipoperiodo={} AND t2.numeroperiodo={} AND t2.ejercicio={} \
                GROUP BY t3.descripcion  \
                ORDER BY total".format(dbase,tipo,self.semana,self.ejercicio))

            list = cursor.fetchall()
            #print(list)
            objDeptos=''
            listDeptos = []
            for item in list:
                if item[1]>5000:
                    objDeptos = {'depto':item[0],'total':format(round(item[1],2))}
                    listDeptos.append(objDeptos)

        return listDispersion,listDeptos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.empresa == '':
            self.semana, self.ejercicio = self.get_current_week_sql()
            context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Seleccione una empresa...'}
            return context_dict
        else:
            dispersion = self.my_custom_sql()[0]
            departamentos = self.my_custom_sql()[1]
            if len(dispersion)>0:
                context_dict = {'dispersion':dispersion,'departamentos':departamentos,"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'Exitoso!'}
                return context_dict
            else:
                context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'No se encontraron resultados con los parámetros utilizados, verifíquelos e intente nuevamente!'}
                return context_dict

        return context

    def post(self, request, **kwargs):

        if request.method == 'POST':
            my_data = request.POST
            acumul = request.POST.get('acumulado', False)
            tipo = request.POST.get('tipo', False)

            self.empresa = my_data['empresa']
            self.ejercicio = my_data['ejercicio']
            self.semana = my_data['semana']
            self.acumulado = acumul
            self.tipo_periodo = tipo

            context = self.get_context_data(**kwargs)

        return render(request,'nominas_app/dispersion.html',context)

class Factura(LoginRequiredMixin,TemplateView):
    template_name = 'nominas_app/factura.html'

    empresa = ''
    ejercicio = ''
    semana = ''
    acumulado = ''

    def get_current_week_sql(self):
        week = datetime.today().isocalendar()[1] -1
        year = datetime.today().isocalendar()[0]
        #print('YEAR: ',year,' WEEK: ', week)
        return week,year

    def my_custom_sql(self):

        if self.empresa == 'INNOVACIONES':
            connec = 'nominasInnova'
            listConceptos = [1,120,140,51,127,41,43,133,74,155,73,75,45,137,145,146,150,159,0]
            conceptos = '1,120,140,51,127,41,43,133,74,155,73,75,45,137,145,146,150,159,0'
        elif self.empresa == 'PRESTADORA':
            connec = 'nominasPrestadora'
            listConceptos = [1,120,155,30,132,154,146,145,74,167,73,75,134,143,144,158,0,168,0]
            conceptos = '1,120,155,30,132,154,146,145,74,167,73,75,134,143,144,158,0,168,0'
        elif self.empresa == 'PREFABRICADOS':
            connec = 'nominasPresol'
            listConceptos = [1,120,140,51,127,41,43,133,74,157,73,75,144,137,145,146,150,158,163]
            conceptos = '1,120,140,51,127,41,43,133,74,157,73,75,144,137,145,146,150,158,163'


        if self.acumulado:
            dbase = 8
        else:
            dbase = 7


        with connections[connec].cursor() as cursor:

            cursor.execute("SELECT t4.idconcepto, t4.descripcion AS concepto, SUM(tp.importetotal) AS total, t2.fechainicio, t2.fechafin \
                            FROM dbo.nom1000{} AS tp \
                            INNER JOIN dbo.nom10004 AS t4 ON t4.idconcepto = tp.idconcepto \
                            INNER JOIN dbo.nom10002 AS t2 ON t2.idperiodo = tp.idperiodo \
                            WHERE tp.idconcepto IN ({}) AND t2.numeroperiodo={} AND t2.ejercicio={} \
                            GROUP BY t4.idconcepto, t4.descripcion, t2.fechainicio, t2.fechafin".format(dbase,conceptos,self.semana,self.ejercicio))

            list = cursor.fetchall()

            objFactura = ''
            listFactura = []
            listTotales = []

            for item in list:
                date_ini = item[3].strftime('%d')
                date_fin = item[4].strftime('%d-%m-%Y')

                if item[0] == listConceptos[0]:
                    concepto = 'TOTAL NOMINA'
                    orden = 1
                    bloque = 'NOMINA'
                elif item[0] == listConceptos[1]:
                    concepto = 'FINIQUITOS'
                    orden = 2
                    bloque = 'NOMINA'
                elif item[0] == listConceptos[2]:
                    concepto = 'PRESTAMOS DE FONDO'
                    orden = 3
                    bloque = 'NOMINA2'
                elif item[0] == listConceptos[3]:
                    concepto = 'FONDO DE AHORRO EMPRESA'
                    orden = 4
                    bloque = 'FAHORRO'
                elif item[0] == listConceptos[4]:
                    concepto = '(+) FONDO DE AHORRO EMPLEADO'
                    orden = 5
                    bloque = 'FAHORRO'
                elif item[0] == listConceptos[5]:
                    concepto = '(+) ABONO A PRESTAMOS FONDO DE AHORRO'
                    orden = 6
                    bloque = 'FAHORRO2'
                elif item[0] == listConceptos[17]:
                    concepto = '(+) DESCUENTO A PRESTAMOS'
                    orden = 7
                    bloque = 'FAHORRO2'
                elif item[0] == listConceptos[6]:
                    concepto = item[1]
                    orden = 8
                    bloque = 'INFONAVIT'
                elif item[0] == listConceptos[7]:
                    concepto = item[1]
                    orden = 9
                    bloque = 'INFONAVIT'
                elif item[0] == listConceptos[8]:
                    concepto = item[1]
                    orden = 10
                    bloque = 'INFONAVIT'
                elif item[0] == listConceptos[9]:
                    concepto = item[1]
                    orden = 11
                    bloque = 'INFONAVIT'
                elif item[0] == listConceptos[10]:
                    concepto = item[1]
                    orden = 12
                    bloque = 'IMSS'
                elif item[0] == listConceptos[11]:
                    concepto = item[1]
                    orden = 13
                    bloque = 'IMSS'
                elif item[0] == listConceptos[12]:
                    concepto = item[1]
                    orden = 14
                    bloque = 'FONACOT'
                elif item[0] == listConceptos[13]:
                    concepto = item[1]
                    orden = 15
                    bloque = 'PROMOBIEN'
                elif item[0] == listConceptos[14]:
                    concepto = item[1]
                    orden = 16
                    bloque = 'PROMOBIEN'
                elif item[0] == listConceptos[15]:
                    concepto = item[1]
                    orden = 17
                    bloque = 'PROMOBIEN'
                elif item[0] == listConceptos[16]:
                    concepto = item[1]
                    orden = 18
                    bloque = 'PROMOBIEN'
                elif item[0] == listConceptos[18]:
                    concepto = item[1]
                    orden = 19
                    bloque = 'PROMOBIEN'

                objFactura = {'idconcepto':item[0],'concepto':concepto,'total':"{:,}".format(round(item[2],2)),
                    'fecha_inicio':date_ini,'fecha_fin':date_fin,'empresa':self.empresa,'ejercicio':self.ejercicio,
                    'periodo':self.semana,'bloque':bloque,'orden':orden,'importe':item[2]}

                listFactura.append(objFactura)

            sumNomina=0
            sumNomina2=0
            sumAhorro=0
            sumAhorro2=0
            sumInfonavit=0
            sumImss=0
            sumFonacot=0
            sumPromobien=0
            totalImss=0
            for item in listFactura:
                if 'Cesantia' in item['concepto']:
                    totalImss += item['importe']

                if item['bloque'] == 'NOMINA':
                    sumNomina += item['importe']
                elif item['bloque'] == 'NOMINA2':
                    sumNomina2 += item['importe']
                elif item['bloque'] == 'FAHORRO':
                    sumAhorro += item['importe']
                elif item['bloque'] == 'FAHORRO2':
                    sumAhorro2 += item['importe']
                elif item['bloque'] == 'INFONAVIT':
                    sumInfonavit += item['importe']
                elif item['bloque'] == 'IMSS':
                    sumImss += item['importe']
                elif item['bloque'] == 'FONACOT':
                    sumFonacot += item['importe']
                elif item['bloque'] == 'PROMOBIEN':
                    sumPromobien += item['importe']

            totalImss += sumImss
            objTotales = {'SubtotNomina':"{:,}".format(round(sumNomina,2)),
                        'SubtotNomina2':"{:,}".format(round(sumNomina2,2)),
                        'TotNomina':"{:,}".format(round(sumNomina + sumNomina2,2)),
                        'SubtotAhorro':"{:,}".format(round(sumAhorro,2)),
                        'SubtotAhorro2':"{:,}".format(round(sumAhorro2,2)),
                        'TotAhorro':"{:,}".format(round(sumAhorro + sumAhorro2,2)),
                        'TotInfonavit':"{:,}".format(round(sumInfonavit,2)),
                        'TotImss':"{:,}".format(round(sumImss,2)),
                        'TotFonacot':"{:,}".format(round(sumFonacot,2)),
                        'TotPromobien':"{:,}".format(round(sumPromobien,2)),
                        'TotalImss':"{:,}".format(round(totalImss,2))}

            listTotales.append(objTotales)

        return listFactura,listTotales

    def get_context_data(self, **kwargs):
        # print('ENTRO : get_context_data')
        context = super().get_context_data(**kwargs)
        if self.empresa == '':
            self.semana,self.ejercicio = self.get_current_week_sql()
            context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Seleccione una empresa...'}
            return context_dict
        else:
            factura,totales = self.my_custom_sql()
            if len(factura)>0:
                context_dict = {'factura':factura,'totales':totales,"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'Exitoso!'}
                return context_dict
            else:
                context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'No se encontraron resultados con los parámetros utilizados, verifíquelos e intente nuevamente!'}
                return context_dict

        return context

    def post(self, request, **kwargs):

        if request.method == 'POST':
            my_data = request.POST
            acumul = request.POST.get('acumulado', False)

            self.empresa = my_data['empresa']
            self.ejercicio = my_data['ejercicio']
            self.semana = my_data['semana']
            self.acumulado = acumul

            context = self.get_context_data(**kwargs)

        return render(request,'nominas_app/factura.html',context)

class FondoAhorro(LoginRequiredMixin,TemplateView):
    template_name = 'nominas_app/fondo_ahorro.html'

    empresa = ''
    ejercicio = ''
    semana = ''
    acumulado = ''

    def get_current_week_sql(self):
        week = datetime.today().isocalendar()[1] -1
        year = datetime.today().isocalendar()[0]
        #print('YEAR: ',year,' WEEK: ', week)
        return week,year

    def my_custom_sql(self):

        if self.empresa == 'INNOVACIONES':
            connec = 'nominasInnova'
            listConceptos = [30,127,130,132,139,140,41,159]
        elif self.empresa == 'PRESTADORA':
            connec = 'nominasPrestadora'
            listConceptos = [132,133,138,151,150,155,154,168]
        elif self.empresa == 'PREFABRICADOS':
            connec = 'nominasPresol'
            listConceptos = [30,51,130,132,139,140,41,158]


        if self.acumulado:
            dbase = 8
        else:
            dbase = 7


        with connections[connec].cursor() as cursor:

            cursor.execute("SELECT codigoempleado AS Numero,nombrelargo AS Empleado,descripcion AS Departamento,\
                ISNULL([{list[0]}],0) AS 'FAEmpresa',ISNULL([{list[1]}],0) AS 'FAEmpleado',ISNULL([{list[0]}],0)+ISNULL([{list[1]}],0) AS 'Total',ISNULL([{list[2]}],0) AS 'AcumEmpresa',\
                ISNULL([{list[3]}],0) AS 'AcumEmpleado',ISNULL([{list[4]}],0) AS 'TotalAhorrado',ISNULL([{list[5]}],0) AS 'PrestamoPeriodo',ISNULL([{list[6]}],0)+ISNULL([{list[7]}],0) AS 'DesctoPeriodo',\
                ISNULL(vecesaplicar,0) AS 'VecesAplicar',ISNULL(vecesaplicado,0) AS 'VecesAplicado',ISNULL(montolimite,0) AS 'MontoLimite',ISNULL(montoacumulado,0) AS 'MontoAcumulado',\
                fechainicio,fechafin\
                FROM(\
                SELECT t1.codigoempleado,t1.nombrelargo,t4.idconcepto,t3.descripcion,ISNULL(SUM(t7.importetotal),0)as total,\
                t17.vecesaplicar,t17.vecesaplicado,t17.montolimite,t17.montoacumulado,t2.fechainicio,t2.fechafin\
                FROM dbo.nom1000{db} t7\
                INNER JOIN dbo.nom10001 t1 ON t1.idempleado=t7.idempleado\
                INNER JOIN dbo.nom10002 t2 ON t2.idperiodo=t7.idperiodo\
                INNER JOIN dbo.nom10004 t4 ON t4.idconcepto = t7.idconcepto\
                INNER JOIN dbo.nom10003 t3 ON t3.iddepartamento = t1.iddepartamento\
                LEFT JOIN dbo.nom10017 t17 ON t17.idempleado = t7.idempleado AND t17.idconcepto = {list[6]} AND t17.estado=1\
                WHERE t2.numeroperiodo = {periodo} AND t2.ejercicio = {ejercicio} AND t7.idconcepto IN ({list[0]},{list[1]},{list[2]},{list[3]},{list[4]},{list[5]},{list[6]},{list[7]}) \
                GROUP BY t4.idconcepto,t1.nombrelargo,t1.codigoempleado,t3.descripcion,t17.vecesaplicar,t17.vecesaplicado,t17.montolimite,t17.montoacumulado,t2.fechainicio,t2.fechafin\
                )AS sourceTable\
                PIVOT (\
                SUM(total)\
                FOR idconcepto IN ([{list[0]}],[{list[1]}],[{list[2]}],[{list[3]}],[{list[4]}],[{list[5]}],[{list[6]}],[{list[7]}])\
                )AS PivotTable".format(db = dbase, periodo = self.semana, ejercicio = self.ejercicio, list = listConceptos))

            list = cursor.fetchall()

            objFondo=''
            listFondo = []
            for item in list:
                date_ini = item[15].strftime('%d')
                date_fin = item[16].strftime('%d-%m-%Y')

                objFondo = {'numero':item[0],'empleado':item[1],'departamento':item[2],'faempresa':"{:,}".format(round(item[3],2)),'faempleado':"{:,}".format(round(item[4],2)),'total':"{:,}".format(round(item[5],2)),
                            'acumempresa':"{:,}".format(round(item[6],2)),'acumempleado':"{:,}".format(round(item[7],2)),'totalahorrado':"{:,}".format(round(item[8],2)),'prestamoperiodo':"{:,}".format(round(item[9],2)),
                            'desctoperiodo':"{:,}".format(round(item[10],2)),'vecesaplicar':item[11],'vecesaplicado':item[12],'montolimite':"{:,}".format(round(item[13],2)),'montoacumulado':"{:,}".format(round(item[14],2)),
                            'fecha_inicio':date_ini,'fecha_fin':date_fin}
                listFondo.append(objFondo)

            cursor.execute("SELECT descripcion AS Departamento,\
                sum([{list[0]}]) AS 'FAEmpresa',sum([{list[1]}]) AS 'FAEmpleado',sum([{list[0]}]+[{list[1]}]) AS 'Total',sum([{list[2]}]) AS 'AcumEmpresa',\
                sum([{list[3]}]) AS 'AcumEmpleado',sum([{list[4]}]) AS 'TotalAhorrado',sum([{list[5]}]) AS 'PrestamoPeriodo',sum([{list[6]}]+[{list[7]}]) AS 'DesctoPeriodo'\
                FROM(\
                SELECT t1.codigoempleado,t1.nombrelargo,t4.idconcepto,t3.descripcion,ISNULL(SUM(t7.importetotal),0)as total,t17.vecesaplicar,t17.vecesaplicado,t17.montolimite,t17.montoacumulado\
                FROM dbo.nom1000{db} t7\
                INNER JOIN dbo.nom10001 t1 ON t1.idempleado=t7.idempleado\
                INNER JOIN dbo.nom10002 t2 ON t2.idperiodo=t7.idperiodo\
                INNER JOIN dbo.nom10004 t4 ON t4.idconcepto = t7.idconcepto\
                INNER JOIN dbo.nom10003 t3 ON t3.iddepartamento = t1.iddepartamento\
                LEFT JOIN dbo.nom10017 t17 ON t17.idempleado = t7.idempleado AND t17.idconcepto={list[6]} AND t17.estado=1\
                WHERE t2.numeroperiodo = {periodo} AND t2.ejercicio = {ejercicio} AND t7.idconcepto IN ({list[0]},{list[1]},{list[2]},{list[3]},{list[4]},{list[5]},{list[6]},{list[7]}) \
                GROUP BY t4.idconcepto,t1.nombrelargo,t1.codigoempleado,t3.descripcion,t17.vecesaplicar,t17.vecesaplicado,t17.montolimite,t17.montoacumulado\
                )AS sourceTable\
                PIVOT (\
                SUM(total)\
                FOR idconcepto IN ([{list[0]}],[{list[1]}],[{list[2]}],[{list[3]}],[{list[4]}],[{list[5]}],[{list[6]}],[{list[7]}])\
                )AS PivotTable\
                GROUP BY PivotTable.descripcion".format(db = dbase, periodo = self.semana, ejercicio = self.ejercicio, list = listConceptos))

            list = cursor.fetchall()
            #print(list)
            objDeptos=''
            listDeptos = []
            for item in list:
                objDeptos = {'depto':item[0],'faempresa':format(round(item[1],2)),'faempleadp':format(round(item[2],2)),
                'total':format(round(item[3],2)),'acumempresa':format(round(item[4],2)),'acumempleado':format(round(item[5],2)),
                'totalahorrado':format(round(item[6],2)),'prestamoperiodo':format(round(item[7],2)),'desctoperiodo':format(round(item[8],2))}
                listDeptos.append(objDeptos)

        return listFondo,listDeptos

    def get_context_data(self, **kwargs):
        # print('ENTRO : get_context_data')
        context = super().get_context_data(**kwargs)
        if self.empresa == '':
            self.semana,self.ejercicio = self.get_current_week_sql()
            context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Seleccione una empresa...'}
            return context_dict
        else:
            fondo,departamentos = self.my_custom_sql()
            if len(fondo)>0:
                context_dict = {'fondo':fondo,'departamentos':departamentos,"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'Exitoso!'}
                return context_dict
            else:
                context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'No se encontraron resultados con los parámetros utilizados, verifíquelos e intente nuevamente!'}
                return context_dict

        return context

    def post(self, request, **kwargs):

        if request.method == 'POST':
            my_data = request.POST
            acumul = request.POST.get('acumulado', False)
            tipo = request.POST.get('tipo', False)

            self.empresa = my_data['empresa']
            self.ejercicio = my_data['ejercicio']
            self.semana = my_data['semana']
            self.acumulado = acumul
            self.tipo_periodo = tipo

            context = self.get_context_data(**kwargs)

        return render(request,'nominas_app/fondo_ahorro.html',context)

class Acumulados(LoginRequiredMixin,TemplateView):
    template_name = 'nominas_app/acumulados.html'

    empresa = ''
    ejercicio = ''
    semana = ''
    acumulado = ''

    def get_current_week_sql(self):
        week = datetime.today().isocalendar()[1] -1
        year = datetime.today().isocalendar()[0]
        #print('YEAR: ',year,' WEEK: ', week)
        return week,year

    def my_custom_sql(self):

        if self.empresa == 'INNOVACIONES':
            connec = 'nominasInnova'
            listConceptos = [3,4,12,16,128,154,30,140,136,20,21,25,13,27,29,5,154,26,
            135,133,43,51,127,41,37,104,89,96,0,114,45,0,123,124,144,
            0,0,0,0,0,137,0,145,146,150,155,120,117,153,159,1,0]

            listPivot ="[3],[4],[12],[16],[128],[154],[30],[140],[136],[20],[21],[25],[13],[27],[29],[5],[26],[135],[133],[43],[51],[127],[41],[37],[104],[89],[96],[114],[45],[123],[124],[144],[137],[145],[146],[150],[155],[120],[117],[153],[159],[1],[0]"
        elif self.empresa == 'PRESTADORA':
            connec = 'nominasPrestadora'
            listConceptos = [3,4,12,128,127,157,30,155,152,20,21,25,13,27,29,5,157,0,
            149,145,146,132,133,154,37,104,89,96,153,41,0,134,136,147,
            148,135,159,160,161,162,0,143,144,158,0,167,120,117,140,168,1,0]

            listPivot = "[3],[4],[12],[128],[127],[157],[30],[155],[152],[20],[21],[25],[13],[27],[29],[5],[149],[145],[146],[132],[133],[154],[37],[104],[89],[96],[153],[41],[134],[136],[147],[148],[135],[159],[160],[161],[162],[143],[144],[158],[167],[120],[117],[140],[168],[1],[0]"
        elif self.empresa == 'PREFABRICADOS':
            connec = 'nominasPresol'
            listConceptos = [3,4,12,16,128,154,30,140,136,20,21,25,12,27,29,5,154,26,
            135,133,43,51,127,41,37,104,89,96,0,114,45,0,123,124,144,
            0,0,0,0,0,137,0,145,146,150,157,120,117,153,158,1,163]

            listPivot = "[3],[4],[12],[16],[128],[154],[30],[140],[136],[20],[21],[25],[27],[29],[5],[26],[135],[133],[43],[51],[127],[41],[37],[104],[89],[96],[114],[45],[123],[124],[144],[137],[0],[145],[146],[150],[157],[120],[117],[153],[158],[1],[163]"

        if self.acumulado:
            dbase = 8
        else:
            dbase = 7

        # pivot = []
        # for piv in listPivot:
        #     pivot.append('['+str(piv)+']')

        with connections[connec].cursor() as cursor:

            cursor.execute("SELECT codigoempleado AS Numero,nombrelargo AS Empleado,cuentapagoelectronico AS Cuenta, descripcion AS Departamento,\
                ISNULL([{list[0]}],0) AS 'Sueldo',ISNULL([{list[1]}],0) AS 'SeptimoDia',ISNULL([{list[2]}],0) AS 'DiaFestivo/Descanso',ISNULL([{list[3]}],0) AS 'BonoPuntualidad',ISNULL([{list[4]}],0) AS 'BonoAsistencia',\
                ISNULL([{list[5]}],0) AS 'ValesDespensa',ISNULL([{list[6]}],0) AS 'FAEmpresa',ISNULL([{list[7]}],0) AS 'PrestamoFA',ISNULL([{list[8]}],0) AS 'SubsidioIncapacidad',ISNULL([{list[9]}],0) AS 'VacacionesATiempo',\
                ISNULL([{list[10]}],0) AS 'PrimaVacaciones',ISNULL([{list[11]}],0) AS 'Aguinaldo',ISNULL([{list[12]}],0) AS 'Gratificacion',ISNULL([{list[13]}],0) AS 'Indemnizacion',ISNULL([{list[14]}],0) AS 'PrimaAntiguedad',\
                ISNULL([{list[15]}],0) AS 'HorasExtra',ISNULL([{list[16]}]+30,0) AS 'BonoSOL',ISNULL([{list[17]}],0) AS 'RepartoUtilidades',\
                ISNULL([{list[18]}],0) AS 'Alimentos',ISNULL([{list[19]}],0) AS 'InfonavitCF',ISNULL([{list[20]}],0) AS 'InfoanvitPorciento',ISNULL([{list[21]}],0) AS 'FondoAhorroEmpr',ISNULL([{list[22]}],0) AS 'FondoAhorroEmpl',\
                ISNULL([{list[23]}],0) AS 'DesctoFondoAhorro',ISNULL([{list[24]}],0) AS 'IMSS',ISNULL([{list[25]}],0) AS 'ISRArt42',ISNULL([{list[26]}],0) AS 'ISRsp',ISNULL([{list[27]}],0) AS 'SubsidioAlEmpleo',\
                ISNULL([{list[28]}],0) AS 'DesctosDiversos',ISNULL([{list[29]}],0) AS 'PrestFondoAhorro',ISNULL([{list[30]}],0) AS 'FONACOT',ISNULL([{list[31]}],0) AS 'FONACOT1',ISNULL([{list[32]}],0) AS 'FONACOT2',\
                ISNULL([{list[33]}],0) AS 'FONACOT3',ISNULL([{list[34]}],0) AS 'FONACOT4',ISNULL([{list[35]}],0) AS 'FONACOT5',ISNULL([{list[36]}],0) AS 'FONACOT6',ISNULL([{list[37]}],0) AS 'FONACOT7',\
                ISNULL([{list[38]}],0) AS 'FONACOT8',ISNULL([{list[39]}],0) AS 'FONACOT9',ISNULL([{list[40]}],0) AS 'PROMOBIEN',ISNULL([{list[41]}],0) AS 'PROMOBIEN1',ISNULL([{list[42]}],0) AS 'PROMOBIEN2',\
                ISNULL([{list[43]}],0) AS 'PROMOBIEN3',ISNULL([{list[44]}],0) AS 'PROMOBIEN4',ISNULL([{list[45]}],0) AS 'InfonavitImporte',ISNULL([{list[46]}],0) AS 'ISRFiniquito',ISNULL([{list[47]}],0) AS 'ISRRetener',\
                ISNULL([{list[48]}],0) AS 'ISRCompensar',ISNULL([{list[49]}],0) AS 'DesctoPrestamo',ISNULL([{list[50]}],0) AS 'BANCOS',ISNULL([{list[51]}],0) AS 'PROMOBIEN5',\
                fechainicio,fechafin\
                FROM(\
                SELECT t1.codigoempleado,t1.nombrelargo,t4.idconcepto,t3.descripcion,t1.cuentapagoelectronico,ISNULL(SUM(t7.importetotal),0)as total,t2.fechainicio,t2.fechafin\
                FROM dbo.nom1000{db} t7\
                INNER JOIN dbo.nom10001 t1 ON t1.idempleado=t7.idempleado\
                INNER JOIN dbo.nom10002 t2 ON t2.idperiodo=t7.idperiodo\
                INNER JOIN dbo.nom10004 t4 ON t4.idconcepto = t7.idconcepto\
                INNER JOIN dbo.nom10003 t3 ON t3.iddepartamento = t1.iddepartamento\
                WHERE t2.numeroperiodo = {periodo} AND t2.ejercicio = {ejercicio} \
                AND t7.idconcepto IN ({list[0]},{list[1]},{list[2]},{list[3]},{list[4]},{list[5]},{list[6]},{list[7]},{list[8]},{list[9]},{list[10]}, \
                                    {list[11]},{list[12]},{list[13]},{list[14]},{list[15]},{list[16]},{list[17]},{list[18]},{list[19]},{list[20]},{list[21]},\
                                    {list[22]},{list[23]},{list[24]},{list[25]},{list[26]},{list[27]},{list[28]},{list[29]},{list[30]},{list[31]},{list[32]},\
                                    {list[33]},{list[34]},{list[35]},{list[36]},{list[37]},{list[38]},{list[39]},{list[40]},{list[41]},{list[42]},{list[43]},\
                                    {list[44]},{list[45]},{list[46]},{list[47]},{list[48]},{list[49]},{list[50]},{list[51]})\
                GROUP BY t4.idconcepto,t1.nombrelargo,t1.codigoempleado,t3.descripcion,t1.cuentapagoelectronico,t2.fechainicio,t2.fechafin\
                )AS sourceTable\
                PIVOT (\
                SUM(total)\
                FOR idconcepto IN ({list_pivot})\
                )AS PivotTable".format(db = dbase, periodo = self.semana, ejercicio = self.ejercicio, list = listConceptos, list_pivot = listPivot))

            list = cursor.fetchall()

            objAcumulado=''
            listAcumulado = []
            for item in list:
                date_ini = item[56].strftime('%d')
                date_fin = item[57].strftime('%d-%m-%Y')

                total_percepciones = item[4] + item[5] + item[6] + item[7] + item[8] + item[9] + item[10] + item[11] + item[12] + item[13] +\
                item[14] + item[15] + item[16] + item[17] + item[18] + item[19] + item[21]

                total_deducciones = item[22] + item[23] + item[24] + item[25] + item[26] + item[27] + item[28] + item[29] + item[30] + item[31] + \
                item[32] + item[33] + item[34] + item[35] + item[36] + item[37] + item[38] + item[39] + item[40] + item[41] + item[42] + item[43] + \
                item[44] + item[45] + item[46] + item[47] + item[48] + item[49] + item[50] + item[51] + item[52] + item[55]

                objAcumulado = {'numero':item[0],'empleado':item[1],'cuenta':item[2],'departamento':item[3],
                            'sueldo':"{:,}".format(round(item[4],2)),'septimo_dia':"{:,}".format(round(item[5],2)),'dia_festivo_descanso':"{:,}".format(round(item[6],2)),
                            'bono_puntualidad':"{:,}".format(round(item[7],2)),'bono_asistencia':"{:,}".format(round(item[8],2)),'vales_despensa':"{:,}".format(round(item[9],2)),
                            'fa_empresa':"{:,}".format(round(item[10],2)),'prestamo_fa':"{:,}".format(round(item[11],2)),'subsidio_incapacidad':"{:,}".format(round(item[12],2)),
                            'vacaciones_a_tiempo':"{:,}".format(round(item[13],2)),'prima_vacaciones':"{:,}".format(round(item[14],2)),'aguinaldo':"{:,}".format(round(item[15],2)),
                            'gratificacion':"{:,}".format(round(item[16],2)),'indemnizacion':"{:,}".format(round(item[17],2)),'prima_antiguedad':"{:,}".format(round(item[18],2)),
                            'horas_extra':"{:,}".format(round(item[19],2)),'bono_sol':"{:,}".format(round(item[20],2)),'reparto_utilidades':"{:,}".format(round(item[21],2)),
                            'total_percepciones':"{:,}".format(round(total_percepciones,2)),
                            'alimentos':"{:,}".format(round(item[22],2)),'infonavit_cf':"{:,}".format(round(item[23],2)),'infonavit_porciento':"{:,}".format(round(item[24],2)),
                            'fondo_ahorro_empresa':"{:,}".format(round(item[25],2)),'fondo_ahorro_empleado':"{:,}".format(round(item[26],2)),'descto_fondo_ahorro':"{:,}".format(round(item[27],2)),
                            'imss':"{:,}".format(round(item[28],2)),'isr_art_42':"{:,}".format(round(item[29],2)),'isr_sp':"{:,}".format(round(item[30],2)),
                            'subsidio_al_empleo':"{:,}".format(round(item[31],2)),'desctos_diversos':"{:,}".format(round(item[32],2)),'prestamo_fondo_ahorro':"{:,}".format(round(item[33],2)),
                            'fonacot':"{:,}".format(round(item[34],2)),'fonacot1':"{:,}".format(round(item[35],2)),'fonacot2':"{:,}".format(round(item[36],2)),
                            'fonacot3':"{:,}".format(round(item[37],2)),'fonacot4':"{:,}".format(round(item[38],2)),'fonacot5':"{:,}".format(round(item[39],2)),
                            'fonacot6':"{:,}".format(round(item[40],2)),'fonacot7':"{:,}".format(round(item[41],2)),'fonacot8':"{:,}".format(round(item[42],2)),
                            'fonacot9':"{:,}".format(round(item[43],2)),'promobien':"{:,}".format(round(item[44],2)),'promobien1':"{:,}".format(round(item[45],2)),
                            'promobien2':"{:,}".format(round(item[46],2)),'promobien3':"{:,}".format(round(item[47],2)),'promobien4':"{:,}".format(round(item[48],2)),
                            'infonavit_importe':"{:,}".format(round(item[49],2)),'isr_finiquito':"{:,}".format(round(item[50],2)),'isr_retener':"{:,}".format(round(item[51],2)),
                            'isr_compensar':"{:,}".format(round(item[52],2)),'descto_prestamo':"{:,}".format(round(item[53],2)),'bancos':"{:,}".format(round(item[54],2)),
                            'promobien5':"{:,}".format(round(item[55],2)),'total_deducciones':"{:,}".format(round(total_deducciones,2)),'fecha_inicio':date_ini,'fecha_fin':date_fin}

                listAcumulado.append(objAcumulado)


        return listAcumulado

    def get_context_data(self, **kwargs):
        # print('ENTRO : get_context_data')
        context = super().get_context_data(**kwargs)
        if self.empresa == '':
            self.semana,self.ejercicio = self.get_current_week_sql()
            context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Seleccione una empresa...'}
            return context_dict
        else:
            acumulado = self.my_custom_sql()
            if len(acumulado)>0:
                context_dict = {'acumulado':acumulado,"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'Exitoso!'}
                return context_dict
            else:
                context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'No se encontraron resultados con los parámetros utilizados, verifíquelos e intente nuevamente!'}
                return context_dict

        return context

    def post(self, request, **kwargs):

        if request.method == 'POST':
            my_data = request.POST
            acumul = request.POST.get('acumulado', False)

            self.empresa = my_data['empresa']
            self.ejercicio = my_data['ejercicio']
            self.semana = my_data['semana']
            self.acumulado = acumul

            context = self.get_context_data(**kwargs)

        return render(request,'nominas_app/acumulados.html',context)

class Promobien(LoginRequiredMixin,TemplateView):
    template_name = 'nominas_app/promobien.html'

    empresa = ''
    ejercicio = ''
    semana = ''
    acumulado = ''

    def get_current_week_sql(self):
        week = datetime.today().isocalendar()[1] -1
        year = datetime.today().isocalendar()[0]
        #print('YEAR: ',year,' WEEK: ', week)
        return week,year

    def my_custom_sql(self):

        if self.empresa == 'INNOVACIONES':
            connec = 'nominasInnova'
            listConceptos = [137,145,146,150,0]
        elif self.empresa == 'PRESTADORA':
            connec = 'nominasPrestadora'
            listConceptos = [143,144,158,0,0]
        elif self.empresa == 'PREFABRICADOS':
            connec = 'nominasPresol'
            listConceptos = [137,145,146,150,163]


        if self.acumulado:
            dbase = 8
        else:
            dbase = 7


        with connections[connec].cursor() as cursor:

            cursor.execute("SELECT \
                            t4.descripcion, \
                            t1.codigoempleado, \
                            t17.numerocontrol, \
                            Convert(nvarchar(50),t1.nombre)+' '+ Convert(nvarchar(50),t1.apellidopaterno)+' '+ Convert(nvarchar(50),t1.apellidomaterno)AS 'Nombre', \
                            t3.descripcion AS departamento, \
                            Convert(nvarchar(50),t17.vecesaplicado) + '/' + Convert(nvarchar(50),t17.vecesaplicar) AS 'NumeroPago', \
                            t7.importetotal,t2.fechainicio,t2.fechafin \
                            FROM dbo.nom10007 t7 \
                            INNER JOIN dbo.nom10002 t2 ON t2.idperiodo = t7.idperiodo \
                            INNER JOIN dbo.nom10001 t1 ON t1.idempleado = t7.idempleado \
                            INNER JOIN dbo.nom10004 t4 ON t4.idconcepto = t7.idconcepto \
                            INNER JOIN dbo.nom10017 t17 ON t17.idmovtopermanente = t7.idmovtopermanente \
                            INNER JOIN dbo.nom10003 t3 ON t3.iddepartamento = t1.iddepartamento \
                            WHERE t2.numeroperiodo = {periodo} AND t2.ejercicio = {ejercicio} \
                            AND t7.importetotal>0 AND t7.idconcepto IN ({list[0]},{list[1]},{list[2]},{list[3]},{list[4]}) \
                            ORDER BY t1.nombre".format(db = dbase, periodo = self.semana, ejercicio = self.ejercicio, list = listConceptos))

            list = cursor.fetchall()

            objPromobien=''
            listPromobien = []
            for item in list:
                date_ini = item[7].strftime('%d')
                date_fin = item[8].strftime('%d-%m-%Y')

                objPromobien = {'concepto':item[0],'numero':item[1],'numero_control':item[2],'nombre':item[3],'departamento':item[4],'numero_pago':item[5],
                'total':"{:,}".format(round(item[6],2)),'fecha_inicio':date_ini,'fecha_fin':date_fin}
                listPromobien.append(objPromobien)

        return listPromobien

    def get_context_data(self, **kwargs):
        # print('ENTRO : get_context_data')
        context = super().get_context_data(**kwargs)
        if self.empresa == '':
            self.semana,self.ejercicio = self.get_current_week_sql()
            context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Seleccione una empresa...'}
            return context_dict
        else:
            promobien = self.my_custom_sql()
            if len(promobien)>0:
                context_dict = {'promobien':promobien,"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'Exitoso!'}
                return context_dict
            else:
                context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'No se encontraron resultados con los parámetros utilizados, verifíquelos e intente nuevamente!'}
                return context_dict

        return context

    def post(self, request, **kwargs):

        if request.method == 'POST':
            my_data = request.POST
            acumul = request.POST.get('acumulado', False)


            self.empresa = my_data['empresa']
            self.ejercicio = my_data['ejercicio']
            self.semana = my_data['semana']
            self.acumulado = acumul

            context = self.get_context_data(**kwargs)

        return render(request,'nominas_app/promobien.html',context)

class Asistencia(LoginRequiredMixin,TemplateView):
    template_name = 'nominas_app/asistencia.html'

    empresa = ''
    ejercicio = ''
    semana = ''

    def get_current_week_sql(self):
        week = datetime.today().isocalendar()[1] -1
        year = datetime.today().isocalendar()[0]
        #print('YEAR: ',year,' WEEK: ', week)
        return week,year

    def my_custom_sql(self):

        if self.empresa == 'INNOVACIONES':
            empresa = 23
            connec = 'nominasInnova'
        elif self.empresa == 'PRESTADORA':
            empresa = 19
            connec = 'nominasPrestadora'
        elif self.empresa == 'PREFABRICADOS':
            empresa = 28
            connec = 'nominasPresol'

        with connections[connec].cursor() as cursor:
            cursor.execute("SELECT \
            CONVERT(DATE,fechainicio,103)AS Fecha_inicio, \
            CONVERT(DATE,fechafin,103)AS Fecha_fin FROM dbo.nom10002 WHERE ejercicio={} AND numeroperiodo={}".format(self.ejercicio,self.semana))

            listFechas = cursor.fetchall()

            listDias = []
            #dia = listFechas[0][0].strftime("%d")
            fecha_inicio = listFechas[0][0]
            #print('fecha_inicio: ',fecha_inicio)
            for x in range(0,7):
                fecha = fecha_inicio + timedelta(days=x)
                listDias.append(fecha)

            #print('LISTDIAS: ',listDias)

        with connections['tempoControl'].cursor() as cursor:
            cursor.execute("SELECT \
                            idEmpleadoRegistrado,CodigoEmpleado,NombreLargo \
                            FROM dbo.tbEmpleadosRegistrados \
                            WHERE Status = 'AC' AND idEmpresaRegistrada = {}".format(empresa))

            listEmpleados = cursor.fetchall()
            listAsistencia = []
            for emp in listEmpleados:
                #print('EMPLEADO: ',emp)
            #with connections['tempoControl'].cursor() as cursor:

                cursor.execute("SELECT \
                                (SELECT CodigoEmpleado FROM tbEmpleadosRegistrados WHERE idEmpleadoRegistrado = {e[0]}) AS Codigo, \
                                (SELECT NombreLargo FROM tbEmpleadosRegistrados WHERE idEmpleadoRegistrado = {e[0]}) AS Empleado, \
                                CASE WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[0]}' AND idEmpleadoRegistrado={e[0]}) = 'ERT' THEN 'R' \
                                WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[0]}' AND idEmpleadoRegistrado={e[0]}) = 'EFT' THEN 'F' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[0]}' AND idEmpleadoRegistrado={e[0]})>=2 THEN 'A' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[0]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[0]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico='VAC' AND idEmpleadoRegistrado={e[0]})>=1 THEN 'V' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[0]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[0]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico IN('INC','MAT','ATRB','ATRY','ENFG') AND idEmpleadoRegistrado={e[0]})>=1 THEN 'I' ELSE 'F' \
                                END AS lunes,\
                                CASE WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[1]}' AND idEmpleadoRegistrado={e[0]}) = 'ERT' THEN 'R' \
                                WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[1]}' AND idEmpleadoRegistrado={e[0]}) = 'EFT' THEN 'F' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[1]}' AND idEmpleadoRegistrado={e[0]})>=2 THEN 'A' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[1]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[1]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico='VAC' AND idEmpleadoRegistrado={e[0]})>=1 THEN 'V' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[1]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[1]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico IN('INC','MAT','ATRB','ATRY','ENFG') AND idEmpleadoRegistrado={e[0]})>=1 THEN 'I' ELSE 'F' \
                                END AS martes,\
                                CASE WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[2]}' AND idEmpleadoRegistrado={e[0]}) = 'ERT' THEN 'R' \
                                WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[2]}' AND idEmpleadoRegistrado={e[0]}) = 'EFT' THEN 'F' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[2]}' AND idEmpleadoRegistrado={e[0]})>=2 THEN 'A' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[2]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[2]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico='VAC' AND idEmpleadoRegistrado={e[0]})>=1 THEN 'V' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[2]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[2]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico IN('INC','MAT','ATRB','ATRY','ENFG') AND idEmpleadoRegistrado={e[0]})>=1 THEN 'I' ELSE 'F' \
                                END AS miercoles,\
                                CASE WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[3]}' AND idEmpleadoRegistrado={e[0]}) = 'ERT' THEN 'R' \
                                WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[3]}' AND idEmpleadoRegistrado={e[0]}) = 'EFT' THEN 'F' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[3]}' AND idEmpleadoRegistrado={e[0]})>=2 THEN 'A' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[3]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[3]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico='VAC' AND idEmpleadoRegistrado={e[0]})>=1 THEN 'V' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[3]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[3]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico IN('INC','MAT','ATRB','ATRY','ENFG') AND idEmpleadoRegistrado={e[0]})>=1 THEN 'I' ELSE 'F' \
                                END AS jueves,\
                                CASE WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[4]}' AND idEmpleadoRegistrado={e[0]}) = 'ERT' THEN 'R' \
                                WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[4]}' AND idEmpleadoRegistrado={e[0]}) = 'EFT' THEN 'F' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[4]}' AND idEmpleadoRegistrado={e[0]})>=2 THEN 'A' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[4]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[4]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico='VAC' AND idEmpleadoRegistrado={e[0]})>=1 THEN 'V' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[4]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[4]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico IN('INC','MAT','ATRB','ATRY','ENFG') AND idEmpleadoRegistrado={e[0]})>=1 THEN 'I' ELSE 'F' \
                                END AS viernes,\
                                CASE WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[5]}' AND idEmpleadoRegistrado={e[0]}) = 'ERT' THEN 'R' \
                                WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[5]}' AND idEmpleadoRegistrado={e[0]}) = 'EFT' THEN 'F' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[5]}' AND idEmpleadoRegistrado={e[0]})>=2 THEN 'A' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[5]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[5]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico='VAC' AND idEmpleadoRegistrado={e[0]})>=1 THEN 'V' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[5]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[5]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico IN('INC','MAT','ATRB','ATRY','ENFG') AND idEmpleadoRegistrado={e[0]})>=1 THEN 'I' ELSE 'F' \
                                END AS sabado,\
                                CASE WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[6]}' AND idEmpleadoRegistrado={e[0]}) = 'ERT' THEN 'R' \
                                WHEN (SELECT TOP 1 CodigoEvento FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[6]}' AND idEmpleadoRegistrado={e[0]}) = 'EFT' THEN 'F' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbEventosRegistrados WHERE CONVERT(DATE,FechaHoraRegistrada,103)='{dias[6]}' AND idEmpleadoRegistrado={e[0]})>=2 THEN '1DL' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[6]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[6]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico='VAC' AND idEmpleadoRegistrado={e[0]})>=1 THEN 'V' \
                                WHEN (SELECT count(idEmpleadoRegistrado) FROM tbVacacionesIncapacidades WHERE '{dias[6]}'>=CONVERT(DATE,FechaInicio,103) AND '{dias[6]}'<=CONVERT(DATE,FechaFin,103) AND Mnemonico IN('INC','MAT','ATRB','ATRY','ENFG') AND idEmpleadoRegistrado={e[0]})>=1 THEN 'I' ELSE '' \
                                END AS domingo".format(dias = listDias, e = emp))

                list = cursor.fetchall()

                objAsistencia=''
                for item in list:
                    # date_ini = item[7].strftime('%d')
                    # date_fin = item[8].strftime('%d-%m-%Y') ,'fecha_inicio':date_ini,'fecha_fin':date_fin

                    objAsistencia = {'codigo':item[0],'nombre':item[1],'lunes':item[2],'martes':item[3],'miercoles':item[4],'jueves':item[5],'viernes':item[6],'sabado':item[7],'domingo':item[8]}
                    listAsistencia.append(objAsistencia)

        return listAsistencia,listDias

    def get_context_data(self, **kwargs):
        # print('ENTRO : get_context_data')
        context = super().get_context_data(**kwargs)
        if self.empresa == '':
            self.semana,self.ejercicio = self.get_current_week_sql()
            context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,"mensaje":'Seleccione una empresa...'}
            return context_dict
        else:
            asistencia,dias = self.my_custom_sql()
            if len(asistencia)>0:
                context_dict = {'asistencia':asistencia,'dias':dias,"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'Exitoso!'}
                return context_dict
            else:
                context_dict = {"ejercicio":self.ejercicio,"semana":self.semana,'empresa':self.empresa,"mensaje":'No se encontraron resultados con los parámetros utilizados, verifíquelos e intente nuevamente!'}
                return context_dict

        return context

    def post(self, request, **kwargs):

        if request.method == 'POST':
            my_data = request.POST

            self.empresa = my_data['empresa']
            self.ejercicio = my_data['ejercicio']
            self.semana = my_data['semana']

            context = self.get_context_data(**kwargs)

        return render(request,'nominas_app/asistencia.html',context)

def Empleado(request):
    codigo = request.GET.get('codigo')
    empresa = request.GET.get('empresa')
    semana = request.GET.get('semana')
    ejercicio = request.GET.get('ejercicio')

    comedor_id = Comedor.objects.filter(empresa=empresa,semana=semana,ejercicio=ejercicio)
    if comedor_id:
        detalle_comedor = ComedorDetalle.objects.filter(codigo_empleado=codigo,id_comedor=comedor_id[0])
        opcion = Opcion.objects.filter(id_comedor_detalle=detalle_comedor[0])
        mensaje = ''
        return render(request, 'nominas_app/detalle_empleado.html', {'empleado': detalle_comedor, 'opcion': opcion, 'mensaje': mensaje})
    else:
        mensaje = 'No se encontraron datos!'
        return render(request, 'nominas_app/detalle_empleado.html', {'empleado': '', 'opcion': '', 'mensaje': mensaje})
