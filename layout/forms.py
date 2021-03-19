from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist

from django import forms
from layout.models import  MailTemplate
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible


class ContactForm(forms.Form):

    email       = forms.CharField(max_length=200)
    request    	= forms.CharField(widget=forms.Textarea())
    captcha 	= ReCaptchaField()

    def clean(self):
        try:
            validate_email(self.cleaned_data.get('email'))
        except ValidationError as e:
            raise ValidationError(_('Invalid email'), code='no_email')
        return self.cleaned_data
