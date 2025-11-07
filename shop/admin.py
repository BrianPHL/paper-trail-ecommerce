from django.contrib import admin
from django.db.models import Sum, Count, Avg
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from datetime import date, timedelta
from .models import UserProfile, Product, Cart, CartItem, Order, OrderItem

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]

# P R O D U C T S
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price', 'stock_quantity', 'is_featured', 'is_bestseller', 'stock_status_display', 'is_active', 'image_preview', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured', 'is_bestseller', 'created_at')
    search_fields = ('name', 'description', 'slug')
    readonly_fields = ('slug', 'created_at', 'modified_at', 'image_preview', 'stock_status_display')
    list_per_page = 25
    list_editable = ('price', 'stock_quantity', 'is_active', 'is_featured', 'is_bestseller')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category', 'price')
        }),
        ('Stock & Availability', {
            'fields': ('stock_quantity', 'is_active', 'stock_status_display')
        }),
        ('Marketing & Display', {
            'fields': ('is_featured', 'is_bestseller'),
            'description': 'Control how this product appears on the homepage'
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
    # methods for sales analytics
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales-analytics/', self.admin_site.admin_view(self.sales_analytics_view), name='sales-analytics'),
        ]
        return custom_urls + urls
    
    def sales_analytics_view(self, request):
        # Calculate analytics
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        completed_orders = Order.objects.filter(status='completed').count()
        pending_orders = Order.objects.filter(status='pending').count()
        cancelled_orders = Order.objects.filter(status='cancelled').count()
        
        # Top products
        top_products = OrderItem.objects.values('product__name').annotate(
            total_sold=Sum('quantity'),
            revenue=Sum('price')
        ).order_by('-total_sold')[:10]

        # Bottom products (least sold)
        bottom_products = OrderItem.objects.values('product__name').annotate(
             total_sold=Sum('quantity'),
             revenue=Sum('price')
        ).order_by('total_sold')[:10]
        
        # Monthly sales filter
        current_year = date.today().year
        selected_month = request.GET.get('month')
        
        if selected_month:
            try:
                year, month = map(int, selected_month.split('-'))
                start_date = date(year, month, 1)
                if month == 12:
                    end_date = date(year + 1, 1, 1) - timedelta(days=1)
                else:
                    end_date = date(year, month + 1, 1) - timedelta(days=1)
                
                filtered_sales = Order.objects.filter(
                    placed_at__date__range=(start_date, end_date)
                ).aggregate(
                    orders=Count('id'),
                    revenue=Sum('total_amount')
                )
                monthly_sales = [{
                    'month': start_date,
                    'orders': filtered_sales['orders'] or 0,
                    'revenue': filtered_sales['revenue'] or 0
                }]
            except ValueError:
                monthly_sales = []  # Invalid month, show nothing
        else:
            # Default: last 12 months
            from django.db.models.functions import TruncMonth
            monthly_sales = Order.objects.filter(status='completed').annotate(
                month=TruncMonth('placed_at')
            ).values('month').annotate(
                orders=Count('id'),
                revenue=Sum('total_amount')
            ).order_by('-month')[:12]
        
        # Generate month options (January to December of current year)
        month_options = []
        for month in range(1, 13):
            month_date = date(current_year, month, 1)
            month_options.append({
                'value': month_date.strftime('%Y-%m'),
                'label': month_date.strftime('%B %Y')
            })
        
        context = dict(
            self.admin_site.each_context(request),
            total_orders=total_orders,
            total_revenue=total_revenue,
            completed_orders=completed_orders,
            pending_orders=pending_orders,
            cancelled_orders=cancelled_orders,
            top_products=top_products,
            bottom_products=bottom_products,
            monthly_sales=monthly_sales,
            month_options=month_options,
            selected_month=selected_month,
        )
        return render(request, 'admin/sales_analytics.html', context)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)

# C A R T 
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'is_active', 'created_at', 'updated_at')
    search_fields = ('user__username', 'session_key')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'price', 'created_at')
    search_fields = ('product__name',)
    readonly_fields = ('created_at', 'updated_at')


# O R D E R S
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price', 'total_price')
    can_delete = False
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'total_amount', 'status', 'placed_at')
    list_filter = ('status', 'placed_at', 'payment_method')
    search_fields = ('full_name', 'email', 'id')
    readonly_fields = ('placed_at', 'user')
    list_editable = ('status',)  # Allow editing status directly in the list view
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'full_name', 'email', 'address', 'payment_method', 'status')
        }),
        ('Pricing', {
            'fields': ('total_amount', 'shipping_fee')
        }),
        ('Timestamps', {
            'fields': ('placed_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total_price')
    list_filter = ('order__status', 'product')
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('total_price',)

from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'category', 'subject', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'name', 'email')
        }),
        ('Feedback Details', {
            'fields': ('category', 'subject', 'message', 'status')
        }),
        ('Admin', {
            'fields': ('admin_notes', 'created_at', 'updated_at')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('user', 'name', 'email', 'category', 'subject', 'message')
        return self.readonly_fields
    
    actions = ['mark_as_read', 'mark_as_archived']
    
    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
        self.message_user(request, f'{queryset.count()} feedback(s) marked as read.')
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_archived(self, request, queryset):
        queryset.update(status='archived')
        self.message_user(request, f'{queryset.count()} feedback(s) archived.')
    mark_as_archived.short_description = 'Archive selected'

# LINK EXTENSION FOR CUSTOM ADMIN 
admin.site.index_template = 'admin/custom_index.html'