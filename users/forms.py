from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
   mobile_no = forms.CharField(widget = forms.TextInput(attrs={'required': 'true', 'class':'form-control form-control-sm', 'id' : 'mobileId'}))
   email = forms.EmailField(widget = forms.EmailInput(attrs={'required': 'true', 'class':'form-control form-control-sm', 'id' : 'emailId'}))
   password = forms.CharField(widget = forms.PasswordInput(attrs={'required': 'true', 'class':'form-control form-control-sm', 'id' : 'passwordId'}))
   password_repeat = forms.CharField(widget = forms.PasswordInput(attrs={'required': 'true', 'class':'form-control form-control-sm', 'id' : 'rePasswordId'}))

   class Meta():
       model = User
       fields = ('mobile_no','email','password','password_repeat')

