from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User = get_user_model()
class UserLoginForm(forms.Form):
    username  = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username") 
        password = self.cleaned_data.get("password")
        if username and password: 
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("This user does not exists")
            
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")

            if not user.is_active:
                raise forms.ValidationError("This user is no longer active in the system")

        return super(UserLoginForm, self).clean(*args,**kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address') #---Overriding Default Email Input
    confirm_email = forms.EmailField(label='Confirm Email Address')
    password = forms.CharField(widget=forms.PasswordInput) #---Overriding Default Password Input
    
    class Meta:
        model=User
        fields = [
            'username',
            'email',
            'confirm_email',
            'password',
        ]
    
    def clean_confirm_email(self): #--clean_confirm_email is mentioned to take action and show validation errors on confirm_email tab
        email = self.cleaned_data.get('email')
        confirm_email = self.cleaned_data.get('confirm_email')
        if email != confirm_email:
            raise forms.ValidationError("Emails Do Not Match !")
        
        email_qs = User.objects.filter(email=email)
        print(email_qs)
        if email_qs.exists():
            raise forms.ValidationError("Emails has already been registered")
        return email