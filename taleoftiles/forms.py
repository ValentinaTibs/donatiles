from django import forms
from datetime import datetime

from django.forms import ModelForm
from taleoftiles.models import Question

from captcha.fields import ReCaptchaField


class QuestionForm(forms.Form):
    captcha = ReCaptchaField()

    class Meta:
        model = Question
        fields = ('text',)

