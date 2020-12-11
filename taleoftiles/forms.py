from django import forms
from datetime import datetime

from django.forms import ModelForm, ModelChoiceField

from taleoftiles.models import Product, Tag

from captcha.fields import ReCaptchaField
from django.core.exceptions import NON_FIELD_ERRORS


class CustomProductModelForm(forms.ModelForm):
    
    series      = forms.ModelChoiceField(queryset = Tag.objects.filter(parent__slug='serie',public = True), required = False)
    samplable   = forms.BooleanField(required = False)
    in_home     = forms.BooleanField(required = False)
    colours     = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__slug='colour',public = True), required = False)
    formats     = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__parent__slug='format',public = True), required = False)
    settings    = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__slug='setting',public = True), required = False)
    styles      = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__slug='style',public = True), required = False)
    effects     = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__slug='effect',public = True), required = False)
    finishes    = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(parent__slug='finish',public = True), required = False)
    # in_product_edits   = forms.ModelMultipleChoiceField(queryset = Tag.objects.filter(in_product_edit=True, public = True), required = False)
    
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
        # in_product_edits = kwargs['instance'].tags.filter(in_product_edit=True)
        samplable   = kwargs['instance'].tags.filter(slug='samplable').first()
        in_home     = kwargs['instance'].tags.filter(slug='in_home').first()

        
        super(CustomProductModelForm, self).__init__(*args, **kwargs)
        if serie:
            self.initial['series'] = serie.pk

        if samplable:
            self.initial['samplable'] = True

        if in_home:
            self.initial['in_home'] = True

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

        # if in_product_edits:
        #     in_product_edits_iv = []
        #     for in_product_edit in in_product_edits:
        #         in_product_edits_iv.append(in_product_edit.pk)
        #     self.initial['in_product_edits'] = in_product_edits_iv      
            
        return

    def save(self, commit=True):

        product = super(CustomProductModelForm, self).save(False)
        if not product.pk:
            super(CustomProductModelForm, self).save(True)

        # ---- SERIE UPDATE -----            
        series = product.tags.filter(parent__slug='serie') 
        for serie in series:
            product.tags.remove(serie.pk)
        if self.cleaned_data.get('series'):
            product.tags.add(self.cleaned_data.get('series')) 

        # ---- SAMPLABLE UPDATE -----   
        samplables = product.tags.filter(slug='samplable') 
        samplable_tag = Tag.objects.get(slug='samplable')
        for samplable in samplables:
            product.tags.remove(samplable.pk)
        if self.cleaned_data.get('samplable'):
            product.tags.add(samplable_tag.pk)

        # ---- IN HOME UPDATE -----   
        in_homes = product.tags.filter(slug='in_home') 
        in_home_tag = Tag.objects.get(slug='in_home')
        for in_home in in_homes:
            product.tags.remove(in_home.pk)
        if self.cleaned_data.get('in_home'):
            product.tags.add(in_home_tag.pk)

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
            product.tags.remove(format_.parent)
        if self.cleaned_data.get('formats'):
            for format_ in self.cleaned_data.get('formats'):
                    product.tags.add(format_) 
                    product.tags.add(format_.parent) 

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

        # ---- FINSH UPDATE -----                    
                    
        finishes = product.tags.filter(parent__slug='finish') 
    
        for finish in finishes:
            product.tags.remove(finish.pk)
        if self.cleaned_data.get('finishes'):
            for finish in self.cleaned_data.get('finishes'):
                    product.tags.add(finish)

        # ---- product edito for catalogue -----                    
                    
        # in_product_edits = product.tags.filter(in_product_edit=True) 
    
        # for in_product_edit in in_product_edits:
        #     product.tags.remove(in_product_edit.pk)
        # if self.cleaned_data.get('in_product_edits'):
        #     for in_product_edit in self.cleaned_data.get('in_product_edits'):
        #             product.tags.add(in_product_edit)

        return super(CustomProductModelForm, self).save(True)

