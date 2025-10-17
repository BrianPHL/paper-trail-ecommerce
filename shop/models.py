from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import os

def product_image_upload_path(instance, filename):
    """Generate upload path for product images"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Create filename: product_name_id.extension
    filename = f"{instance.name.replace(' ', '_').lower()}_{instance.pk or 'new'}.{ext}"
    return os.path.join('products', filename)

class UserProfile(models.Model):
    """Extend User with additional fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    house_address = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

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
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORIES_CHOICES, default='other')
    image = models.ImageField(
        upload_to=product_image_upload_path, 
        blank=True, 
        null=True,
        help_text="Upload a product image (optional)"
    )
    stock_quantity = models.PositiveIntegerField(default=0, help_text="Number of items in stock")
    is_active = models.BooleanField(default=True, help_text="Whether this product is available for purchase")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def __str__(self):
        return f"{ self.name } - PHP { self.price }"
    
    def get_category_display_name(self):
        """Getter function for category name"""
        return dict(self.CATEGORIES_CHOICES).get(self.category, self.category)
    
    def get_absolute_url(self):
        """Get the URL for this product's detail page"""
        return reverse('product_detail', kwargs={'product_id': self.pk})

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
