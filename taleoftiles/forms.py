from django import forms
from datetime import datetime

from django.forms import ModelForm, ModelChoiceField

from taleoftiles.models import Product, Tag

from captcha.fields import ReCaptchaField
from django.core.exceptions import NON_FIELD_ERRORS

class CustomProductModelForm(forms.ModelForm):
    
    series  = forms.ModelChoiceField(queryset = Tag.objects.filter(parent__slug='serie'), required = False)
    colours = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__slug='colour'), required = False)

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('tags',)

    def __init__(self, *args, **kwargs):
        serie       = kwargs['instance'].tags.filter(parent__slug='serie').first()
        colours     = kwargs['instance'].tags.filter(parent__slug='colour')

        super(CustomProductModelForm, self).__init__(*args, **kwargs)
        if serie:
            self.initial['series'] = serie.pk

        if colours:
            col_iv = []
            for colour in colours:
                col_iv.append(colour.pk)
            self.initial['colours'] = col_iv

    def save(self, commit=True):

        product = super(CustomProductModelForm, self).save(False)

        # ---- SERIE UPDATE -----
        series = product.tags.filter(parent__slug='serie') 

        for serie in series:
            product.tags.remove(serie.pk)

        if self.cleaned_data.get('series'):
            product.tags.add(self.cleaned_data.get('series')) 

        # ---- colors UPDATE -----

        colours = product.tags.filter(parent__slug='colour') 

        for color in colours:
            product.tags.remove(color.pk)

        if self.cleaned_data.get('colours'):
            for color in self.cleaned_data.get('colours'):
                    product.tags.add(color) 

        return super(CustomProductModelForm, self).save(True)

        # for color in colours:
        #     print("-----")
        #     print(color)
        #     if self.initial['colours']:
        #     self.initial['colours'] = color.pk

        # self.initial.setdefault('colours', default=None)
        # for color in colours:
        #     self.initial.get('colours').append(color.pk)
            

        #print (self.initial)


    # def clean(self):
    #     super().clean()
    #     print()
        # for form in self.forms:
        #     name = form.cleaned_data['name'].upper()
        #     form.cleaned_data['name'] = name
        #     # update the instance value.
        #     form.instance.name = name

    # def save(self, commit=True):
    #     print("-+   +-")
    #     print(product.tags.all())
    
    #     series = product.tags.filter(parent__slug='serie') 
    #     for serie in series:
    #         print("->   <-")
    #         print(serie)
        
    #         product.tags.remove(serie.pk)

    #     # if self.cleaned_data.get('series'):
    #     #     product.tags.add(self.cleaned_data.get('series')) 

    #     # if self.cleaned_data.get('colours'):
    #     #     for color in self.cleaned_data.get('colours'):
    #     #         product.tags.add(color) 
    #     print("--   --")                
    #     print(product.tags.all())
    #     product = super(CustomProductModelForm, self).save(commit)
    #     return product
