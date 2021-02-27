from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        """ Redefine Meta class to add email field."""
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        """ Add email before save the User model."""

        # Deactivate UserCreationForm save method.
        user = super().save(commit=False)
        # Get user email value from submitted form.
        user.email = self.cleaned_data.get('email')

        if commit:
            user.save()
        # Return UserCreationForm.
        return user
