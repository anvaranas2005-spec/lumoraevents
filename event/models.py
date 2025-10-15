from django.db import models
from django.utils.html import mark_safe


class Service(models.Model):
    PRICE_CHOICES = [
        ('FIXED', 'Fixed Price'),
        ('HOURLY', 'Hourly Rate'),
        ('CUSTOM', 'Custom Quote'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(
        max_length=50,
        help_text="Name of the icon from your icon library (e.g., 'fa-calendar')"
    )
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_type = models.CharField(
        max_length=10,
        choices=PRICE_CHOICES,
        default='FIXED',
        help_text="How the price is calculated"
    )
    show_button = models.BooleanField(
        default=True,
        help_text="Whether to display the action button for this service"
    )
    button_text = models.CharField(
        max_length=30,
        default="Get Started",
        help_text="Text to display on the button"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title

    def display_price(self):
        if not self.price:
            return "Contact for pricing"

        if self.price_type == 'FIXED':
            return f"₹{self.price:,.2f}"
        elif self.price_type == 'HOURLY':
            return f"₹{self.price:,.2f}/hour"
        else:
            return "Custom Quote"

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')
        return "No Image"

    image_tag.short_description = 'Image Preview'


class PortfolioCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Portfolio Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class PortfolioItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(PortfolioCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio/')
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="150" style="object-fit: cover;" />')
        return "No Image"
    image_tag.short_description = 'Image Preview'


from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.password_hash:
            self.password_hash = make_password(self.user.password)
        super().save(*args, **kwargs)


from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()  # Django stores this as timezone-aware if USE_TZ=True
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add is timezone-aware

    def __str__(self):
        return self.title


from django.db import models
from django.utils.safestring import mark_safe


class GallaryItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(PortfolioCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_portfolio/')
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="150" style="object-fit: cover;" />')
        return "No Image"
    image_tag.short_description = 'Image Preview'



class EventService(models.Model):
    PRICE_CHOICES = [
        ('FIXED', 'Fixed Price'),
        ('HOURLY', 'Hourly Rate'),
        ('CUSTOM', 'Custom Quote'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(
        max_length=50,
        help_text="Name of the icon from your icon library (e.g., 'fa-calendar')"
    )
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_type = models.CharField(
        max_length=10,
        choices=PRICE_CHOICES,
        default='FIXED',
        help_text="How the price is calculated"
    )
    show_button = models.BooleanField(
        default=True,
        help_text="Whether to display the action button for this service"
    )
    button_text = models.CharField(
        max_length=30,
        default="Get Started",
        help_text="Text to display on the button"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Event Service"
        verbose_name_plural = "Event Service"

    def __str__(self):
        return self.title

    def display_price(self):
        if not self.price:
            return "Contact for pricing"

        if self.price_type == 'FIXED':
            return f"₹{self.price:,.2f}"
        elif self.price_type == 'HOURLY':
            return f"₹{self.price:,.2f}/hour"
        else:
            return "Custom Quote"

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')
        return "No Image"

    image_tag.short_description = 'Image Preview'


class Booking(models.Model):
    SERVICE_CHOICES = [
        ('photography', 'Photography'),
        ('videography', 'Videography'),
        ('catering', 'Catering'),
        ('decoration', 'Decoration'),
        ('music', 'Music & Entertainment'),
    ]

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    service_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_date = models.DateField()
    event_time = models.TimeField()
    additional_services = models.CharField(
        max_length=255,
        blank=True,
        choices=SERVICE_CHOICES
    )
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking for {self.service_name} by {self.name}"


class Feedback(models.Model):
    SERVICE_CHOICES = [
        ("portfolio_experience", "Portfolio Experience"),
        ("service_experience", "Service Experience"),
        ("overall_experience", "Overall Experience"),
    ]

    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    rating = models.IntegerField()
    comments = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_service_display()} - {self.rating} Stars"