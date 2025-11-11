from django.shortcuts import redirect
from django.urls import reverse

class CompanyAuthenticationMiddleware:
    """Middleware to check for company authentication and prevent cached access to protected routes."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_routes = [
            reverse('view_company_contracts'),
            reverse('companydashboard'),
        ]
        if request.path in protected_routes and not request.session.get('company_id'):
            return redirect('company')  # Redirect to company login if not authenticated

        # Get the response and add cache headers if it's a protected route
        response = self.get_response(request)
        if request.path in protected_routes:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response

class FreelancerAuthenticationMiddleware:
    """Middleware to check for freelancer authentication and prevent cached access to protected routes."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_routes = [
            reverse('freelancerdashboard'),  # Replace with freelancer-specific routes
        ]
        if request.path in protected_routes and not request.session.get('freelancer_id'):
            return redirect('freelancer')  # Redirect to freelancer login if not authenticated

        response = self.get_response(request)
        if request.path in protected_routes:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response

class AdminAuthenticationMiddleware:
    """Middleware to check for admin authentication and prevent cached access to protected routes."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_routes = [
            reverse('adminpage'),  # Replace with admin-specific routes
        ]
        if request.path in protected_routes and not request.session.get('admin_id'):
            return redirect('admin')  # Redirect to admin login if not authenticated

        response = self.get_response(request)
        if request.path in protected_routes:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response
