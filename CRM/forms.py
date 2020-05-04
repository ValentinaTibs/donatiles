from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django.core.validators import validate_email
    

from django import forms

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User,Group


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


    # email = forms.CharField(label='Email', max_length=100,required=False)
    # telephone = forms.CharField(label='Telephone Number', max_length=100,required=False)

    
    # widgets = { 'username': forms.EmailField(label='Email', max_length=100,required=True),}

    # def validate(self, *args, **kwargs):
    #   print("ECCOCI")
    #   if not self.password2:
    #       self.password2 = self.password1
    #   return super().save(*args, **kwargs)

    # def function():
    #   pass
    # def save(self):
    #   print("GIAMMACO")
    #   print(self)
    #   print(self.cleaned_data)


class LoginForm(AuthenticationForm):
    pass