from django import forms
from datetime import datetime

from django.forms import ModelForm, ModelChoiceField
from taleoftiles.models import Question, Shipping, ChartItem, Format, Product

from captcha.fields import ReCaptchaField



# class QuestionForm(ModelForm):
#     captcha = ReCaptchaField()

#     class Meta:
#         model = Question
#         fields = ('name', 'surname', 'email',  'telephone','content' )
#         widgets = { 
#             'content' :  forms.Textarea(attrs={'class': 'border w-100 p-3 mt-3 mt-lg-4', 'placeholder':"Message *"}),
#             'name': forms.TextInput(attrs={'class': 'form-control','placeholder': "Name *"}),
#             'surname': forms.TextInput(attrs={'class': 'form-control','placeholder': "Surname "}),
#             'email': forms.TextInput(attrs={'class': 'form-control', 'type':"email" ,'placeholder': "Email *"}),
#             'telephone': forms.TextInput(attrs={'class': 'form-control','placeholder': "Telephone *"}),
#         }

# # menu = MenuModelChoiceField(queryset=Menu.objects.all())
# #     class Meta:      
# #         model = Item
# #         fields = '__all__'
# class NewChartItemForm(forms.Form):

#     quantity = forms.CharField()    
#     formats = forms.ModelMultipleChoiceField(queryset=None, class =  'form-control')    

#     def __init__(self, *args, **kwargs):
#         the_product = Product.objects.get(pk = kwargs.pop('product_id'))
#         the_coll = the_product.collection

#         super(NewChartItemForm, self).__init__(*args, **kwargs)
#         self.fields['formats'].queryset = Format.objects.filter(collection__pk=the_coll.id)
        
        
# class NewSamplerShipping(ModelForm):
    
#     text =  forms.Textarea(attrs={'class': 'form-control'},)

#     class Meta:
#         model = Shipping
#         fields = ('name','surname','address','address2','city','postcode','email','telephone','note')
#         widgets = { 
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'surname': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.TextInput(attrs={'class': 'form-control'}),
#             'telephone': forms.TextInput(attrs={'class': 'form-control'}),
#             'address': forms.TextInput(attrs={'class': 'form-control'}),
#             'address2': forms.TextInput(attrs={'class': 'form-control'}),
#             'city': forms.TextInput(attrs={'class': 'form-control'}),
#             'postcode': forms.TextInput(attrs={'class': 'form-control'}),
#             'note': forms.TextInput(attrs={'class': 'border p-3 w-100'}),
#         }
