from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist

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
        try:
            validate_email(username)
        except ValidationError as e:
            raise ValidationError(_('Invalid email'), code='no_email')

        #avoid duplicates
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Duplicated email'), code='duplicated')

        return self.cleaned_data    

    def save(self, commit=True):
        
        user = super(RegisterForm, self).save(commit=False)
        
        if commit:
            user.save()
            try: 
                client_group = Group.objects.get(name='Clients') 
            except ObjectDoesNotExist:
                return user
            client_group.user_set.add(user)

        return user    


class LoginForm(AuthenticationForm):
    pass