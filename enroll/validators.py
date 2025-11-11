# validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_unique_email(value):
    from .models import Freelancer, Company, AdminUser, Job_portal
    
    if Freelancer.objects.filter(email=value).exists():
        raise ValidationError(_('Email is already in use by Freelancer.'))
    
    if Company.objects.filter(email=value).exists():
        raise ValidationError(_('Email is already in use by Company.'))
    
    if AdminUser.objects.filter(email=value).exists():
        raise ValidationError(_('Email is already in use by Admin.'))
    
    if Job_portal.objects.filter(email=value).exists():
        raise ValidationError(_('Email is already in use by job_portal.'))
