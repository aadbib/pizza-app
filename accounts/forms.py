# Importeer de nodige libraries om forms te maken en het account model te kunnen gebruiken
from django import forms
from orders.models import Account

# Userform die we bij het registreren van users kunnen gebruiken
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id':'inputUsername', 'class':'form-control', 'placeholder': 'Username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'inputPassword4', 'class':'form-control', 'placeholder':'Password'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id':'inputEmail4', 'class':'form-control', 'placeholder':'Username@domain.com'}), required=True)
    city = forms.CharField(widget=forms.TextInput(attrs={'id':'inputCity', 'class':'form-control', 'placeholder':'Amsterdam'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'inputFirst_name', 'class':'form-control', 'placeholder':'Joe'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id':'inputLast_name', 'class':'form-control', 'placeholder':'Rogan'}), required=True)

    # Meta class die de attributen mapt aan het Account-model (De extended User-model gedefinieerd in 'accounts')
    class Meta:
        model = Account
        fields = ('username', 'password', 'email', 'city', 'first_name', 'last_name')

# LoginForm die we kunnen gebruiken bij het inloggen van een user
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'username','class': 'form-control', 'placeholder': 'Username', 'name':'username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password','class':'form-control', 'placeholder':'Password', 'name':'password'}), required=True)