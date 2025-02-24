from django import forms
import re
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.forms import AuthenticationForm

class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add base classes to all widgets
            field.widget.attrs.update({
                'class': 'px-2 py-2 w-full border-b-2 focus:border-[#333] outline-none text-sm bg-white',
                'placeholder': f'Enter your {field.label.lower()}'
            })
            
            # Special handling for specific field types
            if isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs['placeholder'] = 'Enter your password'
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs['placeholder'] = 'Enter your email address'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'px-2 py-2 w-full border-b-2 focus:border-[#333] outline-none text-sm bg-white appearance-none'
                })


class CustomRegistrationForm(StyleMixin,forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'confirm_password']
        help_texts = {
            'username': None,
        }

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
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')
        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False  # Ensure user is inactive
        if commit:
            user.save()
        return user

class LoginForm(StyleMixin,AuthenticationForm):
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
        label='Assign Permissions'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']