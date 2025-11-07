from django.contrib import admin
from django.db.models import Sum, Count, Avg, F
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from datetime import date, timedelta
from .models import UserProfile, Product, Cart, CartItem, Order, OrderItem, Feedback, InventoryTransaction, Address

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

# INVENTORY MANAGEMENT
@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'product', 'transaction_type', 'quantity_change_display', 'stock_before', 'stock_after', 'order_link', 'created_by')
    list_filter = ('transaction_type', 'created_at', 'product__category')
    search_fields = ('product__name', 'order__id', 'notes', 'created_by__username')
    readonly_fields = ('created_at', 'stock_before', 'stock_after')
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('product', 'transaction_type', 'quantity_change')
        }),
        ('Stock Information', {
            'fields': ('stock_before', 'stock_after')
        }),
        ('Related Information', {
            'fields': ('order', 'notes', 'created_by', 'created_at')
        }),
    )
    
    @admin.display(description="Quantity Change")
    def quantity_change_display(self, obj):
        color = 'green' if obj.quantity_change > 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:+d}</span>',
            color, obj.quantity_change
        )
    
    @admin.display(description="Order")
    def order_link(self, obj):
        if obj.order:
            from django.urls import reverse
            url = reverse('admin:shop_order_change', args=[obj.order.id])
            return format_html('<a href="{}">Order #{}</a>', url, obj.order.id)
        return '-'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('inventory-dashboard/', self.admin_site.admin_view(self.inventory_dashboard), name='inventory-dashboard'),
        ]
        return custom_urls + urls
    
    def inventory_dashboard(self, request):
        """Inventory Management Dashboard"""
        from django.db.models import Q
        from datetime import datetime, timedelta
        
        # Low stock products (5 or less)
        low_stock_products = Product.objects.filter(
            stock_quantity__lte=5,
            is_active=True
        ).order_by('stock_quantity')
        
        # Out of stock products
        out_of_stock = Product.objects.filter(
            stock_quantity=0,
            is_active=True
        ).count()
        
        # Recent transactions (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_transactions = InventoryTransaction.objects.filter(
            created_at__gte=thirty_days_ago
        ).select_related('product', 'order', 'created_by').order_by('-created_at')[:50]
        
        # Stock movement by transaction type (last 30 days)
        stock_movement = InventoryTransaction.objects.filter(
            created_at__gte=thirty_days_ago
        ).values('transaction_type').annotate(
            total_quantity=Sum('quantity_change'),
            transaction_count=Count('id')
        ).order_by('-transaction_count')
        
        # Top selling products (by quantity)
        top_selling = InventoryTransaction.objects.filter(
            transaction_type='sale',
            created_at__gte=thirty_days_ago
        ).values('product__name', 'product__id').annotate(
            total_sold=Sum('quantity_change')
        ).order_by('total_sold')[:10]  # Most negative = most sold
        
        # Total inventory value
        from django.db.models import F, DecimalField
        from django.db.models.functions import Coalesce
        total_inventory_value = Product.objects.aggregate(
            total=Sum(F('stock_quantity') * F('price'), output_field=DecimalField())
        )['total'] or 0
        
        # Products needing restock
        products_needing_restock = Product.objects.filter(
            Q(stock_quantity__lte=10) & Q(is_active=True)
        ).count()
        
        context = dict(
            self.admin_site.each_context(request),
            low_stock_products=low_stock_products,
            out_of_stock_count=out_of_stock,
            recent_transactions=recent_transactions,
            stock_movement=stock_movement,
            top_selling=top_selling,
            total_inventory_value=total_inventory_value,
            products_needing_restock=products_needing_restock,
            title="Inventory Management Dashboard"
        )
        
        return render(request, 'admin/inventory_dashboard.html', context)

# Update OrderAdmin to show inventory impact
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'total_amount', 'shipping_fee', 'status', 'placed_at', 'user')
    search_fields = ('full_name', 'email', 'address', 'user__username')
    list_filter = ('status', 'payment_method', 'placed_at')
    readonly_fields = ('placed_at', 'inventory_impact_display')
    list_editable = ('status',)
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'user', 'full_name', 'email', 'address')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'total_amount', 'shipping_fee', 'status')
        }),
        ('Timestamps', {
            'fields': ('placed_at',)
        }),
        ('Inventory Impact', {
            'fields': ('inventory_impact_display',),
            'description': 'Stock changes caused by this order'
        })
    )
    
    @admin.display(description="Inventory Impact")
    def inventory_impact_display(self, obj):
        transactions = obj.inventory_transactions.all().select_related('product')
        if not transactions:
            return format_html('<em>No inventory changes recorded</em>')
        
        html = '<table style="width:100%; border-collapse: collapse;">'
        html += '<tr style="background: #f0f0f0;"><th style="padding:8px; text-align:left;">Product</th><th style="padding:8px; text-align:center;">Qty Change</th><th style="padding:8px; text-align:center;">Stock Before</th><th style="padding:8px; text-align:center;">Stock After</th></tr>'
        
        for trans in transactions:
            html += f'<tr><td style="padding:8px; border-top:1px solid #ddd;">{trans.product.name}</td>'
            html += f'<td style="padding:8px; border-top:1px solid #ddd; text-align:center; color:red; font-weight:bold;">{trans.quantity_change:+d}</td>'
            html += f'<td style="padding:8px; border-top:1px solid #ddd; text-align:center;">{trans.stock_before}</td>'
            html += f'<td style="padding:8px; border-top:1px solid #ddd; text-align:center;">{trans.stock_after}</td></tr>'
        
        html += '</table>'
        return format_html(html)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('order-history/', self.admin_site.admin_view(self.order_history_view), name='order-history'),
        ]
        return custom_urls + urls
    
    def order_history_view(self, request):
        """Complete order history with analytics"""
        from datetime import datetime, timedelta
        
        # All orders
        all_orders = Order.objects.all().select_related('user').prefetch_related('items__product').order_by('-placed_at')
        
        # Order statistics
        total_orders = all_orders.count()
        total_revenue = all_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # Orders by status
        orders_by_status = all_orders.values('status').annotate(
            count=Count('id'),
            revenue=Sum('total_amount')
        ).order_by('-count')
        
        # Recent orders (last 50)
        recent_orders = all_orders[:50]
        
        # Monthly breakdown (last 12 months)
        from django.db.models.functions import TruncMonth
        monthly_orders = all_orders.annotate(
            month=TruncMonth('placed_at')
        ).values('month').annotate(
            orders=Count('id'),
            revenue=Sum('total_amount')
        ).order_by('-month')[:12]
        
        # Top customers
        top_customers = all_orders.filter(user__isnull=False).values(
            'user__username', 'user__email'
        ).annotate(
            order_count=Count('id'),
            total_spent=Sum('total_amount')
        ).order_by('-total_spent')[:10]
        
        context = dict(
            self.admin_site.each_context(request),
            recent_orders=recent_orders,
            total_orders=total_orders,
            total_revenue=total_revenue,
            orders_by_status=orders_by_status,
            monthly_orders=monthly_orders,
            top_customers=top_customers,
            title="Order History & Analytics"
        )
        
        return render(request, 'admin/order_history.html', context)

# Update ProductAdmin to show inventory transactions
class ProductAdmin(admin.ModelAdmin):
    # ... (keep existing fields)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales-analytics/', self.admin_site.admin_view(self.sales_analytics_view), name='sales-analytics'),
            path('<int:product_id>/inventory-history/', self.admin_site.admin_view(self.product_inventory_history), name='product-inventory-history'),
        ]
        return custom_urls + urls
    
    def product_inventory_history(self, request, product_id):
        """Show inventory history for a specific product"""
        product = Product.objects.get(id=product_id)
        transactions = product.inventory_transactions.all().select_related('order', 'created_by').order_by('-created_at')
        
        context = dict(
            self.admin_site.each_context(request),
            product=product,
            transactions=transactions,
            title=f"Inventory History: {product.name}"
        )
        
        return render(request, 'admin/product_inventory_history.html', context)

# LINK EXTENSION FOR CUSTOM ADMIN 
admin.site.index_template = 'admin/custom_index.html'