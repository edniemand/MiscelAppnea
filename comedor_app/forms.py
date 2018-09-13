from django import forms
from comedor_app.models import Comedor,ComedorDetalle,Opcion

class ComedorForm(forms.ModelForm):

    class Meta():
        model = Comedor
        fields = "__all__"

class ComedorDetalleForm(forms.ModelForm):

    class Meta():
        model = ComedorDetalle
        fields = "__all__"

class OpcionForm(forms.ModelForm):

    class Meta():
        model = Opcion
        fields = ('empresa','ejercicio','semana','id_comedor','id_comedor_detalle','dia','comida')

        widgets = {
            'comida': forms.TextInput(attrs={'class':'editable medium-editor-textarea form-control','required': True}),
            'id_comedor': forms.Select(attrs={'class':'form-control','id':'id_comedor','name':'id_comedor','required': True}),
            'id_comedor_detalle': forms.Select(attrs={'class':'form-control','id':'id_comedor_detalle','name':'id_comedor_detalle','required': True}),
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['id_comedor'].queryset = Comedor.objects.all()
        self.fields['id_comedor_detalle'].queryset = ComedorDetalle.objects.none()

        if 'id_comedor' in self.data:
            try:
                id_comedor = int(self.data.get('id_comedor'))
                self.fields['id_comedor_detalle'].queryset = ComedorDetalle.objects.filter(id_comedor=id_comedor).order_by('codigo_empleado')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['id_comedor_detalle'].queryset = self.instance.id_comedor.id_comedor_detalle_set.order_by('codigo_empleado')
