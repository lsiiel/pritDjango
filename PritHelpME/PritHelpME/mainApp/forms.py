from django import forms

class AreaForm(forms.Form):
    length1 = forms.FloatField(label='Длина первого объекта (м)', min_value=0)
    width1 = forms.FloatField(label='Ширина первого объекта (м)', min_value=0)
    has_subtract_object = forms.BooleanField(label='Есть объект, площадь которого нужно вырезать', required=False)
    length2 = forms.FloatField(label='Длина второго объекта (м)', min_value=0, required=False)
    width2 = forms.FloatField(label='Ширина второго объекта (м)', min_value=0, required=False)
    material_length = forms.FloatField(label='Длина материала (см)', min_value=0)
    material_width = forms.FloatField(label='Ширина материала (см)', min_value=0)
