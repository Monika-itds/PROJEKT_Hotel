from django import forms

class AvailabilityForm(forms.Form):
    ROOM_CATEGORIES = (
        ('STA', 'standard'),
        ('DEL', 'deluxe'),
        ('SUP', 'superior'),
        ('PRE', 'prezydencki'),
        ('KIN', 'królewski')
    )
    room_category = forms.ChoiceField(choices=ROOM_CATEGORIES, required=True)
    check_in = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])

class LoginForm(forms.Form):
    login = forms.CharField(label='Login')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)

def login_not_taken(login):
    if User.object.filter(username=login):
        raise ValidationError('Podany login jest już zajęty')

class UserRegistrationForm(forms.Form):
    login = forms.CharField(label='Login', validators=[login_not_taken])
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password_repeated = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)
    name = forms.CharField(label="Imię")
    surname = forms.CharField(label="Nazwisko")
    email = forms.EmailField(label="Email")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_repeated = cleaned_data.get('password_repeated')
        if password != password_repeated:
            raise forms.ValidationError('Hasła są różne!')
        return cleaned_data