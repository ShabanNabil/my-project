from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailAuthBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email')  # أخذ email من kwargs
        if not email:
            return None
        try:
            user = User.objects.get(Q(email__iexact=email))
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None