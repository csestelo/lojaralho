from django.forms import ModelForm, ValidationError
from django.forms.fields import CharField

from webapp.models import User as UserModel


class User(ModelForm):
    email_verify = CharField(required=True, max_length=254)
    password_verify = CharField(required=True, max_length=128)

    def clean_email(self):
        email = self.data['email']
        if email != self.data['email_verify']:
            raise ValidationError('Email e confirmação não bateram')
        return email

    def clean_password(self):
        password = self.data['password']
        if password != self.data['password_verify']:
            raise ValidationError('Senha e confirmação não bateram')
        return password

    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email', 'email_verify',
                  'password', 'password_verify', 'address', 'cellphone')
