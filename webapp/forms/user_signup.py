from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from django.forms.fields import CharField

from webapp.models import User as UserModel


class UserSignupForm(UserCreationForm):
    email_verify = CharField(required=True, max_length=254)

    def clean_email_verify(self):
        email = self.cleaned_data.get('email')
        if email != self.cleaned_data['email_verify']:
            raise ValidationError('Email e confirmação não bateram.')
        return email

    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email',
                  'email_verify', 'address', 'cellphone')
