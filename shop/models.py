from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import os

def product_image_upload_path(instance, filename):
    """Generate upload path for product images"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Create filename: product_name_id.extension
    filename = f"{instance.name.replace(' ', '_').lower()}_{instance.pk or 'new'}.{ext}"
    return os.path.join('products', filename)

def profile_picture_upload_path(instance, filename):
    """Generate upload path for user profile pictures"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Create filename: user_id_profile.extension
    filename = f"user_{instance.user.id}_profile.{ext}"
    return os.path.join('profiles', filename)

class UserProfile(models.Model):
    """Extend User with additional fields"""
    
    CURRENCY_CHOICES = [
        ('PHP', 'Philippine Peso (₱)'),
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('CREDIT_CARD', 'Credit Card'),
        ('PAYPAL', 'PayPal'),
        ('GCASH', 'GCash'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    house_address = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(
        upload_to=profile_picture_upload_path,
        blank=True,
        null=True,
        help_text="Upload a profile picture"
    )
    preferred_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='PHP',
        help_text="Preferred currency for pricing"
    )
    preferred_payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='COD',
        help_text="Preferred payment method"
    )
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    @property
    def profile_picture_url(self):
        """Get the profile picture URL or return None"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return None

class Address(models.Model):
    """Address model for user addresses"""
    
    ADDRESS_TYPE_CHOICES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]
    
    COUNTRY_CHOICES = [
        ('Philippines', 'Philippines'),
        ('United States', 'United States'),
        ('Canada', 'Canada'),
        ('United Kingdom', 'United Kingdom'),
        ('Australia', 'Australia'),
        ('Japan', 'Japan'),
        ('South Korea', 'South Korea'),
        ('Singapore', 'Singapore'),
        ('Malaysia', 'Malaysia'),
        ('Thailand', 'Thailand'),
        ('Indonesia', 'Indonesia'),
        ('Vietnam', 'Vietnam'),
        ('India', 'India'),
        ('China', 'China'),
        ('Hong Kong', 'Hong Kong'),
        ('Taiwan', 'Taiwan'),
        ('Germany', 'Germany'),
        ('France', 'France'),
        ('Italy', 'Italy'),
        ('Spain', 'Spain'),
        ('Netherlands', 'Netherlands'),
        ('Belgium', 'Belgium'),
        ('Switzerland', 'Switzerland'),
        ('Austria', 'Austria'),
        ('Sweden', 'Sweden'),
        ('Norway', 'Norway'),
        ('Denmark', 'Denmark'),
        ('Finland', 'Finland'),
        ('Brazil', 'Brazil'),
        ('Mexico', 'Mexico'),
        ('Argentina', 'Argentina'),
        ('Chile', 'Chile'),
        ('Colombia', 'Colombia'),
        ('Peru', 'Peru'),
        ('New Zealand', 'New Zealand'),
        ('South Africa', 'South Africa'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Israel', 'Israel'),
        ('Turkey', 'Turkey'),
        ('Russia', 'Russia'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=100, help_text="Address label (e.g., Home, Work)")
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES, default='home')
    street_address = models.CharField(max_length=255, help_text="Street address")
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, help_text="State/Province")
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, default='Philippines')
    is_default = models.BooleanField(default=False, help_text="Set as default address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.label}"
    
    def save(self, *args, **kwargs):
        # If this address is set as default, make sure no other address for this user is default
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
    
    @property
    def full_address(self):
        """Return the full formatted address"""
        return f"{self.street_address}, {self.city}, {self.state_province} {self.postal_code}, {self.country}"

class Product(models.Model):
    """Product model with category"""

    CATEGORIES_CHOICES = [
        ('notebooks', 'Notebooks'),
        ('pens', 'Pens'),
        ('pencils', 'Pencils'),
        ('art_materials', 'Art Materials'),
        ('papers', 'Papers'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True, help_text="URL-friendly version of the product name (auto-generated)")
    description = models.TextField()
    image = models.ImageField(
        upload_to=product_image_upload_path, 
        blank=True, 
        null=True,
        help_text="Upload a product image (optional)"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORIES_CHOICES, default='other')
    weight = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Weight in grams (g)"
    )
    dimensions = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Product dimensions (e.g., '21cm x 14.8cm' or '15cm L x 10cm W x 2cm H')"
    )
    stock_quantity = models.PositiveIntegerField(default=0, help_text="Number of items in stock")
    is_active = models.BooleanField(default=True, help_text="Whether this product is available for purchase")
    is_featured = models.BooleanField(default=False, help_text="Mark as featured product (shown on homepage)")
    is_bestseller = models.BooleanField(default=False, help_text="Mark as bestseller")
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def __str__(self):
        return f"{ self.name } - PHP { self.price }"
    
    def save(self, *args, **kwargs):
        """Override save to auto-generate slug"""
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            
            # Ensure slug is unique
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)
    
    def get_category_display_name(self):
        """Getter function for category name"""
        return dict(self.CATEGORIES_CHOICES).get(self.category, self.category)
    
    def get_absolute_url(self):
        """Get the URL for this product's detail page"""
        return reverse('pdp', kwargs={'slug': self.slug})

    @property
    def image_url(self):
        """Get the image URL or return a placeholder"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/shop/images/placeholder-product.jpg'
    
    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock_quantity > 0 and self.is_active
    
    @property
    def stock_status(self):
        """Get stock status as a string"""
        if not self.is_active:
            return "Discontinued"
        elif self.stock_quantity == 0:
            return "Out of Stock"
        elif self.stock_quantity <= 5:
            return "Low Stock"
        else:
            return "In Stock"
    
    @property
    def is_new_arrival(self):
        """Check if product is a new arrival (added within last 30 days)"""
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at >= timezone.now() - timedelta(days=30)
