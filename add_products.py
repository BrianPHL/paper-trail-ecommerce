import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_trail_ecommerce_project.settings')
django.setup()

from shop.models import Product
from django.core.files import File

# CHANGE THIS PATH to where your images are stored
IMAGES_FOLDER = r"C:\Users\brian\OneDrive\Desktop\paper-trail-ecommerce\shop\static\shop\images"

# Your products data
products = [
    # NOTEBOOKS
    {
        'name': 'Classic Spiral Notebook (A5)',
        'description': 'Durable cover and smooth ruled pages, ideal for class notes or journaling.',
        'price': 45.00,
        'category': 'notebooks',
        'stock_quantity': 50,
        'image_name': 'classicspiralnb.png'
    },
    {
        'name': 'Composition Notebook',
        'description': 'Classic black-and-white marble design with a sturdy cover and sewn binding that keeps pages securely in place.',
        'price': 55.00,
        'category': 'notebooks',
        'stock_quantity': 40,
        'image_name': 'compositionnb.png'
    },
    {
        'name': 'Dot Grid Notebook (A5)',
        'description': 'Features grid pages, great for technical drawings or bullet journaling.',
        'price': 60.00,
        'category': 'notebooks',
        'stock_quantity': 35,
        'image_name': 'dotgridjournalnb.png'
    },
    {
        'name': 'Grid Notebook (A5)',
        'description': 'Features grid pages, great for technical drawings or bullet journaling.',
        'price': 50.00,
        'category': 'notebooks',
        'stock_quantity': 45,
        'image_name': 'gridnb.png'
    },
    {
        'name': 'Hardbound Journal (A6)',
        'description': 'Compact and sturdy notebook with thick paper, perfect for daily reflections.',
        'price': 85.00,
        'category': 'notebooks',
        'stock_quantity': 25,
        'image_name': 'hardboundjournalnb.png'
    },
    {
        'name': 'Mini Pocket Notebook',
        'description': 'Compact design for quick notes and reminders.',
        'price': 30.00,
        'category': 'notebooks',
        'stock_quantity': 60,
        'image_name': 'minipocketnb.png'
    },

    # PENS
    {
        'name': 'Calligraphy Brush Pen Set',
        'description': 'Ideal for hand lettering and creative journaling.',
        'price': 180.00,
        'category': 'pens',
        'stock_quantity': 20,
        'image_name': 'callibrushsetpen.png'
    },
    {
        'name': 'Fine Liner Pen (Black, 0.4mm)',
        'description': 'Precision tip for detailed writing or sketching.',
        'price': 45.00,
        'category': 'pens',
        'stock_quantity': 75,
        'image_name': 'finelinerpen.png'
    },
    {
        'name': 'Multicolor 4-in-1 Pen',
        'description': 'Combines four ink colors in one pen for convenience.',
        'price': 60.00,
        'category': 'pens',
        'stock_quantity': 50,
        'image_name': 'multicolorpen.png'
    },
    {
        'name': 'Retractable Ballpoint Pen (Blue, 1.0mm)',
        'description': 'Easy-click pen for everyday writing.',
        'price': 25.00,
        'category': 'pens',
        'stock_quantity': 100,
        'image_name': 'retballpointpen.png'
    },
    {
        'name': 'Rollerball Pen (Blue, 0.7mm)',
        'description': 'Smooth ink delivery with a classic design.',
        'price': 40.00,
        'category': 'pens',
        'stock_quantity': 80,
        'image_name': 'rollerballpen.png'
    },
    {
        'name': 'Smooth Gel Pen (Black, 0.5mm)',
        'description': 'Quick-drying gel pen with smooth ink flow, great for writing or school use.',
        'price': 25.00,
        'category': 'pens',
        'stock_quantity': 120,
        'image_name': 'smoothgelpen.png'
    },

    # PENCILS
    {
        'name': 'Charcoal Pencil Set',
        'description': 'Rich, deep tones for artistic sketches.',
        'price': 150.00,
        'category': 'pencils',
        'stock_quantity': 30,
        'image_name': 'charcoalpencilset.png'
    },
    {
        'name': 'Colored Pencil Set (12 Colors)',
        'description': 'Smooth pigment for coloring and artwork.',
        'price': 120.00,
        'category': 'pencils',
        'stock_quantity': 40,
        'image_name': 'coloredpencils.png'
    },
    {
        'name': 'Eco Recycled Pencil',
        'description': 'Made from recycled materials, perfect for eco-conscious users.',
        'price': 20.00,
        'category': 'pencils',
        'stock_quantity': 150,
        'image_name': 'ecorecycledpencil.png'
    },
    {
        'name': 'Graphite Sketch Pencil Set (6B–4H)',
        'description': 'Ideal for shading and technical sketches.',
        'price': 130.00,
        'category': 'pencils',
        'stock_quantity': 35,
        'image_name': 'graphitepencil.png'
    },
    {
        'name': 'Mechanical Pencil (0.5mm)',
        'description': 'Refillable pencil with comfortable grip.',
        'price': 45.00,
        'category': 'pencils',
        'stock_quantity': 70,
        'image_name': 'mechpencil.png'
    },
    {
        'name': 'Wooden Pencil (Classic)',
        'description': 'Durable lead pencil for writing and drawing.',
        'price': 10.00,
        'category': 'pencils',
        'stock_quantity': 200,
        'image_name': 'woodenpencil.png'
    },

    # ART MATERIALS
    {
        'name': 'Acrylic Paint Tubes (12 pcs)',
        'description': 'Rich, vibrant colors for canvas and crafts.',
        'price': 220.00,
        'category': 'art_materials',
        'stock_quantity': 25,
        'image_name': 'acrylicpainttubes.png'
    },
    {
        'name': 'Artist Marker Set (24 Colors)',
        'description': 'Dual-tip markers for shading and blending.',
        'price': 350.00,
        'category': 'art_materials',
        'stock_quantity': 15,
        'image_name': 'artistmarkerset.png'
    },
    {
        'name': 'Craft Scissors (Decorative Edge)',
        'description': 'Perfect for paper crafting and scrapbooking.',
        'price': 85.00,
        'category': 'art_materials',
        'stock_quantity': 30,
        'image_name': 'craftscissor.png'
    },
    {
        'name': 'Glue Stick (Large)',
        'description': 'Mess-free adhesive for craft and school projects.',
        'price': 35.00,
        'category': 'art_materials',
        'stock_quantity': 80,
        'image_name': 'gluestick.png'
    },
    {
        'name': 'Oil Pastel Set (36 Colors)',
        'description': 'Creamy texture for vibrant artwork.',
        'price': 180.00,
        'category': 'art_materials',
        'stock_quantity': 20,
        'image_name': 'oilpastelset.png'
    },
    {
        'name': 'Paintbrush Set (10 pcs)',
        'description': 'Various brush sizes for detailed or broad strokes.',
        'price': 120.00,
        'category': 'art_materials',
        'stock_quantity': 35,
        'image_name': 'paintbrushset.png'
    },
    {
        'name': 'Palette Mixing Tray',
        'description': 'Durable plastic tray for mixing paints easily.',
        'price': 40.00,
        'category': 'art_materials',
        'stock_quantity': 50,
        'image_name': 'palettetray.png'
    },
    {
        'name': 'Sketch Pad (A4)',
        'description': 'Thick paper ideal for pencil, ink, and charcoal sketches.',
        'price': 90.00,
        'category': 'art_materials',
        'stock_quantity': 40,
        'image_name': 'sketchpad.png'
    },
    {
        'name': 'Watercolor Paint Set (24 Colors)',
        'description': 'High-quality pigments for smooth blending.',
        'price': 220.00,
        'category': 'art_materials',
        'stock_quantity': 25,
        'image_name': 'watercolorpaintset.png'
    },

    # PAPERS
    {
        'name': 'Colored Paper Set (A4, 10 Colors)',
        'description': 'Bright and assorted colors for crafts.',
        'price': 70.00,
        'category': 'papers',
        'stock_quantity': 60,
        'image_name': 'coloredpaperset.png'
    },
    {
        'name': 'Graph Paper (A4)',
        'description': 'Ideal for mathematics and engineering drawings.',
        'price': 30.00,
        'category': 'papers',
        'stock_quantity': 100,
        'image_name': 'graphpaper.png'
    },
    {
        'name': 'Long Bond Paper (500 Sheets)',
        'description': 'Standard paper for printing and writing.',
        'price': 180.00,
        'category': 'papers',
        'stock_quantity': 80,
        'image_name': 'longbondpapers.png'
    },
    {
        'name': 'Origami Paper (Double-Sided)',
        'description': 'Colorful sheets for paper folding crafts.',
        'price': 90.00,
        'category': 'papers',
        'stock_quantity': 45,
        'image_name': 'origamipaper.png'
    },
    {
        'name': 'Photo Paper (Glossy A4)',
        'description': 'High-quality print paper for vivid images.',
        'price': 150.00,
        'category': 'papers',
        'stock_quantity': 30,
        'image_name': 'photopaper.png'
    },
    {
        'name': 'Sticky Notes (Assorted Colors)',
        'description': 'Repositionable notes for reminders.',
        'price': 50.00,
        'category': 'papers',
        'stock_quantity': 90,
        'image_name': 'stickynotes.png'
    },
]

# Create the products
created_count = 0
skipped_count = 0
for item in products:
    try:
        # Check if product already exists (by name)
        if Product.objects.filter(name=item['name']).exists():
            print(f"⏭️  Skipped '{item['name']}' - already exists")
            skipped_count += 1
            continue
        
        # Remove image_name from product data
        image_name = item.pop('image_name', None)
        
        # Create product
        product = Product.objects.create(
            name=item['name'],
            description=item['description'],
            price=Decimal(str(item['price'])),
            category=item['category'],
            stock_quantity=item['stock_quantity']
        )
        
        # Add image if exists
        if image_name:
            image_path = os.path.join(IMAGES_FOLDER, image_name)
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    product.image.save(image_name, File(f), save=True)
                print(f"✅ Created '{product.name}' with image")
            else:
                print(f"⚠️  Created '{product.name}' but no image found: {image_name}")
        else:
            print(f"✅ Created '{product.name}' without image")
        
        created_count += 1
            
    except Exception as e:
        print(f"❌ Error with '{item['name']}': {e}")

print(f"\n🎉 Done! Created {created_count} new products, skipped {skipped_count} existing products.")
