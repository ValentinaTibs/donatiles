from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist

from django import forms

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User,Group

from CRM.models import Shipping,ChartItem,Tag
from taleoftiles.models import Product

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

class NewChartItemForm(forms.ModelForm):

    class Meta:
        model = ChartItem
        fields = ('size', 'quantity' ,'product','chart')
        widgets = { 
            'product'   :forms.HiddenInput(),
            'chart'     :forms.HiddenInput(),
            'size'      :forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):

        product = args[0]['product']

        if product:
            prod_sizes = Tag.objects.filter(parent__parent__slug = 'format', prices__product__pk = product)
            if not ('size' in args[0]):
                args[0]['size'] = prod_sizes.first()

        super(NewChartItemForm, self).__init__(*args, **kwargs)
        self.fields['size'].required = True
        self.fields['size'].empty_label = None
        self.fields['size'].queryset = prod_sizes
        self.fields['quantity'].required = True   


        
    def clean(self):
        print("+++")
        quantity    = self.cleaned_data.get('quantity')
        product     = self.cleaned_data.get('product')
        if quantity < product.min_ammount:
            raise forms.ValidationError(_('Not Enought'), code='min-ammount-error')

        else:
            return super(NewChartItemForm, self).clean()


        self._errors['starting_date'] = ['min-ammount-error']


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
            raise forms.ValidationError(_('Duplicated email'), code='duplicated-user-error')

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