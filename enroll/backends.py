from django.contrib.auth.backends import BaseBackend
from .models import Company, Freelancer

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        user = None
        # Look up user by email in both models
        try:
            user = Company.objects.get(email=email)
        except Company.DoesNotExist:
            try:
                user = Freelancer.objects.get(email=email)
            except Freelancer.DoesNotExist:
                return None

        # Use model's check_password method to validate password
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Company.objects.get(pk=user_id)
        except Company.DoesNotExist:
            try:
                return Freelancer.objects.get(pk=user_id)
            except Freelancer.DoesNotExist:
                return None
