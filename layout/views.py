from django.shortcuts import render,redirect

from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from layout.models      import Element, Mail, MailTemplate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



def support(request):  
    dyn_elements = Element.objects.filter(tag__parent__slug = 'support', public = True)
    return render(request, "support.html",{
        'layout_elems'  : dyn_elements,
        })

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email_data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=email_data))

            if associated_users.exists():
                for user in associated_users:
                    
                    caio = MailTemplate()
                    caio.caval_donato()

            # email_data = password_reset_form.cleaned_data['email']
            # associated_users = User.objects.filter(Q(email=email_data))
            # if associated_users.exists():
            #     for user in associated_users:
            #         # message = Mail()
            #         # message.to = To("tibaldo.valentina@gmail.com")
            #         # message.subject = Subject("Password Reset Requested", p=0)
            #         # message.from_email = Email("info@taleoftiles.com")
            #         # email_template_name = "password/password_reset_email.txt"
            #         # c = {
            #         #         "email":user.email,
            #         #         'domain':'127.0.0.1:8000',
            #         #         'site_name': 'Website',
            #         #         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            #         #         "user": user,
            #         #         'token': default_token_generator.make_token(user),
            #         #         'protocol': 'http',
            #         #         }
            #         # email = render_to_string(email_template_name, c)
            #         # message.html_content = HtmlContent(email)
            #         # message.content = render_to_string(email_template_name, c)
            #         # try:
            #         #     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            #         #     response = sg.send(message)
            #         #     print(response.status_code)
            #         #     print(response.body)
            #         #     print(response.headers)

            #         #     return redirect ("/password_reset/done/")
            #         # except Exception as e:
            #         #     print(str(e))
            #         #     print(str(e.body))    
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

