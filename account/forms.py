from django import forms
from .models import UserBase



from django import forms
from .models import UserBase

class RegistrationForm(forms.ModelForm):
    """
    A form for user registration that includes fields for username, email,
    and password. This form is based on the UserBase model and provides custom
    validation for the username and password fields.
    """

    user_name = forms.CharField(
        label='Enter Username', 
        min_length=4, 
        max_length=50, 
        help_text='Required'
    )
    """
    Field for entering the user's username. The username must be between 4 and 50 characters
    in length and is a required field. A help text is provided indicating it is a required field.
    """
    
    email = forms.EmailField(
        max_length=100, 
        help_text='Required', 
        error_messages={'required': 'Sorry, you will need an email'}
    )
    """
    Field for entering the user's email. The email must be valid and is required. 
    If the email is not provided, a custom error message will appear.
    """
    
    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput
    )
    """
    Field for entering the user's password. The password is rendered as a password input field,
    ensuring it is not visible as typed.
    """
    
    password2 = forms.CharField(
        label='Repeat password', 
        widget=forms.PasswordInput
    )
    """
    Field to confirm the user's password by repeating it. Like the 'password' field, it is a password input field.
    """
    
    class Meta:
        """
        Metadata for the form, specifying which model and fields are associated with the form.
        """
        model = UserBase
        fields = ('user_name', 'email',)
    
    def clean_user_name(self):
        """
        Validates the 'user_name' field to ensure that the username is unique. If the username
        already exists in the database, a validation error is raised.

        Returns:
            str: The validated (and lowercase) username.
        
        Raises:
            ValidationError: If the username already exists in the database.
        """
        user_name = self.cleaned_data['user_name'].lower()
        # Check if the username already exists
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name
