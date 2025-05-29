from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

exclude_fields = [
    'password', 'id', 'is_staff', 'is_active',
    'date_joined', 'is_superuser', 'last_login'
]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [f.name for f in User._meta.fields if f.name not in exclude_fields] + ['password1', 'password2']