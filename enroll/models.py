from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from .validators import validate_unique_email
from django.utils import timezone
from datetime import date, timedelta,datetime, time
from django.utils.timezone import now



class Freelancer(models.Model):
    freelancer_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True, validators=[EmailValidator()])
    phone_number = models.CharField(max_length=200)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email
    def delete(self, *args, **kwargs):
        # Set all rooms booked by this company to available
        Booking.objects.filter(freelancer=self).update(status='Available')
        super().delete(*args, **kwargs)  # Proceed with deletion


class Company(models.Model):
    company_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True, validators=[EmailValidator()])
    phone_number = models.CharField(max_length=200)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email
    
    def delete(self, *args, **kwargs):
        # Set all rooms booked by this company to 'Available'
        User.objects.filter(booked_by=self).update(status='Available')
        super().delete(*args, **kwargs)  # Proceed with deletion
    

class FreelancerRegistration(models.Model):
    freelancer_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)  # New field
    def __str__(self):
        return self.email
    
    
class CompanyRegistration(models.Model):
    company_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, null=True, blank=True)  
    number_of_employees = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.email
    
class Job_portal(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True, validators=[EmailValidator(), validate_unique_email])
    phone_number = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)  # New field

    def __str__(self):
        return self.email

class AdminUser(models.Model):
    admin_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True, validators=[EmailValidator(), validate_unique_email])
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email
    
class User(models.Model):

    number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)
    details = models.CharField(max_length=256)
    booked_by = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
      return f'Room {self.number}'
    

class BookingRequest(models.Model):
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    room = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking request for Room {self.room.number} by {self.company.company_name}'
        
    
class Company_Portfolio(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=100)  
    email = models.EmailField()                
    phone = models.CharField(max_length=20)   
    summary = models.TextField()                
    services = models.TextField(blank=True, null=True)  
    projects = models.TextField(blank=True, null=True)
    awards = models.TextField()   
    website = models.URLField(blank=True, null=True)  
    contact = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name
    
class Company_Complaint(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.subject

class JobPosting(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_portal = models.ForeignKey(Job_portal, on_delete=models.CASCADE, related_name='job_postings')
    job_title = models.CharField(max_length=200)
    num_people = models.IntegerField()
    qualifications = models.TextField()
    salary = models.CharField(max_length=100)
    job_description = models.TextField()
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=100)
    skills = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.job_title


class JobApplication(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')  # Linked job posting
    applicant = models.ForeignKey(Job_portal, on_delete=models.CASCADE)  # The user applying for the job  
    name = models.CharField( max_length=50)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Phone number of the applicant
    education_level = models.CharField(max_length=100, null=True, blank=True)  # Education level of the applicant
    work_experience = models.TextField(null=True, blank=True) 
    cover_letter = models.TextField()
    email = models.EmailField(max_length=55)
    resume = models.FileField(upload_to='resumes/')  # Optional, if you want to upload files
    applied_at = models.DateTimeField(default=timezone.now)
 
    def __str__(self):
        return f'{self.applicant} applied for {self.job}'
    
class Freelancer_Portfolio(models.Model):
    freelancer = models.OneToOneField(Freelancer, on_delete=models.CASCADE,null=True, blank=True)  # One-to-one relationship
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    summary = models.TextField()
    experience = models.TextField()
    education = models.TextField()
    skills = models.TextField()
    awards = models.TextField()
    additional = models.TextField()
    contact = models.TextField()

    def __str__(self):
        return self.name
    
class Freelancer_Complaint(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.subject    


class Room(models.Model):
    room_number = models.IntegerField(unique=True)  # Ensure unique room numbers

    def __str__(self):
        return f"Room {self.room_number}"

class Desk(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="desks")
    desk_number = models.IntegerField()

    class Meta:
        # Ensure desk numbers are unique within each room
        constraints = [
            models.UniqueConstraint(fields=['room', 'desk_number'], name='unique_room_desk')
        ]

    def __str__(self):
        return f"Desk {self.desk_number} in {self.room}"

class Booking(models.Model):
    TIME_SLOTS = [
        ('08:00-16:00', '8:00 AM to 4:00 PM'),
        ('16:00-00:00', '4:00 PM to 12:00 AM'),
        ('00:00-08:00', '12:00 AM to 8:00 AM'),
    ]

    desk = models.ForeignKey(Desk, on_delete=models.CASCADE, related_name="bookings")
    freelancer = models.ForeignKey(Freelancer,null=True, blank=True, on_delete=models.CASCADE)
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    date = models.DateField()
    status = models.CharField(max_length=10, default='Pending')

    def __str__(self):
        return f"Booking for {self.desk} on {self.date} during {self.time_slot}"

    @property
    def is_booked(self):
        return self.status == 'booked'


class TrainingRoom(models.Model):
    number = models.CharField(max_length=100,unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_booking_duration = models.IntegerField(help_text="Maximum booking duration in hours")
    
    def __str__(self):
        return f'Room {self.number}'

class TrainingBookingRequest(models.Model):
    room = models.ForeignKey(TrainingRoom, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_time = models.TimeField()  # Start time of the booking
    end_time = models.TimeField()    # End time of the booking
    booking_date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, default="pending")

    def __str__(self):
        return f"Booking by {self.company} for Room {self.room.number} on {self.booking_date}"

class Message(models.Model):
    # Define sender and recipient relationships
    sender_freelancer = models.ForeignKey(Freelancer, null=True, blank=True, on_delete=models.SET_NULL, related_name="sent_messages")
    sender_company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, related_name="sent_messages")
    recipient_freelancer = models.ForeignKey(Freelancer, null=True, blank=True, on_delete=models.SET_NULL, related_name="received_messages")
    recipient_company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, related_name="received_messages")
    body = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        sender = self.sender_freelancer or self.sender_company
        recipient = self.recipient_freelancer or self.recipient_company
        return f'Message from {sender} to {recipient}'

    class Meta:
        ordering = ['-timestamp']


class CompanyContract(models.Model):
    contract_details = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_global = models.BooleanField(default=True)  # Visible to all companies by default

    def __str__(self):
        return f"Contract for Companies: {self.contract_details[:20]}..."

# Freelancer Contract Model
class FreelancerContract(models.Model):
    contract_details = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_global = models.BooleanField(default=True)  # Visible to all freelancers by default

    def __str__(self):
        return f"Contract for Freelancers: {self.contract_details[:20]}..."

# Company Contract Response Model
class CompanyContractResponse(models.Model):
    CONTRACT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    ]

    contract = models.ForeignKey(CompanyContract, on_delete=models.CASCADE, related_name='responses')
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS_CHOICES, default='Pending')
    agreed_by_company = models.BooleanField(default=False)

    def __str__(self):
        return f"Response by {self.company.company_name} - {self.status}"

# Freelancer Contract Response Model
class FreelancerContractResponse(models.Model):
    CONTRACT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Agreed', 'Agreed'),
        ('Disagreed', 'Disagreed')
    ]

    contract = models.ForeignKey(FreelancerContract, on_delete=models.CASCADE, related_name='responses')
    freelancer = models.ForeignKey(Freelancer, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS_CHOICES, default='Pending')
    agreed_by_freelancer = models.BooleanField(default=False)

    def __str__(self):
        return f"Response by {self.freelancer.freelancer_name} - {self.status}"
    

class Announcement(models.Model):
    text = models.TextField()  # Announcement content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of announcement creation

    def __str__(self):
        return self.text[:50]  # Display a snippet of the text in the admin panel


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question