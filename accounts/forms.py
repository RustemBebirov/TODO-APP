from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.db.models.fields import EmailField
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'u-form-group'})
    )
   
    password2 = forms.CharField(label='Confirm',widget=forms.PasswordInput(attrs=
    {'autocomplete':'new-password','class':'u-form-group'}))
    
    
    class Meta:
        model = CustomUser
        fields = ('email',)


    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError('Bu emailden istifade olunub')
        return email



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)



class LoginForm(forms.Form):
    email = forms.EmailField(max_length=127,widget=forms.EmailInput(attrs={
        'class':'u-form-group',
        'placeholder':'Email'
    }))
    password = forms.CharField(max_length=127,widget=forms.PasswordInput(attrs={
        'class':'u-form-group',
        'placeholder':'Password'
    }))