from django import forms
from .models import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"

class OrderForm(forms.ModelForm):


    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone', 'order_note'] 