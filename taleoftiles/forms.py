from django import forms
from datetime import datetime

from django.forms import ModelForm
from taleoftiles.models import Question, Shipping, ChartItem

from captcha.fields import ReCaptchaField


class QuestionForm(forms.Form):
    captcha = ReCaptchaField()

    class Meta:
        model = Question
        fields = ('text',)


class NewChartItemForm(ModelForm):
    
    class Meta:
        model = ChartItem
        fields = ('squared_meter',)

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for squared_meter in value:
            min_ammount(squared_meter)


class NewSamplerShipping(ModelForm):
    
    text =  forms.Textarea(attrs={'class': 'form-control'},)

    class Meta:
        model = Shipping
        fields = ('name','surname','address','address2','city','postcode','email','telephone','note')
        widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }
