from datetime import date, datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password ,check_password
from .models import FAQ, Announcement, CompanyContractResponse, FreelancerContractResponse, TrainingBookingRequest,CompanyContract, FreelancerContract, TrainingRoom, User, Room, Desk,Message, Company, Freelancer ,FreelancerRegistration,CompanyRegistration, AdminUser,Room, Desk, Booking, Company_Portfolio ,Company_Complaint, JobPosting , Job_portal,  Freelancer_Complaint ,Freelancer_Portfolio, JobApplication

class StudentRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['number', 'status', 'details','booked_by']
class CompanyRegistrationform(forms.ModelForm):
    class Meta:
        model = CompanyRegistration
        fields = [
            'company_name',
            'email',
            'phone_number',
            'password',
            'address',
            'industry',
            'number_of_employees',
        ]
        widgets = {
            'password': forms.PasswordInput(),  # To hide password input
        }
class FreelancerRegistrationform(forms.ModelForm):
    class Meta:
        model = FreelancerRegistration
        fields = [
            'freelancer_name',
            'email',
            'phone_number',
            'password',
            'address',
            'date_of_birth',
        ]
        widgets = {
            'password': forms.PasswordInput(),  # To hide password input
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),  # Date input for better UX
        }
        
class CompanySignupForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['email', 'company_name', 'phone_number', 'password']

class FreelancerSignupForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['email', 'freelancer_name', 'phone_number', 'password']

class AdminSignupForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ['email', 'admin_name', 'phone_number', 'password']


class JobSignupForm(forms.ModelForm):
    class Meta:
        model = Job_portal
        fields = ['email', 'name', 'phone_number', 'password','address','date_of_birth']
        

class CompanyLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        # Fetch the company by email
        company = Company.objects.filter(email=email).first()

        # Direct comparison of the password (insecure, but for demo purposes)
        if company and check_password(password, company.password):
            return self.cleaned_data
        else:
            raise forms.ValidationError('Invalid email or password for company.')

class FreelancerLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        freelancer = Freelancer.objects.filter(email=email).first()

        if freelancer and check_password(password, freelancer.password):  # Direct comparison (insecure, but for demo purposes)
            return self.cleaned_data
        else:
            raise forms.ValidationError('Invalid email or password for freelancer.')
        

class AdminLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        adminuser = AdminUser.objects.filter(email=email).first()

        if adminuser and adminuser.password == password:  # Simple authentication check
            return self.cleaned_data
        else:
            raise forms.ValidationError('Invalid email or password for Admin.')
        

class JobLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        jobportal = Job_portal.objects.filter(email=email).first()

        if jobportal and check_password(password, jobportal.password): # Simple authentication check
            return self.cleaned_data
        else:
            raise forms.ValidationError('Invalid email or password please check and try again.')
            
class Company_PortfolioForm(forms.ModelForm):
    class Meta:
        model = Company_Portfolio
        fields = ['name', 'email', 'phone', 'summary', 'services', 'projects', 'awards', 'website', 'contact']

class Company_ComplaintForm(forms.ModelForm):
    class Meta:
        model = Company_Complaint
        fields = ['name', 'email', 'subject', 'message']

class Freelancer_PortfolioForm(forms.ModelForm):
    class Meta:
        model = Freelancer_Portfolio
        fields = ['name', 'email', 'phone', 'summary', 'experience', 'education', 'skills', 'awards', 'additional', 'contact']

class Freelancer_ComplaintForm(forms.ModelForm):
    class Meta:
        model = Freelancer_Complaint
        fields = ['name', 'email', 'subject', 'message']

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['job_title', 'num_people', 'qualifications', 'salary', 'job_description', 'location', 'job_type', 'skills']
        exclude = ['timestamp']  # Exclude the posted_at field

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['name','phone_number', 'email','education_level', 'work_experience','cover_letter', 'resume']     

      
class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'email', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if the email has been changed
        if self.instance.email != email:
            # Check if the email exists in the Company model
            if Company.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use by another company.")
            
            # Check if the email exists in the Freelancer model
            if Freelancer.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use by a freelancer.")
            
            if AdminUser.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use by a admin.")
            
            if Job_portal.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use by a job_portal.")
        
        return email
    


class FreelancerUpdateForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['freelancer_name', 'email', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Mask the password field
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Only check for uniqueness if the email has been changed
        if self.instance.email != email:
            # Check if the email exists in the Freelancer model
            if Freelancer.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use by another freelancer.")

            # Check if the email exists in the Company model
            if Company.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use by a company.")
            if AdminUser.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use by a admin.")
            
            if Job_portal.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use by a job_portal.")

        return email

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number']

class DeskForm(forms.ModelForm):
    class Meta:
        model = Desk
        fields = ['room', 'desk_number']
    def clean_desk_number(self):
        desk_number = self.cleaned_data.get('desk_number')
        room = self.cleaned_data.get('room')

        # Check if a desk with the same number already exists in the same room
        if Desk.objects.filter(desk_number=desk_number, room=room).exists():
            raise forms.ValidationError(f"A desk with number {desk_number} already exists in this room.")
        
        return desk_number    

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['desk', 'time_slot', 'date']
        widgets = {
            'date': forms.SelectDateWidget(),  # Optional date picker widget
        }

class RoomAvailabilityForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), empty_label="Select a Room")

    def get_availability(self):
        room = self.cleaned_data.get('room')
        availability = []

        if room:
            for desk in room.desks.all():
                desk_availability = {
                    'desk_number': desk.desk_number,
                    'time_slots': {}
                }
                for time_slot in ['08:00-16:00', '16:00-00:00', '00:00-08:00']:
                    bookings = desk.bookings.filter(time_slot=time_slot)

                    if bookings.exists():
                        booking = bookings.first()
                        desk_availability['time_slots'][time_slot] = 'Booked' if booking.is_booked else 'Available'
                    else:
                        desk_availability['time_slots'][time_slot] = 'Available'

                availability.append(desk_availability)
        
        return availability
        

# class MessageForm(forms.ModelForm):
#     recipient = forms.ModelChoiceField(
#         queryset=Freelancer.objects.all(), 
#         required=False, 
#         label="Select Freelancer Recipient"
#     )
#     company_recipient = forms.ModelChoiceField(
#         queryset=Company.objects.all(), 
#         required=False, 
#         label="Select Company Recipient"
#     )

#     class Meta:
#         model = Message
#         fields = ['subject', 'body', 'recipient', 'company_recipient']

#     def clean(self):
#         cleaned_data = super().clean()
#         recipient = cleaned_data.get('recipient')
#         company_recipient = cleaned_data.get('company_recipient')

#         if not recipient and not company_recipient:
#             raise forms.ValidationError("Please specify a recipient (Freelancer or Company).")

#         return cleaned_data
    

# class ReplyForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ['body']  

class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = TrainingBookingRequest
        fields = ['room', 'start_time', 'end_time', 'status']

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Check if the booking duration is valid
        if start_time and end_time:
            booking_duration = (datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)).total_seconds() / 3600
            if booking_duration > room.max_booking_duration:
                raise forms.ValidationError(f'Maximum booking duration is {room.max_booking_duration} hours.')

        return cleaned_data       
    
class TrainingRoomForm(forms.ModelForm):
    start_time = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M %p'),
        input_formats=['%I:%M %p'],  # Accepts time in AM/PM format
        label="Start time"
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M %p'),
        input_formats=['%I:%M %p'],  # Accepts time in AM/PM format
        label="End time"
    )

    class Meta:
        model = TrainingRoom  # Ensure you're using the correct model
        fields = ['number', 'start_time', 'end_time', 'max_booking_duration']




class CompanyContractForm(forms.ModelForm):
    class Meta:
        model = CompanyContract
        fields = ['contract_details']

# Freelancer Contract Form
class FreelancerContractForm(forms.ModelForm):
    class Meta:
        model = FreelancerContract
        fields = ['contract_details']

# Company Contract Response Form
class CompanyContractResponseForm(forms.ModelForm):
    class Meta:
        model = CompanyContractResponse
        fields = ['status']

# Freelancer Contract Response Form
class FreelancerContractResponseForm(forms.ModelForm):
    class Meta:
        model = FreelancerContractResponse
        fields = ['status']    


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
        labels = {
            'text': 'Add Announcement',
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the question'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the answer'}),
        }