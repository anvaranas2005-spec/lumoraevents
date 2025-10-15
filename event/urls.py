from django.urls import path
import event.views



urlpatterns = [
    path('', event.views.home, name='home'),
    path('services/', event.views.services, name='services'),
    path('about/', event.views.about, name='about'),
    path('contact/', event.views.contact, name='contact'),
    path('TermsofService/', event.views.TermsofService, name='TermsofService'),
    path('PrivacyPolicy/', event.views.PrivacyPolicy, name='PrivacyPolicy'),
    path('user_TermsofService/', event.views.user_TermsofService, name='user_TermsofService'),
    path('user_PrivacyPolicy/', event.views.user_PrivacyPolicy, name='user_PrivacyPolicy'),
    path('portfolio/', event.views.portfolio, name='portfolio'),
    path('register/', event.views.register, name='register'),
    path('login/', event.views.login_view, name='login'),
    path('logout/', event.views.logout, name='logout'),
    path('dashboard/', event.views.user_dashboard, name='user_dashboard'),
    path('user_portfolio/', event.views.user_portfolio, name='user_portfolio'),
    path('user_services/', event.views.user_services, name='user_services'),
    path('user_about/', event.views.user_about, name='user_about'),
    path('user_services/', event.views.user_services, name='user_services'),
    path('services/book/', event.views.service_booking, name='service_booking'),
    path('book/<int:service_id>/', event.views.service_booking, name='service_booking'),
    path('submit-feedback/', event.views.feedback_view, name='submit_feedback'),
    path('feedback/', event.views.feedback_view, name='feedback_page'),
    path('user_contact/', event.views.user_contact, name='user_contact'),
]