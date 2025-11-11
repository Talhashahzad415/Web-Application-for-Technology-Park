from django.db.models import Q
from django.views.generic import ListView
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404, HttpResponse, HttpResponseNotAllowed
from .forms import AnnouncementForm, CompanyContractForm, FAQForm, FreelancerContractForm, FreelancerUpdateForm, RoomAvailabilityForm,RoomForm,CompanyRegistrationform,FreelancerRegistrationform, DeskForm, BookingForm, StudentRegistration, CompanyUpdateForm,RoomForm, DeskForm, CompanySignupForm,JobApplicationForm, FreelancerSignupForm,AdminSignupForm,JobSignupForm,JobLoginForm, CompanyLoginForm, FreelancerLoginForm,AdminLoginForm, AuthenticationForm , Company_PortfolioForm, Company_ComplaintForm, JobPostingForm, Freelancer_PortfolioForm, Freelancer_ComplaintForm, TrainingRoomForm
from .models import FAQ, Announcement, BookingRequest, Company_Complaint, Company_Portfolio, CompanyContract, CompanyContractResponse, Freelancer_Complaint, Freelancer_Portfolio, FreelancerContract, FreelancerContractResponse, JobApplication, TrainingBookingRequest, User,Message, Room,TrainingRoom,CompanyRegistration,FreelancerRegistration, Desk, Booking,  Company, Freelancer ,JobPosting, AdminUser, Job_portal
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.contrib.auth.hashers import make_password ,check_password
from django.contrib import messages
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
import logging

from enroll import models
logger = logging.getLogger(__name__)
from django.db.models import Q



def company_registration_view(request):
    if request.method == 'POST':
        form = CompanyRegistrationform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms')  # Redirect to a success page or wherever you want
    else:
        form = CompanyRegistrationform()

    return render(request, 'enroll/company_registration.html', {'form': form})
def freelancer_registration_view(request):
    if request.method == 'POST':
        form = FreelancerRegistrationform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('check_room_list')  # Redirect to a success page or wherever you want
    else:
        form = FreelancerRegistrationform()

    return render(request, 'enroll/freelancer_registration.html', {'form': form})

def show_complaint(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')
    
    freelancer_complaints = Freelancer_Complaint.objects.all()  # Fetch all rooms to display
    company_complaints = Company_Complaint.objects.all()  # Fetch all rooms to display
    context ={
        'freelancer_complaints': freelancer_complaints,
        'company_complaints': company_complaints,
        'admin_name': admin_name,
   }
    return render(request, 'enroll/show_complaints.html',context)

def show_profiles(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')
    freelancer_profile = Freelancer.objects.all()  # Fetch all rooms to display
    company_profile = Company.objects.all()  # Fetch all rooms to display
    context ={
        'freelancer_profile': freelancer_profile,
        'company_profile': company_profile,
        'admin_name': admin_name,
   }
    return render(request, 'enroll/show_profile.html',context)

def show_freelancer_application_view(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')    
    freelancer_application = FreelancerRegistration.objects.all()  # Fetch all rooms to display
    return render(request, 'enroll/freelancer_application.html', {'freelancer_application': freelancer_application, 'admin_name':admin_name})

def show_company_application_view(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin') 
    company_application = CompanyRegistration.objects.all()  # Fetch all rooms to display
    return render(request, 'enroll/company_application.html', {'company_application': company_application,'admin_name':admin_name})

def home_page(request):
    return render(request, 'enroll/home_page.html')
def view_edit(request):
    stud = User.objects.all()
    return render(request,'enroll/view-edit-rooms.html',{'stu':stud})

def index_page(request):
    return render(request, 'enroll/index.html')

def freelancer_page(request):
    return render(request, 'enroll/freelance.html')

def admin_dashboard(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    email = request.session.get('email')

    if not admin_id:
        return redirect('admin')
    
    context = {
        'admin_name': admin_name,
        'email': email,
    }
    return render(request, 'enroll/adminpage.html',context)

def company_page(request):
    return render(request, 'enroll/company.html')

def job_portal(request):
    return render(request, 'enroll/job_portal.html')

def company_dashboard(request):
    company_id = request.session.get('company_id')
    company = get_object_or_404(Company, id=company_id)
    company_name = request.session.get('company_name')
    announcements = Announcement.objects.order_by('-created_at')
    if not company_id:
        return redirect('company')  # Redirect to login if not authenticated

    # Get related job postings for this company
    job_postings = JobPosting.objects.filter(company=company)
    
    # Fetch available training rooms
    rooms = TrainingRoom.objects.all()

    # Pass the company name and data to the template
    context = {
        'company_name': company_name,
        'rooms': rooms,
        'job_postings': job_postings,
        'announcements': announcements,
    }
    return render(request, 'enroll/company_dashboard.html', context)


def freelancer_dashboard(request):
    freelancer_id = request.session.get('freelancer_id')
    freelancer_name = request.session.get('freelancer_name')
    email = request.session.get('email')
    announcements = Announcement.objects.order_by('-created_at')

    if not freelancer_id:
        return redirect('freelancer')  # Redirect to login if not authenticated
    
    desks = Desk.objects.all()
    context = {
        'freelancer_name': freelancer_name,
        'desks': desks,
        'email': email,
        'announcements': announcements,
         
    }

    return render(request, 'enroll/freelancer_dashboard.html', context)

#This Function will Add new Item and Show All Items
def add_show(request):
    if request.method == 'POST':
        fm = StudentRegistration(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'New Room Added Successfully!')
            return redirect('addandshow')
    else:
        fm = StudentRegistration()
    return render(request,'enroll/addandshow.html',{'form':fm})

def show_rooms(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')
    if not company_id:
        return redirect('company')
    
    if request.method == 'POST':
        fm = StudentRegistration(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('show_rooms')  # Redirect to the same page to see the updated list
    else:
        fm = StudentRegistration()

    rooms = User.objects.all()  # Fetch all rooms to display
    return render(request, 'enroll/show_rooms.html', {'form': fm, 'rooms': rooms,'company_name':company_name})

def show_rooms_admin(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')
    
    rooms = User.objects.all()  # Fetch all rooms to display
    return render(request, 'enroll/admin_show_rooms.html', {'rooms': rooms,'admin_name':admin_name})

def show_rooms_view(request):
    rooms = User.objects.all()  # Fetch all rooms to display
    return render(request, 'enroll/company_room_list.html', {'rooms': rooms})

def check_rooms_view(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')

    if not company_id:
        return redirect('company')  # Redirect to login if not authenticated

    rooms = User.objects.all()
    context = {
        'company_name': company_name,
        'rooms': rooms
    }
      # Fetch all rooms to display
    return render(request, 'enroll/company_rooms.html',context)

def add_show_jobs(request):
    jobs = JobPosting.objects.all()  # Fetch all jobs from the database
    
    # If jobs exist, display them with a "time ago" calculation
    job_list = []
    for job in jobs:
        time_diff = timezone.now() - job.timestamp  # Ensure the timestamp field is correct
        if time_diff.days > 0:
            time_ago = f"{time_diff.days} days ago"
        elif time_diff.seconds // 3600 > 0:
            time_ago = f"{time_diff.seconds // 3600} hours ago"
        elif time_diff.seconds // 60 > 0:
            time_ago = f"{time_diff.seconds // 60} minutes ago"
        else:
            time_ago = "just now"
        
        job_list.append({
            'job': job,
            'time_ago': time_ago
        })
    
    context = {
        'job_list': job_list,
    }
    
    return render(request, 'enroll/show_jobs.html', context)

#This Function will update/edit

def update_data(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        form = StudentRegistration(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('viewedit')
    else:
        form = StudentRegistration(instance=user)
    return render(request, 'enroll/updateroom.html', {'form': form, 'id': id})

# Delete function for User model
def delete_data(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        user.delete()
        return redirect('viewedit')
    return HttpResponse('Invalid request method', status=400)


def success(request):
    return render(request, 'enroll/success.html')

def company_signup(request):
    if request.method == 'POST':
        form = CompanySignupForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.password = make_password(form.cleaned_data['password'])
            company.save()
            # login(request, company)  
            return redirect('adminpage')
    else:
        form = CompanySignupForm()
    return render(request, 'enroll/company_signup.html', {'form': form})

def freelancer_signup(request):
    if request.method == 'POST':
        form = FreelancerSignupForm(request.POST)
        if form.is_valid():
            freelancer = form.save(commit=False)
            freelancer.password = make_password(form.cleaned_data['password'])
            freelancer.save()
            # login(request, freelancer)  # Ensure the login function works with your custom model
            return redirect('adminpage')
    else:
        form = FreelancerSignupForm()
    return render(request, 'enroll/freelancer_signup.html', {'form': form})

def job_portal_signup(request):
    if request.method == 'POST':
        form = JobSignupForm(request.POST)
        if form.is_valid():
            job_portal = form.save(commit=False)
            job_portal.password = make_password(form.cleaned_data['password'])
            job_portal.save()
            # login(request, freelancer)  # Ensure the login function works with your custom model
            return redirect('job_portal')
    else:
        form = JobSignupForm()
    return render(request, 'enroll/job_portal_signup.html', {'form': form})


def company_login_view(request):
    if request.method == 'POST':
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Fetch the company by email
            company = Company.objects.filter(email=email).first()
            
            if company and check_password(password, company.password):
                # Store company ID and name in the session
                request.session['company_id'] = company.id
                request.session['company_name'] = company.company_name  # Assuming it's company_name
                request.session['email'] = company.email 
                return redirect('companydashboard')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = CompanyLoginForm()

    return render(request, 'enroll/company.html', {'form': form})

def company_logout(request):
    # Clear the session data
    request.session.flush()  # This removes all session data
    # Redirect to the login page
    return redirect('company')


def freelancer_login_view(request):
    if request.method == 'POST':
        form = FreelancerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            freelancer = Freelancer.objects.filter(email=email).first()

            # Use check_password to compare hashed password
            if freelancer and check_password(password, freelancer.password):
                request.session['freelancer_id'] = freelancer.id
                request.session['freelancer_name'] = freelancer.freelancer_name
                request.session['email'] = freelancer.email  # Store email in the session
                    
                    # Debugging: check if email is set in session
                return redirect('freelancerdashboard')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = FreelancerLoginForm()

    return render(request, 'enroll/freelance.html', {'form': form})

def freelancer_logout(request):
    request.session.flush() 
    return redirect('freelancer')

def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if the admin user exists
            admin_user = AdminUser.objects.filter(email=email).first()
            
            if admin_user and admin_user.password==password:  # Use check_password
                # Login successful
                request.session['admin_id'] = admin_user.id  # Simple session-based login
                request.session['admin_name'] = admin_user.admin_name
                request.session['email'] = admin_user.email
                return redirect('adminpage')
            else:
                form.add_error(None, 'Invalid email or password.')  # Adding a non-field error to the form
    else:
        form = AdminLoginForm()

    return render(request, 'enroll/home_page.html', {'form': form})

def admin_logout(request):
    request.session.flush() 
    return redirect('admin')

def job_login_view(request):
    if request.method == 'POST':
        form = JobLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if the admin user exists
            jobportal = Job_portal.objects.filter(email=email).first()
            
            if jobportal and check_password(password, jobportal.password):  # Use check_password
                # Login successful
                request.session['job_id'] = jobportal.id  # Simple session-based login
                return redirect('show_jobs')
            else:
                form.add_error(None, 'Invalid email or password.')  # Adding a non-field error to the form
    else:
        form = JobLoginForm()
    return render(request, 'enroll/job_portal.html', {'form': form})

def job_posting_view(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')

    if not company_id:
        return redirect('company')
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            # Fetch the company_id from the session
            company_id = request.session.get('company_id')
            if not company_id:
                return redirect('company')  # Handle unauthorized access

            # Assuming you have a way to get the job_portal
            job_portal = Job_portal.objects.first()  # Replace this with your logic to get the correct Job_portal

            # Create the job posting with the company and job portal
            job_posting = form.save(commit=False)
            job_posting.company_id = company_id  # Set the company_id from session
            job_posting.job_portal = job_portal  # Set the job portal (ensure job_portal is valid)
            job_posting.save()
            return redirect('companydashboard')  # Redirect to a success page
    else:
        form = JobPostingForm()
    return render(request, 'enroll/jobcreation_form.html', {'form': form,'company_name' : company_name})


def apply_for_job(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id)

    if request.method == 'POST':
        
        job_portal_id = request.session.get('job_id')  # Assuming job_id is stored in the session
        job_portal_instance = Job_portal.objects.get(id=job_portal_id)
        freelancer_id = request.session.get('freelancer_id')  # Assuming freelancer_id is stored in the session
        freelancer_instance = Freelancer.objects.get(id=freelancer_id)
        
        
        job_application = JobApplication(
            job=job_posting,
            applicant=job_portal_instance or freelancer_instance,  # Directly use the Job_portal instance
            cover_letter=request.POST.get('cover_letter'),
            resume=request.FILES.get('resume'),  # Handle resume file
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            phone_number = request.POST.get('phone_number'),
            education_level = request.POST.get('education_level'),
            work_experience = request.POST.get('work_experience'),
        )
        job_application.save()
        return redirect('show_jobs')

    # If it's a GET request, render the application form
    return render(request, 'enroll/apply_for_job.html', {'job': job_posting})

# View for company to see applications for their jobs
def view_applications(request, job_id):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')

    if not company_id:
        return redirect('company')
    # Retrieve the JobPosting instance using the job_id
    job_posting = get_object_or_404(JobPosting, id=job_id)
    
    # Retrieve all applications related to this job posting
    applications = job_posting.applications.all()  # Use related_name to access related applications

    return render(request, 'enroll/view_applications.html', {
        'job': job_posting,  # Pass the job posting instance
        'applications': applications,  # Pass the applications queryset
        'company_name' : company_name,
    })
def company_applications(request, job_posting_id):
    # Get the job posting
    job_posting = get_object_or_404(JobPosting, id=job_posting_id)

    # Ensure the user is the company that created this job posting
    if request.user.jobportal != job_posting.company:
        return render(request, 'not_authorized.html')  # Render a page indicating unauthorized access

    # Retrieve all applications for this job posting
    applications = job_posting.applications.all()

    return render(request, 'company_applications.html', {'job_posting': job_posting, 'applications': applications})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def portfolio_view(request):
    # Get the logged-in company ID and name from the session
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')

    if not company_id:
        return redirect('company')  # Redirect to company login page if not authenticated

    # Get the logged-in company instance
    company = get_object_or_404(Company, id=company_id)

    # Check if a portfolio already exists for the company
    try:
        portfolio = Company_Portfolio.objects.get(company=company)
        # If portfolio exists, display the portfolio details
        return render(request, 'enroll/portfolio_detail.html', {
            'portfolio': portfolio,
            'company_name': company_name,
        })
    except Company_Portfolio.DoesNotExist:
        # Allow portfolio creation if it does not exist
        if request.method == 'POST':
            form = Company_PortfolioForm(request.POST, request.FILES)  # Include request.FILES for file uploads
            if form.is_valid():
                portfolio = form.save(commit=False)  # Create the portfolio object but don’t save yet
                portfolio.company = company  # Associate the portfolio with the logged-in company
                portfolio.save()  # Save the portfolio to the database
                messages.success(request, '🎉 Your portfolio has been created successfully!')
                return redirect('portfolio')  # Redirect to view the newly created portfolio
        else:
            form = Company_PortfolioForm()

        # Render the portfolio creation form
        return render(request, 'enroll/portfolio.html', {
            'form': form,
            'company_name': company_name,
        })



def complaint_view(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')
    email = request.session.get('email')

    if not company_id:
        return redirect('company')
    
    if request.method == 'POST':
        form = Company_ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '🎉 Your complaint has been successfully submitted!')
            return redirect('complaint')
          
    else:
        form = Company_ComplaintForm()

    context = {
        'form': form,
        'company_name': company_name, # Add company name to context for display in template
        'email': email,  
    }     

    return render(request, 'enroll/complaint.html', context)


def freelancer_portfolio_view(request):
    freelancer_id = request.session.get('freelancer_id')
    freelancer_name = request.session.get('freelancer_name')

    # Redirect to login if the freelancer is not authenticated
    if not freelancer_id:
        return redirect('freelancer')  # Replace 'freelancer' with your login URL name

    try:
        # Check if a portfolio exists for the freelancer
        portfolio = Freelancer_Portfolio.objects.get(freelancer__id=freelancer_id)
        # If portfolio exists, render the detail page
        return render(request, 'enroll/freelancer_portfolio_detail.html', {
            'portfolio': portfolio,
            'freelancer_name': freelancer_name,
        })
    except Freelancer_Portfolio.DoesNotExist:
        # If portfolio does not exist, allow the freelancer to create one
        if request.method == 'POST':
            form = Freelancer_PortfolioForm(request.POST, request.FILES)  # Include request.FILES for file uploads
            if form.is_valid():
                portfolio = form.save(commit=False)
                portfolio.freelancer_id = freelancer_id  # Associate the portfolio with the freelancer
                portfolio.save()
                messages.success(request, '🎉 Your portfolio has been created successfully!')
                return redirect('freelancer_portfolio')  # Redirect to display the newly created portfolio
        else:
            form = Freelancer_PortfolioForm()

        # Render the form to create a portfolio
        return render(request, 'enroll/freelancer_portfolio.html', {
            'form': form,
            'freelancer_name': freelancer_name,
        })
                                            
def freelancer_complaint_view(request):
    freelancer_id = request.session.get('freelancer_id')
    freelancer_name = request.session.get('freelancer_name')
    email = request.session.get('email')

    if not freelancer_id:
        return redirect('freelancer')  # Redirect to login if not authenticated

    if request.method == 'POST':
        form = Freelancer_ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '🎉 Your complaint has been successfully submitted!')
            return redirect('freelancer_complaint')  # Redirect to a success page or wherever you want
    else:
        # Pre-fill the form with freelancer's name and email
        form = Freelancer_ComplaintForm(initial={'name': freelancer_name, 'email': email})

    context = {
        'form': form,
        'freelancer_name': freelancer_name,
        'email': email,
    }

    return render(request, 'enroll/freelancer_complaint.html', context)

def company_edit_profile_view(request):
    company_id = request.session.get('company_id')
    
    if not company_id:
        return redirect('company')  # Redirect to login if not logged in

    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        messages.error(request, "Company not found.")
        return redirect('companydashboard')  # Redirect if company not found

    if request.method == 'POST':
        form = CompanyUpdateForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            
            # Check if password was changed
            new_password = form.cleaned_data.get('password')
            if new_password:
                company.password = make_password(new_password)  # Hash the new password
            
            company.save()  # Save the updated company details with hashed password
            messages.success(request, "Profile updated successfully!")
            return redirect('company_edit_profile')  # Redirect to the profile page after update
        else:
            messages.error(request, "There was an error in your form.")
    else:
        form = CompanyUpdateForm(instance=company)  # Pre-fill form with company data

    return render(request, 'enroll/edit_profile_company.html', {'form': form})

def freelancer_edit_profile_view(request):
    # Fetch the freelancer from the session
    freelancer_id = request.session.get('freelancer_id')
    freelancer = get_object_or_404(Freelancer, id=freelancer_id)

    if request.method == 'POST':
        form = FreelancerUpdateForm(request.POST, instance=freelancer)
        if form.is_valid():
             freelancer=form.save(commit=False)
             new_password = form.cleaned_data.get('password')
             if new_password:
                freelancer.password = make_password(new_password)
                freelancer.save()
             messages.success(request, "Profile updated successfully!")
             return redirect('freelancer_edit_profile')  # Redirect to the freelancer dashboard after updating
        else:
            if not form.errors:
                form.add_error(None, 'There was an error in your form.')
    else:
        form = FreelancerUpdateForm(instance=freelancer)

    return render(request, 'enroll/freelancer_edit_profile.html', {'form': form})


def create_room_view(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')   
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_desk')  # Redirect to list of rooms after creation
    else:
        form = RoomForm()
    return render(request, 'enroll/create_room.html', {'form': form,'admin_name':admin_name})

# Create Desk
def create_desk_view(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')   
    if request.method == 'POST':
        form = DeskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Desk Created Successfully!")
            return redirect('create_desk')  # Redirect to the list of rooms
    else:
        form = DeskForm()
    return render(request, 'enroll/create_desk.html', {'form': form,'admin_name': admin_name})

# Book a Desk
def book_desk_view(request):
    freelancer_id = request.session.get('freelancer_id')
    freelancer_name = request.session.get('freelancer_name')

    if not freelancer_id:
        return redirect('freelancer')  # Redirect to login if not authenticated

    freelancer = Freelancer.objects.get(id=freelancer_id)
    rooms = Room.objects.all()
    desks = Desk.objects.all()

    if request.method == 'POST':
        room_id = request.POST.get('room')
        desk_id = request.POST.get('desk')
        time_slot = request.POST.get('time_slot')
        date = request.POST.get('date')

        if not room_id or not desk_id or not time_slot or not date:
            messages.error(request, "All fields are required.")
            return redirect('book_desk')  # Redirect to the same page

        desk = get_object_or_404(Desk, id=desk_id)

        # Check if a booking has already been accepted for this desk and time slot
        accepted_booking = Booking.objects.filter(desk=desk, time_slot=time_slot, status='booked').exists()

        if accepted_booking:
            # Show an error message if the desk has already been accepted for the selected time slot
            messages.error(request, "This desk is already booked and cannot be reserved.")
            return redirect('book_desk')  # Redirect back to the booking page

        # Create the booking with status 'pending'
        booking = Booking(desk=desk, freelancer=freelancer, time_slot=time_slot, date=date, status='Pending')
        booking.save()

        messages.success(request, "Your booking request send successfully! Waiting for admin approval.")
        return redirect('book_desk')  # Redirect after successful booking

    context = {
        'rooms': rooms,
        'desks': desks,
        'freelancer_name': freelancer_name,
    }
    return render(request, 'enroll/book_desk.html', context)

def room_list_view(request):
    freelancer_id = request.session.get('freelancer_id')
    freelancer_name = request.session.get('freelancer_name')
    if not freelancer_id:
        return redirect('freelancer')
    form = RoomAvailabilityForm(request.POST or None)
    availability = []
    no_desk_message = ""

    if form.is_valid():
        availability = form.get_availability()

        # Check if the selected room has desks
        room = form.cleaned_data.get('room')
        if room and not room.desks.exists():
            no_desk_message = "This room does not have any desks"  # Assign error message

    context = {
        'freelancer_name': freelancer_name,
        'form': form,
        'availability': availability,
        'no_desk_message': no_desk_message,  # Add the message to the context
    }
    return render(request, 'enroll/room_list.html', context)

def admin_room_list_view(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')
    form = RoomAvailabilityForm(request.POST or None)
    availability = []
    no_desk_message = ""

    if form.is_valid():
        availability = form.get_availability()

        # Check if the selected room has desks
        room = form.cleaned_data.get('room')
        if room and not room.desks.exists():
            no_desk_message = "This room does not have any desks"  # Assign error message

    context = {
        'admin_name': admin_name,
        'form': form,
        'availability': availability,
        'no_desk_message': no_desk_message,  # Add the message to the context
    }
    return render(request, 'enroll/admin_room_list.html', context)

def check_room_list_view(request):
    # Initialize the form for room availability
    form = RoomAvailabilityForm(request.POST or None)
    availability = []

    # Process the form if it has been submitted
    if form.is_valid():
        availability = form.get_availability()  # Get room availability

    context = {
        'form': form,
        'availability': availability,
    }

    return render(request, 'enroll/check_rooms.html', context)

def admin_booking_management(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')
    bookings = Booking.objects.filter(status='Pending')  # Get all pending bookings

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')  # Accept or Reject

        booking = get_object_or_404(Booking, id=booking_id)

        if action == 'accept':
            booking.status = 'booked'
            booking.save()
            messages.success(request, f"Booking for ({booking.desk} at time slot {booking.time_slot}) has been approved and other requests for this desk at that time slot have been removed.")

            # Automatically remove other pending requests for the same desk and time slot
            Booking.objects.filter(desk=booking.desk, time_slot=booking.time_slot, status='Pending').exclude(id=booking.id).delete()
        elif action == 'reject':
            booking.status = 'available'  # Mark the desk available if rejected
            booking.save()
            messages.info(request, f"Booking request for ({booking.desk} at time slot {booking.time_slot}) has been rejected.")

        return redirect('admin_requests')  # Redirect after processing the request

    context = {
        'bookings': bookings,
        'admin_name': admin_name,
    }
    return render(request, 'enroll/admin_requests.html', context)


def book_room(request, room_id):
    # Assuming company_id is stored in the session when the company logs in
    company_id = request.session.get('company_id')

    if not company_id:
        return redirect('company')

    company = get_object_or_404(Company, id=company_id)
    room = get_object_or_404(User, id=room_id)  # Use User here to get the room

    if request.method == 'POST':
        # Create a booking request
        booking_request = BookingRequest.objects.create(
            company=company,  # Link the booking request to the company
            room=room,  # Link the booking request to the room
            status='pending'  # Set the initial status of the booking request
        )
        
        messages.success(request, "Room booking request send successfully! Waiting for admin approval.")
        return redirect('show_rooms')
    
    return render(request, 'enroll/show_rooms.html', {'room': room}) 


def manage_booking_requests(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')

    if not admin_id:
        return redirect('admin')  # Redirect to admin login if not authenticated

    admin = get_object_or_404(AdminUser, id=admin_id)
    requests = BookingRequest.objects.filter(status='pending')  # Ensure you are fetching pending requests
    return render(request, 'enroll/admin_company_requests.html', {'requests': requests,'admin_name':admin_name})


def update_booking_status(request, request_id, action):
    booking_request = get_object_or_404(BookingRequest, id=request_id)
    
    if action == 'approve':
        # Change status to 'booked' for the approved request
        booking_request.status = 'approved'
        booking_request.room.status = 'Booked'
        booking_request.room.booked_by = booking_request.company
        booking_request.save()
        booking_request.room.save()

        # Reject or delete all other pending requests for the same room
        BookingRequest.objects.filter(room=booking_request.room, status='pending').exclude(id=booking_request.id).delete()

        messages.success(request, f"Booking for Room {booking_request.room.number} has been approved and other requests for this room have been removed.")

    elif action == 'reject':
        # Mark the request as rejected
        booking_request.status = 'rejected'
        booking_request.save()
        messages.info(request, f"Booking request for Room {booking_request.room.number} has been rejected.")

    return redirect('manage_booking_requests')

def add_training_room(request):
    if request.method == 'POST':
        form = TrainingRoomForm(request.POST)
        if form.is_valid():
            form.save()  # Save the valid form to create a new Room
            return redirect('training_room_list')  # Redirect to the room list or another page
    else:
        form = TrainingRoomForm()

    return render(request, 'enroll/create_training_room.html', {'form': form})

# List all rooms for any user (admin or regular user)
def training_room_list(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')
    
    rooms = TrainingBookingRequest.objects.all()
    return render(request, 'enroll/room_details.html', {'rooms': rooms,'admin_name':admin_name})

# Functionality to book a room
def book_training_room(request, room_id):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')

    if not company_id:
        return redirect('company')
    room = get_object_or_404(TrainingRoom, id=room_id)
    error_messages = []  # Collect all error messages

    if request.method == 'POST':
        start_time = request.POST.get('start_time').strip()
        end_time = request.POST.get('end_time').strip()
        company_id = request.POST.get('company_id')
        booking_date = date.today()  # Default to today's date

        company = None  # Initialize company variable outside of try block

        # Condition 1: Check if company_id is provided and valid
        if not company_id:
            error_messages.append('Company ID is required.')
        else:
            try:
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                error_messages.append('Invalid company ID.')

        # Condition 2: Time conversion with flexible parsing
        start_time_obj, end_time_obj = None, None  # Initialize these to ensure availability for later checks
        time_formats = ['%I:%M %p', '%H:%M']  # 12-hour (am/pm) and 24-hour formats

        def parse_time(input_time):
            for fmt in time_formats:
                try:
                    return datetime.strptime(input_time, fmt).time()
                except ValueError:
                    continue
            return None

        start_time_obj = parse_time(start_time)
        end_time_obj = parse_time(end_time)

        if not start_time_obj or not end_time_obj:
            error_messages.append('Invalid time format. Please use a valid format (e.g., 11:00 AM or 23:00).')

        # Condition 3: Duration check (only if times were parsed)
        if start_time_obj and end_time_obj:
            duration = datetime.combine(date.min, end_time_obj) - datetime.combine(date.min, start_time_obj)
            max_duration = room.max_booking_duration  # Assuming this is in hours
            if duration > timedelta(hours=max_duration):
                error_messages.append(f'Booking duration cannot exceed {max_duration} hours.')

            # Condition 4: Check if booking times lie within the room's available hours
            if start_time_obj < room.start_time or end_time_obj > room.end_time:
                error_messages.append('Selected time must be within the room\'s available hours.')

        # Condition 5: Check for overlapping bookings (only if times were parsed)
        if start_time_obj and end_time_obj:
            overlapping_bookings = TrainingBookingRequest.objects.filter(
                room=room,
                booking_date=booking_date,
                status='booked'  # Only check for rooms with booked status
            ).filter(
                start_time__lt=end_time_obj,  # New end time should not be after any existing start time
                end_time__gt=start_time_obj   # New start time should not be before any existing end time
            )

            if overlapping_bookings.exists():
                error_messages.append('Room is already booked for the selected time slot today.')

        # If there are any error messages, display them and redirect
        if error_messages:
            for error in error_messages:
                messages.error(request, error)
            return redirect('book_training_room', room_id=room_id)

        # If no errors, proceed with booking
        if company and start_time_obj and end_time_obj:  # Ensure required fields are valid before creating booking
            booking = TrainingBookingRequest(
                room=room,
                company=company,
                start_time=start_time_obj,
                end_time=end_time_obj,
                booking_date=booking_date,  # Save today's date
                status='pending'  # Default status when the request is made
            )
            booking.save()
            messages.success(request, 'Booking request submitted successfully.')
            return redirect('book_training_room', room_id=room_id)

    return render(request, 'enroll/book_training_room.html', {'room': room,'company_name':company_name,'company_id':company_id})

    
def training_manage_booking_requests(request):
    booking_requests = TrainingBookingRequest.objects.filter(status='pending')
    return render(request, 'enroll/training_manage_booking_requests.html', {'booking_requests': booking_requests})

def training_update_booking_status(request, request_id, action):
    booking_request = get_object_or_404(TrainingBookingRequest, id=request_id)

    if action == 'accept':
        booking_request.status = 'booked'
        messages.success(request, 'Booking request accepted.')

        TrainingBookingRequest.objects.filter(
            room=booking_request.room,
            booking_date=booking_request.booking_date,
            start_time__lt=booking_request.end_time,
            end_time__gt=booking_request.start_time,
            status='pending'
        ).exclude(id=booking_request.id).update(status='rejected')
        
    elif action == 'reject':
        booking_request.status = 'available'
        messages.success(request, 'Booking request rejected.')
    
    booking_request.save()
    return redirect('training_manage_booking_requests')  # Redirect back to the requests list    


def delete_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    application.delete()
    messages.success(request, 'Application deleted successfully!')
    return redirect('view_applications', job_id=application.job.id)    

def download_resume(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    response = FileResponse(open(application.resume.path, 'rb'), as_attachment=True)
    return response

def view_resume(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    response = FileResponse(open(application.resume.path, 'rb'), as_attachment=False)
    return response


# Create global contract for all companies
def create_company_contract(request):
    admin_id= request.session.get('admin_id')
    admin_name= request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')
    if request.method == 'POST':
        form = CompanyContractForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Contract created successfully")
            return redirect('create_company_contract')
    else:
        form = CompanyContractForm()
    return render(request, 'enroll/create_company_contract.html', {'form': form,'admin_name':admin_name})

# Admin creates a contract for freelancers
def create_freelancer_contract(request):
    admin_id= request.session.get('admin_id')
    admin_name= request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')  # Redirect to login if no admin is logged in
    if request.method == 'POST':
        form = FreelancerContractForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Contract created successfully")
            return redirect('create_freelancer_contract')
    else:
        form = FreelancerContractForm()
    return render(request, 'enroll/create_freelancer_contract.html', {'form': form,'admin_name':admin_name})

# View contracts for the company
def view_company_contracts(request):
    company_id = request.session.get('company_id')  # Get the logged-in company's ID from the session
    company_name = request.session.get('company_name')  
    if not company_id:
        return redirect('company')  # Redirect to login if no company is logged in

    # Get the logged-in company
    company = get_object_or_404(Company, id=company_id)

    # Filter CompanyContracts where either the contract is global or the company has responded
    contracts = CompanyContract.objects.filter(
        Q(is_global=True) | Q(responses__company__id=company_id)
    ).distinct()

    # Prepare the response status for each contract
    for contract in contracts:
        contract_response = contract.responses.filter(company=company).first()
        if contract_response:
            contract.user_response_status = contract_response.status
        else:
            contract.user_response_status = None  # No response from the company

    context = {
        'contracts': contracts,
        'company': company,  # Pass company info to the template\
        'company_name': company_name,  # Pass company name to the template
    }
    return render(request, 'enroll/view_contracts.html', context)

# View contracts for the freelancer
def view_freelancer_contracts(request):
    freelancer_id = request.session.get('freelancer_id')
    freelancer_name = request.session.get('freelancer_name')
    if not freelancer_id:
        return redirect('login')

    # Get the logged-in freelancer
    freelancer = get_object_or_404(Freelancer, id=freelancer_id)

    # Filter FreelancerContracts where either the contract is global or the freelancer has responded
    contracts = FreelancerContract.objects.filter(
        Q(is_global=True) | Q(responses__freelancer__id=freelancer_id)
    ).distinct()

    # Prepare the response status for each contract
    for contract in contracts:
        contract_response = contract.responses.filter(freelancer=freelancer).first()
        if contract_response:
            contract.user_response_status = contract_response.status
        else:
            contract.user_response_status = None  # No response from the freelancer

    context = {
        'contracts': contracts,
        'freelancer': freelancer,  # Pass freelancer info to the template
        'freelancer_name': freelancer_name,  # Pass freelancer name to the template
    }
    return render(request, 'enroll/view_freelancer_contracts.html', context)

# Company responds to a contract
def respond_to_company_contract(request, contract_id, response):
    company_id = request.session.get('company_id')
    company = get_object_or_404(Company, id=company_id)
    if not company_id:
        return redirect('company')  # Redirect to login if no company is logged in

    # Get the contract
    contract = get_object_or_404(CompanyContract, id=contract_id)

    # Handle the "leave" action to delete the company profile
    if response == 'leave':
        company.delete()
        return redirect('company')  # Update with your desired URL

    # Get or create a response for the company to this contract
    contract_response, created = CompanyContractResponse.objects.get_or_create(
        company=company,
        contract=contract
    )

    # Update the response based on the action
    if response == 'agree':
        contract_response.status = 'Agreed'
        contract_response.agreed_by_company = True
    elif response == 'disagree':
        contract_response.status = 'Disagreed'
        contract_response.agreed_by_company = False

    # Save the response
    contract_response.save()

    return redirect('view_company_contracts')  # Adjust to the view that shows contract status


# Freelancer responds to a contract
def respond_to_freelancer_contract(request, contract_id, response):
    # Check for freelancer login
    freelancer_id = request.session.get('freelancer_id')
    if not freelancer_id:
        return redirect('freelancer')  # Redirect to freelancer login if not logged in

    freelancer = get_object_or_404(Freelancer, id=freelancer_id)
    
    # Get the contract
    contract = get_object_or_404(FreelancerContract, id=contract_id)

    # Handle the "leave" action to delete the freelancer profile
    if response == 'leave':
        freelancer.delete()
        return redirect('freelancer')  # Redirect after profile deletion

    # Get or create a response for the freelancer to this contract
    contract_response, created = FreelancerContractResponse.objects.get_or_create(
        freelancer=freelancer,
        contract=contract
    )

    # Update the response based on the action
    if response == 'agree':
        contract_response.status = 'Agreed'
        contract_response.agreed_by_freelancer = True
    elif response == 'disagree':
        contract_response.status = 'Disagreed'
        contract_response.agreed_by_freelancer = False

    # Save the response
    contract_response.save()

    return redirect('view_freelancer_contracts')  # Redirect to the freelancer's contracts page



def view_edit_room_list(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')  # Redirect to login if no admin is logged in
    rooms = Room.objects.all()
    context={
        'rooms': rooms,
        'admin_name': admin_name,  # Pass admin name to the template for display in the template
    }
    return render(request, 'enroll/view_edit_room_list.html', context)

def room_edit(request, room_id):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('view_edit_room_list')  # Adjust the redirect URL as needed
    else:
        form = RoomForm(instance=room)
    return render(request, 'enroll/update_room.html', {'form': form, 'room': room,'admin_name':admin_name})

def room_delete(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return redirect('view_edit_room_list')  # Adjust the redirect URL as needed

# Desk Views
def view_edit_desk_list(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')
    desks = Desk.objects.all()
    return render(request, 'enroll/view_edit_desk_list.html', {'desks': desks,'admin_name':admin_name})

def desk_edit(request, desk_id):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')
    if not admin_id:
        return redirect('admin')
    desk = get_object_or_404(Desk, id=desk_id)
    if request.method == 'POST':
        form = DeskForm(request.POST, instance=desk)
        if form.is_valid():
            form.save()
            return redirect('view_edit_desk_list')  # Adjust the redirect URL as needed
    else:
        form = DeskForm(instance=desk)
    return render(request, 'enroll/update_desk.html', {'form': form, 'desk': desk,'admin_name':admin_name})

def desk_delete(request, desk_id):
    desk = get_object_or_404(Desk, id=desk_id)
    desk.delete()
    return redirect('view_edit_desk_list')  # Adjust the redirect URL as needed


def delete_freelancer(request, freelancer_id):
    freelancer = get_object_or_404(Freelancer, id=freelancer_id)
    if request.method == 'POST':
        freelancer.delete()
        messages.success(request, "Freelancer profile deleted successfully.")
        return redirect('view_profiles')  # Adjust this to your overview page URL name

def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        company.delete()
        messages.success(request, "Company profile deleted successfully.")
        return redirect('view_profiles')  # Adjust this to your overview page URL name
    

# View to create an announcement
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Announcement created successfully.")  # Display success message when announcement is created successfully
            return redirect('create_announcement')  # Redirect to announcements page after saving
    else:
        form = AnnouncementForm()
    return render(request, 'enroll/create_announcement.html', {'form': form})

# View to display announcements
def show_announcements(request):
    announcements = Announcement.objects.order_by('-created_at')
    print(announcements) 
    return render(request, 'enroll/announcements.html', {'announcements': announcements})

def add_faq(request):
    admin_id = request.session.get('admin_id')  # Get the logged-in admin's ID from the session
    admin_name = request.session.get('admin_name')  
    if not admin_id:
        return redirect('admin')
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faq_list')
    else:
        form = FAQForm()
    return render(request, 'enroll/add_faq.html', {'form': form,'admin_name': admin_name})

class FAQListView(ListView):
    def get(self, request):
        admin_id = request.session.get('admin_id')  # Get the logged-in admin's ID from the session
        admin_name = request.session.get('admin_name')  
        if not admin_id:
           return redirect('admin')
        # Fetch all FAQs
        faqs = FAQ.objects.all()
        return render(request, 'enroll/faq_list.html', {
            'faqs': faqs,
            'admin_name': admin_name 
            
        })

def companyfaq_list_view(request):
    company_id = request.session.get('company_id')  # Get the logged-in company's ID from the session
    company_name = request.session.get('company_name')  
    if not company_id:
        return redirect('company')
    faqs = FAQ.objects.all()  # Fetch all FAQs
    announcements = Announcement.objects.order_by('-created_at')  # Fetch announcements sorted by latest
    return render(request, 'enroll/company_faq_list.html', {
        'faqs': faqs,
        'announcements': announcements,
        'company_name': company_name
    })

def freelancerfaq_list_view(request):
    freelancer_id = request.session.get('freelancer_id')  # Get the logged-in freelancer's ID from the session
    freelancer_name = request.session.get('freelancer_name')  
    if not freelancer_id:
        return redirect('freelancer')
    faqs = FAQ.objects.all()  # Fetch all FAQs
    announcements = Announcement.objects.order_by('-created_at')  # Fetch announcements sorted by latest
    return render(request, 'enroll/freelancer_faq_list.html', {
        'faqs': faqs,
        'announcements': announcements,
        'freelancer_name': freelancer_name
    })









def contact_list_view(request):
    # Check if the user is logged in (either freelancer or company)
    freelancer_id = request.session.get('freelancer_id')
    company_id = request.session.get('company_id')

    if not freelancer_id and not company_id:
        return redirect('login')

    # Fetch all freelancers and companies
    freelancers = Freelancer.objects.all()
    companies = Company.objects.all()

    # Combine freelancers and companies into a single list with labels
    contact_list = []
    for freelancer in freelancers:
        contact_list.append({
            'id': freelancer.id,
            'name': freelancer.freelancer_name,
            'type': 'freelancer',  # Label as 'freelancer'
        })

    for company in companies:
        contact_list.append({
            'id': company.id,
            'name': company.company_name,
            'type': 'company',  # Label as 'company'
        })

    # Sort contacts alphabetically by name
    contact_list = sorted(contact_list, key=lambda x: x['name'].lower())

    context = {
        'contact_list': contact_list,
    }

    return render(request, 'enroll/contact_list.html', context)


def chat_with_contact(request, contact_id, contact_type):
    # Identify the logged-in user
    freelancer_id = request.session.get('freelancer_id')
    company_id = request.session.get('company_id')

    if freelancer_id:
        user = get_object_or_404(Freelancer, id=freelancer_id)
        user_is_freelancer = True
    elif company_id:
        user = get_object_or_404(Company, id=company_id)
        user_is_freelancer = False
    else:
        return redirect('login')

    # Identify the contact
    if contact_type == 'freelancer':
        contact = get_object_or_404(Freelancer, id=contact_id)
        contact_name = contact.freelancer_name
        contact_is_freelancer = True
    elif contact_type == 'company':
        contact = get_object_or_404(Company, id=contact_id)
        contact_name = contact.company_name
        contact_is_freelancer = False
    else:
        return redirect('contact_list')

    # Fetch messages between the logged-in user and the contact
    messages = Message.objects.filter(
        Q(sender_freelancer=user if user_is_freelancer else None, recipient_freelancer=contact if contact_is_freelancer else None) |
        Q(sender_freelancer=contact if contact_is_freelancer else None, recipient_freelancer=user if user_is_freelancer else None) |
        Q(sender_company=user if not user_is_freelancer else None, recipient_freelancer=contact if contact_is_freelancer else None) |
        Q(sender_freelancer=user if user_is_freelancer else None, recipient_company=contact if not contact_is_freelancer else None) |
        Q(sender_company=user if not user_is_freelancer else None, recipient_company=contact if not contact_is_freelancer else None) |
        Q(sender_company=contact if not contact_is_freelancer else None, recipient_company=user if not user_is_freelancer else None)
    ).order_by('timestamp')

    # Handle message sending
    if request.method == 'POST':
        body = request.POST.get('message')
        if body:
            Message.objects.create(
                sender_freelancer=user if user_is_freelancer else None,
                sender_company=user if not user_is_freelancer else None,
                recipient_freelancer=contact if contact_is_freelancer else None,
                recipient_company=contact if not contact_is_freelancer else None,
                body=body
            )
            return redirect('chat_with_contact', contact_id=contact_id, contact_type=contact_type)

    # Pass data to the template
    context = {
        'contact_name': contact_name,
        'messages': messages,
        'user_id': user.id,
        'user_is_freelancer': user_is_freelancer,
    }
    return render(request, 'enroll/chat.html', context)