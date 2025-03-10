from django import forms
import re
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.forms import (
    AuthenticationForm, 
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from .models import CustomUser

class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder_mapping = {
            'username': 'Enter your username',
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'email': 'Enter your email address',
            'password1': 'Create password',
            'password2': 'Confirm password',
            'phone_number': '+8801000000000'
        }
        
        for field_name, field in self.fields.items():
            base_classes = 'px-2 py-2 w-full border-b-2 focus:border-blue-500 outline-none text-sm bg-white'
            field.widget.attrs.update({'class': base_classes})

            # Set placeholders based on field type and name
            if isinstance(field.widget, forms.PasswordInput):
                if field_name == 'password2':
                    field.widget.attrs['placeholder'] = placeholder_mapping.get(field_name, 'Confirm password')
                else:
                    field.widget.attrs['placeholder'] = placeholder_mapping.get(field_name, 'Enter password')
                    
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs['placeholder'] = placeholder_mapping.get(field_name, 'Enter your email')
                
            elif isinstance(field.widget, forms.TextInput):
                field.widget.attrs['placeholder'] = placeholder_mapping.get(
                    field_name, 
                    'Enter ' + field.label.lower() if field.label else 'Enter text'
                )
                if field_name == 'phone_number':
                    field.widget.attrs['pattern'] = r'^\+?1?\d{9,15}$'
                    
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                    'accept': 'image/*'
                })
                
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] += ' appearance-none'
                field.widget.attrs['placeholder'] = 'Select ' + field.label.lower()

class CustomRegistrationForm(StyleMixin, UserCreationForm):
    password1 = forms.CharField(
        label="Password",
    )
    password2 = forms.CharField(label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        help_texts = {'username': None}


    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []
        if len(password1) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password1):
            errors.append("Password must include at least one uppercase letter.")
        if not re.search(r'[a-z]', password1):
            errors.append("Password must include at least one lowercase letter.")
        if not re.search(r'\d', password1):
            errors.append("Password must include at least one number.")
        if not re.search(r'[@#$%^&+=]', password1):
            errors.append("Password must include at least one special character.")
        if errors:
            raise forms.ValidationError(errors)
        return password1

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class LoginForm(StyleMixin, AuthenticationForm):
    username = forms.CharField(label="Username", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class AssignRoleForm(StyleMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role",
        label="User Role"
    )

class CreateGroupForm(StyleMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Permissions'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        labels = {'name': 'Group Name'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].queryset = Permission.objects.select_related('content_type')

class CustomUserChangeForm(StyleMixin, UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture')
        widgets = {
            'profile_picture': forms.FileInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)
        self.fields['profile_picture'].required = False

class CustomPasswordChangeForm(StyleMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['old_password'].widget.attrs['placeholder'] = 'Current password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm new password'
        
        for field in self.fields.values():
            field.help_text = ''  
            field.widget.attrs.pop('aria-describedby', None)  

class CustomPasswordResetForm(StyleMixin, PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your registered email'})
    )

class CustomPasswordResetConfirmForm(StyleMixin, SetPasswordForm):
    pass
    