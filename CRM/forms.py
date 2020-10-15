from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist

from django.utils.crypto import get_random_string

from django import forms

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User,Group
from taleoftiles.utils  import compute_single_price, compute_sm_price

from CRM.models import Shipping,ChartItem,Tag
from taleoftiles.models import Product
from layout.models import  MailTemplate

class ShippingForm(forms.ModelForm):

    class Meta:
        model = Shipping
        fields = ('fullname','country','city','CAP','shipping_address','telephone_num','email')
        
        widgets = { 
            'fullname'              :forms.TextInput(),
            'email'                 :forms.TextInput(),
            'city'                  :forms.TextInput(),
            'CAP'                   :forms.TextInput(),
            'shipping_address'      :forms.TextInput(),  
            'telephone_num'         :forms.TextInput()
        }

        def __init__(self, *args, **kwargs):
            super(ShippingForm, self).__init__(*args, **kwargs)
            

class NewChartItemForm(forms.ModelForm):

    class Meta:
        model = ChartItem
        fields = ('size', 'quantity' ,'product','chart','has_frido')
        widgets = { 
            'product'   :forms.HiddenInput(),
            'chart'     :forms.HiddenInput(),
            'size'      :forms.RadioSelect(),
            'has_frido' :forms.CheckboxInput(attrs={'checked' : True,}),
        }

    def __init__(self, *args, **kwargs):

        product = args[0].get('product')
        size = args[0].get('size')
        if product:
            prod_sizes = Tag.objects.filter(parent__parent__slug = 'format', prices__product__pk = product)
        else:
            raise forms.ValidationError(_('Wrong Product'), code='prod-error')

        super(NewChartItemForm, self).__init__(*args, **kwargs)
        self.fields['size'].required = True
        self.fields['size'].empty_label = None
        self.fields['size'].queryset = prod_sizes
        self.fields['quantity'].required = True   
                
    def clean(self):

        quantity    = self.cleaned_data.get('quantity')
        product     = self.cleaned_data.get('product')

        if quantity < product.min_ammount:
            raise forms.ValidationError(_('Not Enought'), code='min-ammount-error')
        else:
            return super(NewChartItemForm, self).clean()

        self._errors['starting_date'] = ['min-ammount-error']

class AddChartForm(NewChartItemForm):

    save_it = forms.BooleanField(required=False)
    finish  = forms.ModelChoiceField(queryset=Tag.objects.filter(parent__slug = 'finish'), empty_label=None)

    class Meta(NewChartItemForm.Meta):
        fields = NewChartItemForm.Meta.fields + ('save_it','finish')

    def __init__(self, *args, **kwargs):
        product = args[0].get('product')
        super(AddChartForm, self).__init__(*args, **kwargs)
        if product:
            prod_finishes =self.fields['finish'].queryset.filter( products__pk = product)
        else:
            raise forms.ValidationError(_('Wrong Product'), code='prod-error')

        self.fields['finish'].queryset = prod_finishes

    def clean(self):
        cleaned_data = super(AddChartForm, self).clean()

        
def create_first_pwd():
    return get_random_string(length=9)

class RegisterForm(UserCreationForm):


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        del self.fields['password1']

    def clean(self):
        self.cleaned_data["password1"] = create_first_pwd()

        super(RegisterForm, self).clean()
        username = self.cleaned_data.get('username')

        try:
            validate_email(username)
        except ValidationError as e:
            raise ValidationError(_('Invalid email'), code='no_email')

        #avoid duplicates
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Duplicated email'), code='duplicated-user-error')
        
        #send welcome email with pwd 
        MailTemplate().send_first_password(username,self.cleaned_data.get('password1'))
        
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