from django.contrib import admin
from enroll.models import FAQ, Announcement, CompanyContract, CompanyContractResponse, FreelancerContract, FreelancerContractResponse, JobApplication, TrainingBookingRequest, User,BookingRequest,TrainingRoom,Message,FreelancerRegistration,CompanyRegistration,Room, Desk, Booking, Company, Freelancer, AdminUser ,Job_portal, Company_Portfolio ,Company_Complaint, JobPosting , Freelancer_Portfolio ,Freelancer_Complaint



@admin.register(FreelancerRegistration)
class freelancerregistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'freelancer_name','email','phone_number','password','address','date_of_birth')

@admin.register(CompanyRegistration)
class companyregistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name','email','phone_number','password','address','industry','number_of_employees')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'status', 'details','booked_by')

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ['company', 'room', 'status', 'created_at'] 
  
@admin.register(Company_Complaint)
class Company_ComplaintAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'email', 'subject', 'message']  

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['id','job_title', 'num_people', 'qualifications', 'salary', 'skills','job_description', 'location', 'job_type','timestamp']


@admin.register(JobApplication)
class job_application(admin.ModelAdmin):
    list_display = ['id','name','phone_number', 'education_level', 'work_experience','cover_letter', 'resume','applicant']  
    
@admin.register(Company_Portfolio)
class Company_PortfolioAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'email', 'phone', 'summary', 'services', 'projects', 'awards', 'website', 'contact'] 
    
@admin.register(Freelancer_Portfolio)
class Freelancer_PortfolioAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'email', 'phone', 'summary', 'experience', 'education', 'skills', 'awards', 'additional', 'contact'] 

@admin.register(Freelancer_Complaint)
class Freelancer_ComplaintAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'email', 'subject', 'message'] 

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id','company_name','email', 'phone_number','password'] 

@admin.register(Freelancer)
class FreelancerAdmin(admin.ModelAdmin):
    list_display = ['id','freelancer_name','email', 'phone_number','password']    


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['id','admin_name','email', 'phone_number','password']  

@admin.register(Job_portal)
class jobAdmin(admin.ModelAdmin):
    list_display = ['id','name','email', 'phone_number','password','address','date_of_birth']   

@admin.register(Room)
class roomAdmin(admin.ModelAdmin):
    list_display = ['id','room_number']  

@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display = ['id','room', 'desk_number'] 

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id','desk', 'time_slot','status', 'date','freelancer']  

@admin.register(TrainingRoom)
class TrainingRoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'start_time', 'end_time', 'max_booking_duration')

@admin.register(TrainingBookingRequest)
class TrainingBookingRequestAdmin(admin.ModelAdmin):
    list_display = ('room', 'company', 'start_time', 'end_time','status')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','sender_freelancer','sender_company', 'recipient_freelancer', 'recipient_company', 'body')    


@admin.register(CompanyContract)
class CompanyContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract_details', 'created_at', 'is_global')  # Use available fields

@admin.register(FreelancerContract)
class FreelancerContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract_details', 'created_at', 'is_global')  # Use available fields

@admin.register(CompanyContractResponse)
class CompanyContractResponseAdmin(admin.ModelAdmin):
    list_display = ('contract', 'company', 'status', 'agreed_by_company')

@admin.register(FreelancerContractResponse)
class FreelancerContractResponseAdmin(admin.ModelAdmin):
    list_display = ('contract', 'freelancer', 'status', 'agreed_by_freelancer')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id','text','created_at')
    

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question','answer','created_at')
    search_fields = ('question', 'answer')    

