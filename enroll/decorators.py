# enroll/decorators.py
from django.shortcuts import redirect

def company_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('company_id'):
            return view_func(request, *args, **kwargs)
        return redirect('company')  # Redirect to the company login page if not logged in
    return _wrapped_view
