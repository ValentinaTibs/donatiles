from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django import forms

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User,Group

from CRM.models import Shipping

class ShippingForm(forms.ModelForm):

    class Meta:
        model = Shipping
        fields = ('fullname','country','city','CAP','shipping_address','telephone_num')
        
        def __init__(self, *args, **kwargs):
            super(ShippingForm, self).__init__(*args, **kwargs)
            self.fields['fullname']         .required = True
            self.fields['country']          .required = True
            self.fields['city']             .required = True
            self.fields['CAP']              .required = True
            self.fields['shipping_address'] .required = True
            self.fields['telephone_num']    .required = True

class RegisterForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        del self.fields['password2']

    def clean(self):
        super(RegisterForm, self).clean()
        username = self.cleaned_data.get('username')

        #ensure is a well formed email
        if not validate_email( username ):
            raise ValidationError(_('Invalid email'), code='no_email')

        #avoid duplicates
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Invalid value'), code='duplicated')

        return self.cleaned_data    

    def save(self, commit=True):
        
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.groups.set(Group.objects.get(name='Clients'))

        if commit:
            user.save()

        return user    


class LoginForm(AuthenticationForm):
    pass