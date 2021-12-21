from django import forms

class NewChartItemCapsuleForm(forms.Form):
    
    product     = forms.HiddenInput(),
    chart       = forms.HiddenInput(),
    finish      = forms.HiddenInput(),
    quantity    = forms.IntegerField(required=True)
