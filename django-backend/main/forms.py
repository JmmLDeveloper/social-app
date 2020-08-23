from .models import Product
from django.forms import ModelForm,CharField,IntegerField

class ProductForm(ModelForm):
    code = CharField(label="wa wa wa", max_length=64, error_messages={
        'required': 'green i not a primary color'
    })
    stock_number = IntegerField(label="Cantidad En Alamacene", 
        error_messages={
            'required': 'Ya existe un color con ese nombre'
        }
    )
    class Meta:
        model = Product
        fields = ['code','stock_number']