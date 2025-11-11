from django.contrib import admin
from django.urls import path
from enroll import views 
from enroll.views import company_login_view, freelancer_login_view, admin_login_view ,job_login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('freelancer-registration/', views.freelancer_registration_view, name='freelancer_registration'),
    path('company-registration/', views.company_registration_view, name='company-registration'),
    path('admindashboard/freelancer-applications/', views.show_freelancer_application_view, name='freelancer-applications'),
    path('admindashboard/company-applications/', views.show_company_application_view, name='company-applications'),
    path('freelancer/', freelancer_login_view, name='freelancer'),
    path('index/', views.index_page, name='index'),
    path('company/', company_login_view, name='company'),
    path('', admin_login_view, name='admin'),
    path('addandshow/', views.add_show, name='addandshow'),
    path('company/showrooms/', views.show_rooms, name='show_rooms'),
    path('rooms', views.show_rooms_view, name='rooms'),
    path('check_rooms', views.check_rooms_view, name='check_rooms'),
    path('admindashboard/check_rooms', views.show_rooms_admin, name='admin_check_rooms'),
    path('showjobs/', views.add_show_jobs, name='show_jobs'),
    path('delete/<int:id>/', views.delete_data, name='deletedata'),  # Note: Fixed path pattern
    path('update/<int:id>/', views.update_data, name='updatedata'),
    path('admindashboard/', views.admin_dashboard, name='adminpage'),
    path('company/companydashboard/', views.company_dashboard, name='companydashboard'),
    path('jobportal/', job_login_view, name='job_portal'),
    path('company/complaint/', views.complaint_view, name='complaint'),
    path('company/portfolio/', views.portfolio_view, name='portfolio'), 
    path('freelancerdashboard/complaint/', views.freelancer_complaint_view, name='freelancer_complaint'),
    path('freelancerdashboard/freelancerportfolio/', views.freelancer_portfolio_view, name='freelancer_portfolio'), 
    path('company/postjob/', views.job_posting_view, name='jobcreation'),
    path('freelancer/freelancerdashboard/', views.freelancer_dashboard, name='freelancerdashboard'),
    path('success/', views.success, name='success'),
    path('admindashboard/company', views.company_signup, name='company_signup'),
    path('admindashboard/freelancer-signup/',views.freelancer_signup, name='freelancer_signup'),
    path('signupjob/',views.job_portal_signup, name='job_portal_signup'),
    path('company/portfolio/', views.portfolio_view, name='portfolio'),
    path('admindashboard/view-edit', views.view_edit, name='viewedit'),
    path('company/edit-profile/', views.company_edit_profile_view, name='company_edit_profile'),
    path('freelancer/edit-profile/', views.freelancer_edit_profile_view, name='freelancer_edit_profile'),
    path('admindashboard/rooms/create/', views.create_room_view, name='create_room'),
    path('desks/create/', views.create_desk_view, name='create_desk'),
    path('booking/create/', views.book_desk_view, name='book_desk'),
    path('rooms/', views.room_list_view, name='room_list'),
    path('check_room_list/', views.check_room_list_view, name='check_room_list'),
    path('admindashboard/check_room_list/', views.admin_room_list_view, name='admin_check_room_list'),
    path('admindashboard/requests/', views.admin_booking_management, name='admin_requests'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('admindashboard/booking-requests/', views.manage_booking_requests, name='manage_booking_requests'),    
    path('update-booking-status/<int:request_id>/<str:action>/', views.update_booking_status, name='update_booking_status'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('applications/<int:job_id>/', views.view_applications, name='view_applications'),
    path('applications/<int:job_posting_id>/', views.company_applications, name='company_applications'),
    path('applications/delete/<int:application_id>/', views.delete_application, name='delete_application'),
    path('resume/download/<int:application_id>/', views.download_resume, name='download_resume'),
    path('resume/view/<int:application_id>/', views.view_resume, name='view_resume'),
    path('admindashboard/complaints', views.show_complaint, name='view_complaint'),
    path('admindashboard/profiles', views.show_profiles, name='view_profiles'),
    path('rooms-details/', views.training_room_list, name='training_room_list'),
    path('rooms/book/<int:room_id>/', views.book_training_room, name='book_training_room'),  # Room booking for all users
    path('rooms/add/', views.add_training_room, name='add_training_room'),  # Room creation for admin only
    path('admindashboard/bookings/', views.training_manage_booking_requests, name='training_manage_booking_requests'),
    path('admindashboard/bookings/<int:request_id>/<str:action>/', views.training_update_booking_status, name='training_update_booking_status'),
    path('create_company_contract/', views.create_company_contract, name='create_company_contract'),
    path('create_freelancer_contract/', views.create_freelancer_contract, name='create_freelancer_contract'),
    path('company/contracts/', views.view_company_contracts, name='view_company_contracts'),
    path('freelancer/contracts/', views.view_freelancer_contracts, name='view_freelancer_contracts'),
    path('company/contracts/<int:contract_id>/<str:response>/', views.respond_to_company_contract, name='respond_to_company_contract'),
    path('freelancer/contracts/<int:contract_id>/<str:response>/', views.respond_to_freelancer_contract, name='respond_to_freelancer_contract'),

    path('admindashboard/view_edit_rooms/', views.view_edit_room_list, name='view_edit_room_list'),
    path('rooms/edit/<int:room_id>/', views.room_edit, name='room_edit'),
    path('rooms/delete/<int:room_id>/', views.room_delete, name='room_delete'),

    # Desk URLs
    path('admindashboard/view_edit_desk/', views.view_edit_desk_list, name='view_edit_desk_list'),
    path('desks/edit/<int:desk_id>/', views.desk_edit, name='desk_edit'),
    path('desks/delete/<int:desk_id>/', views.desk_delete, name='desk_delete'),
    
    path('delete_freelancer/<int:freelancer_id>/', views.delete_freelancer, name='delete_freelancer'),
    path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),

    path('company/logout/', views.company_logout, name='company_logout'),
    path('freelancer/logout/', views.freelancer_logout, name='freelancer_logout'),
    path('adminpage/logout/', views.admin_logout, name='admin_logout'),

    path('announcements/', views.show_announcements, name='show_announcements'),
    path('create-announcement/', views.create_announcement, name='create_announcement'),

    path('add_faqs/', views.add_faq, name='add_faq'),
    path('view_faqs', views.FAQListView.as_view(), name='faq_list'),
    path('company/view_faqs', views.companyfaq_list_view, name='companyfaq_list'),
    path('freelancer/view_faqs', views.freelancerfaq_list_view, name='freelancerfaq_list'),


    path('contacts/', views.contact_list_view, name='contact_list'),
    
    # Route to open the chat with a specific contact
    path('chat/<int:contact_id>/<str:contact_type>/', views.chat_with_contact, name='chat_with_contact'),

]
