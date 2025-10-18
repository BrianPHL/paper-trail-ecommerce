from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import UserProfile, Product

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price', 'stock_quantity', 'stock_status_display', 'is_active', 'image_preview', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'slug')
    readonly_fields = ('slug', 'created_at', 'modified_at', 'image_preview', 'stock_status_display')
    list_per_page = 25
    list_editable = ('price', 'stock_quantity', 'is_active')
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate slug from name in admin
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category', 'price')
        }),
        ('Stock & Availability', {
            'fields': ('stock_quantity', 'is_active', 'stock_status_display')
        }),
        ('Product Details', {
            'fields': ('weight', 'dimensions'),
            'classes': ('collapse',)
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload a product image'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',)
        })
    )
    
    @admin.display(description="Image Preview")
    def image_preview(self, obj):
        """Show image preview in admin"""
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return format_html('<div style="width:100px;height:100px;background:#f0f0f0;border-radius:4px;display:flex;align-items:center;justify-content:center;color:#666;">No image</div>')
    
    @admin.display(description="Stock Status")
    def stock_status_display(self, obj):
        """Display stock status with color coding"""
        status = obj.stock_status
        colors = {
            'In Stock': 'green',
            'Low Stock': 'orange', 
            'Out of Stock': 'red',
            'Discontinued': 'gray'
        }
        color = colors.get(status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
