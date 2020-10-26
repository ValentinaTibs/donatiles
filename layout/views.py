from django.shortcuts import render,redirect

from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from layout.models      import Element, Mail, MailTemplate
from taleoftiles.models import Publication
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User



def support(request):  
    dyn_elements = Element.objects.filter(tag__parent__slug = 'support', public = True)
    return render(request, "support.html",{
        'layout_elems'  : dyn_elements,
        })

def termsandconds(request):  
    termsandconds = Publication.objects.get(slug = 'termsandconds')
    return render(request, "empty.html",{
        'publication'  : termsandconds,
        })


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email_data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=email_data)

            if associated_users.exists():
                for user in associated_users:

                    new_mail = MailTemplate()
                    new_mail.send_password_reset(user)
                    return redirect ("/password_reset/done/")
  
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

