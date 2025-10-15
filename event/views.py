from django.shortcuts import render, get_object_or_404
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return render(request,'home.html')


def services(request):
    active_services = Service.objects.filter(is_active=True).order_by('order')
    return render(request, 'services.html', {'services': active_services})


from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import EventService


def user_services(request):
    """
    Enhanced event service listing view with:
    - Price type filtering (All/Fixed/Hourly/Custom)
    - Search functionality
    - Sorting options
    - Pagination
    """
    # Base queryset - only active services
    services_list = EventService.objects.filter(is_active=True)

    # 1. PRICE TYPE FILTERING
    price_type = request.GET.get('price_type', 'all')
    if price_type in dict(EventService.PRICE_CHOICES).keys():
        services_list = services_list.filter(price_type=price_type)
    # 'all' shows all services

    # 2. SEARCH FUNCTIONALITY
    search_query = request.GET.get('q', '')
    if search_query:
        services_list = services_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # 3. SORTING OPTIONS
    sort_by = request.GET.get('sort', 'order')  # Default to manual ordering
    valid_sort_fields = {
        'title': 'title',
        'price': 'price',
        'order': 'order',  # Your existing manual ordering
        'newest': '-created_at',
        'featured': '-is_featured',  # Add this field if needed
    }

    if sort_by in valid_sort_fields:
        services_list = services_list.order_by(valid_sort_fields[sort_by])

    # 4. PAGINATION
    items_per_page = int(request.GET.get('items', 12))  # Default 12, configurable
    paginator = Paginator(services_list, items_per_page)
    page_number = request.GET.get('page')

    try:
        services = paginator.page(page_number)
    except PageNotAnInteger:
        services = paginator.page(1)
    except EmptyPage:
        services = paginator.page(paginator.num_pages)

    # Context data
    context = {
        'services': services,
        'search_query': search_query,
        'sort_by': sort_by,
        'current_price_type': price_type,
        'price_types': EventService.PRICE_CHOICES,
        'items_per_page': items_per_page,
        'page_title': 'Our Event Services',
        'meta_description': 'Browse our comprehensive event planning and management services',
    }

    return render(request, 'user_services.html', context)


def service_detail(request, slug):
    """Detailed view for a single service with view counting"""
    service = get_object_or_404(EventService, slug=slug, is_active=True)

    # Increment view count (add views field to model if needed)
    if hasattr(service, 'views'):
        service.views += 1
        service.save(update_fields=['views'])

    # Get related services (same price type, excluding current)
    related_services = EventService.objects.filter(
        price_type=service.price_type,
        is_active=True
    ).exclude(
        id=service.id
    ).order_by('?')[:4]  # Random 4 services

    context = {
        'service': service,
        'related_services': related_services,
        'page_title': f'{service.title} | Services',
        'meta_description': service.description[:160],
    }

    return render(request, 'service_detail.html', context)


def about(request):
    return render(request,'about.html')

def user_about(request):
    return render(request,'user_about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        # Validate form data
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill all required fields')
            return redirect('contact')

        try:
            # Email to admin
            admin_subject = f"New Contact Form: {subject}"
            admin_message = f"""
            Name: {name}
            Email: {email}
            Subject: {subject}
            Message: {message}
            """

            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )

            # Optional: Send confirmation to user
            user_subject = "Thank you for contacting Lumora Events"
            user_message = f"""
            Dear {name},

            Thank you for reaching out to us. We've received your message and will get back to you soon.

            Your message:
            {message}

            Best regards,
            The Lumora Events Team
            """

            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, 'Thank you for your message! We will contact you soon.')
            return redirect('contact')

        except Exception as e:
            messages.error(request, 'An error occurred while sending your message. Please try again later.')
            # Log the error if needed
            # import logging
            # logging.error(f"Contact form error: {str(e)}")
            return redirect('contact')

    return render(request, 'contact.html')


def TermsofService(request):
    return render(request,'TermsofService.html')

def PrivacyPolicy(request):
    return render(request,'PrivacyPolicy.html')

def user_TermsofService(request):
    return render(request,'user_TermsofService.html')

def user_PrivacyPolicy(request):
    return render(request,'user_PrivacyPolicy.html')


def portfolio(request):
    categories = PortfolioCategory.objects.filter(is_active=True)
    active_category = request.GET.get('category', 'all')

    portfolio_items = PortfolioItem.objects.filter(is_active=True).order_by('-event_date')

    if active_category != 'all':
        portfolio_items = portfolio_items.filter(category__slug=active_category)

    featured_items = PortfolioItem.objects.filter(is_featured=True, is_active=True)[:3]

    context = {
        'categories': categories,
        'active_category': active_category,
        'portfolio_items': portfolio_items,
        'featured_items': featured_items,
    }
    return render(request, 'portfolio.html', context)




def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please login.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose another.')
            return redirect('register')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            UserProfile.objects.create(user=user)
            auth.login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('register')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'login.html')


@login_required
def user_dashboard(request):
    now = timezone.now()
    events = Event.objects.filter(created_by=request.user).order_by('-date')

    context = {
        'events': events,
        'now': now,  # For status comparison in template
        'upcoming_events_count': events.filter(date__gte=now).count(),
        'monthly_events_count': events.filter(
            date__month=now.month,
            date__year=now.year
        ).count(),
    }
    return render(request, 'user_dashboard.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')




from django.shortcuts import render, get_object_or_404
from .models import GallaryItem, PortfolioCategory


def user_portfolio(request):
    # Get all active categories for the filter dropdown
    categories = PortfolioCategory.objects.filter(is_active=True)

    # Get the selected category from request (using slug instead of ID)
    selected_category_slug = request.GET.get('category', 'all')

    # Start with all active gallery items
    gallery_items = GallaryItem.objects.filter(is_active=True).select_related('category')

    # Apply category filter if specified and not 'all'
    if selected_category_slug != 'all':
        # Make sure the category exists and is active
        category = get_object_or_404(PortfolioCategory, slug=selected_category_slug, is_active=True)
        gallery_items = gallery_items.filter(category=category)

    # Optional: Add featured items filter
    featured_only = request.GET.get('featured', 'false').lower() == 'true'
    if featured_only:
        gallery_items = gallery_items.filter(is_featured=True)

    # Order by event date
    gallery_items = gallery_items.order_by('-event_date')

    context = {
        'gallery_items': gallery_items,
        'categories': categories,
        'selected_category_slug': selected_category_slug,
        'featured_only': featured_only,
    }

    return render(request, 'user_portfolio.html', context)


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EventService, Booking
from .forms import BookingForm
from django.urls import reverse

def service_booking(request):
    service_title = request.GET.get('service', '')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            if request.user.is_authenticated:
                booking.user = request.user

            booking.save()

            # Send email
            try:
                send_mail(
                    f'New Booking: {booking.service_name}',
                    f'''New Booking Details:
                    Service: {booking.service_name}
                    Name: {booking.name}
                    Email: {booking.email}
                    Phone: {booking.phone}
                    Date: {booking.event_date}
                    Time: {booking.event_time}
                    Additional Services: {booking.additional_services}
                    Message: {booking.message}''',
                    'noreply@lumora-events.com',
                    ['aswinharidasan6777@gmail.com'],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but don't break the flow
                print(f"Email sending failed: {e}")

            messages.success(request, 'Your booking has been submitted successfully!')
            return redirect(reverse('user_services'))   # Explicitly redirect to user_services

    else:
        initial = {'service_name': service_title}
        form = BookingForm(initial=initial)

    return render(request, 'service_booking.html', {
        'form': form,
        'service_title': service_title
    })


from django.shortcuts import render
from django.http import HttpResponse
from .models import Feedback


def feedback_view(request):
    if request.method == "POST":
        service = request.POST.get("service")
        rating = request.POST.get("rating")
        comments = request.POST.get("comments", "")

        # Validate required fields
        if not all([service, rating]):
            messages.error(request, "Please select a service and rating")
            return redirect('feedback_page')  # Replace with your feedback URL name

        try:
            # Create feedback entry
            Feedback.objects.create(
                service=service,
                rating=rating,
                comments=comments
            )
            messages.success(request, "Feedback submitted successfully!")
            return redirect('feedback_page')  # Replace with your feedback URL name

        except Exception as e:
            messages.error(request, f"Error submitting feedback: {str(e)}")
            return redirect('feedback_page')  # Replace with your feedback URL name

    return render(request, "feedback.html")



def user_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        # Validate form data
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill all required fields')
            return redirect('contact')

        try:
            # Email to admin
            admin_subject = f"New Contact Form: {subject}"
            admin_message = f"""
            Name: {name}
            Email: {email}
            Subject: {subject}
            Message: {message}
            """

            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )

            # Optional: Send confirmation to user
            user_subject = "Thank you for contacting Lumora Events"
            user_message = f"""
            Dear {name},

            Thank you for reaching out to us. We've received your message and will get back to you soon.

            Your message:
            {message}

            Best regards,
            The Lumora Events Team
            """

            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, 'Thank you for your message! We will contact you soon.')
            return redirect('contact')

        except Exception as e:
            messages.error(request, 'An error occurred while sending your message. Please try again later.')
            # Log the error if needed
            # import logging
            # logging.error(f"Contact form error: {str(e)}")
            return redirect('contact')

    return render(request, 'user_contact.html')