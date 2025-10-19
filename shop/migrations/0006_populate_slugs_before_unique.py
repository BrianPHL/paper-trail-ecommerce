from django.db import migrations
from django.utils.text import slugify


def generate_unique_slugs(apps, schema_editor):
    """Generate unique slugs for all existing products"""
    Product = apps.get_model('shop', 'Product')
    
    for product in Product.objects.all():
        if not product.slug:
            base_slug = slugify(product.name)
            slug = base_slug
            counter = 1
            
            # Ensure slug is unique
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            product.slug = slug
            product.save(update_fields=['slug'])
    
    print(f"Generated slugs for {Product.objects.count()} products")


def reverse_slugs(apps, schema_editor):
    """Reverse operation: clear all slugs"""
    Product = apps.get_model('shop', 'Product')
    Product.objects.all().update(slug=None)


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_product_is_bestseller_product_is_featured_and_more'),
    ]

    operations = [
        migrations.RunPython(generate_unique_slugs, reverse_slugs),
    ]
