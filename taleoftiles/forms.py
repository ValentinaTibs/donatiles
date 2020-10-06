from django import forms
from datetime import datetime

from django.forms import ModelForm, ModelChoiceField

from taleoftiles.models import Product, Tag

from captcha.fields import ReCaptchaField
from django.core.exceptions import NON_FIELD_ERRORS


class CustomProductModelForm(forms.ModelForm):
    
    series      = forms.ModelChoiceField(queryset = Tag.objects.filter(parent__slug='serie'), required = False)
    colours     = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__slug='colour'), required = False)
    formats     = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__parent__slug='format'), required = False)
    settings    = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__slug='setting'), required = False)
    styles      = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__slug='style'), required = False)
    effects     = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__slug='effect'), required = False)
    finishes    = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__slug='finish'), required = False)

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('tags',)

    def __init__(self, *args, **kwargs):
        if not kwargs.get('instance'):
            super(CustomProductModelForm, self).__init__(*args, **kwargs)
            return

        serie       = kwargs['instance'].tags.filter(parent__slug='serie').first()
        colours     = kwargs['instance'].tags.filter(parent__slug='colour')
        formats     = kwargs['instance'].tags.filter(parent__parent__slug='format')
        settings    = kwargs['instance'].tags.filter(parent__slug='setting')
        styles      = kwargs['instance'].tags.filter(parent__slug='style')
        effects     = kwargs['instance'].tags.filter(parent__slug='effect')
        finishes    = kwargs['instance'].tags.filter(parent__slug='finish')
        
        super(CustomProductModelForm, self).__init__(*args, **kwargs)
        if serie:
            self.initial['series'] = serie.pk

        if colours:
            col_iv = []
            for colour in colours:
                col_iv.append(colour.pk)
            self.initial['colours'] = col_iv

        if formats:
            format_iv = []
            for format_ in formats:
                format_iv.append(format_.pk)
            self.initial['formats'] = format_iv   
        
        if settings:
            settings_iv = []
            for setting in settings:
                settings_iv.append(setting.pk)
            self.initial['settings'] = settings_iv   

        if styles:
            styles_iv = []
            for style in styles:
                styles_iv.append(style.pk)
            self.initial['styles'] = styles_iv 

        if effects:
            effects_iv = []
            for effect in effects:
                effects_iv.append(effect.pk)
            self.initial['effects'] = effects_iv  

        if finishes:
            finishes_iv = []
            for finish in finishes:
                finishes_iv.append(finish.pk)
            self.initial['finishes'] = finishes_iv  
            
        return

    def save(self, commit=True):

        product = super(CustomProductModelForm, self).save(False)

        # ---- SERIE UPDATE -----
        if not product.pk:
            super(CustomProductModelForm, self).save(True)
            
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

        # ---- FORMATS UPDATE -----
        formats = product.tags.filter(parent__parent__slug='format') 
        for format_ in formats:
            product.tags.remove(format_.pk)
        if self.cleaned_data.get('formats'):
            for format_ in self.cleaned_data.get('formats'):
                    product.tags.add(format_) 

        # ---- SETTINGS UPDATE -----
        settings = product.tags.filter(parent__slug='setting') 
        for setting in settings:
            product.tags.remove(setting.pk)
        if self.cleaned_data.get('settings'):
            for setting in self.cleaned_data.get('settings'):
                    product.tags.add(setting)                                     

        # ---- STYLEs UPDATE -----
        styles = product.tags.filter(parent__slug='style') 
        for style in styles:
            product.tags.remove(style.pk)
        if self.cleaned_data.get('styles'):
            for style in self.cleaned_data.get('styles'):
                    product.tags.add(style) 

        # ---- EFFECT UPDATE -----
        effects = product.tags.filter(parent__slug='effect') 
    
        for effect in effects:
            product.tags.remove(effect.pk)
        if self.cleaned_data.get('effects'):
            for effect in self.cleaned_data.get('effects'):
                    product.tags.add(effect)
                    
        finishes = product.tags.filter(parent__slug='finish') 
    
        for finish in finishes:
            product.tags.remove(finish.pk)
        if self.cleaned_data.get('finishes'):
            for finish in self.cleaned_data.get('finishes'):
                    product.tags.add(finish)

        return super(CustomProductModelForm, self).save(True)

