"""
Script to seed the database with sample products
Run this once to populate your database with test data
"""
from database.db_manager import DatabaseManager
from config import Config

def seed_database():
    db = DatabaseManager()
    
    sample_products = [
        {
            'name': 'Oversized White Tee',
            'brand': 'Zara',
            'price': 29.90,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.zara.com/example',
            'sizes': ['XS', 'S', 'M', 'L', 'XL'],
            'colors': ['White', 'Cream', 'Beige'],
            'styles': 'minimal, clean girl, modern, casual, oversized, white t-shirt',
            'category': 'Tops',
            'description': 'Classic oversized white t-shirt perfect for the clean girl aesthetic'
        },
        {
            'name': 'High-Waisted Mom Jeans',
            'brand': 'H&M',
            'price': 39.99,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.hm.com/example',
            'sizes': ['2', '4', '6', '8', '10', '12', '14'],
            'colors': ['Light Blue', 'Medium Wash', 'Black'],
            'styles': 'casual, clean girl, denim, high-waisted jeans, vintage',
            'category': 'Bottoms',
            'description': 'High-waisted mom jeans with vintage wash'
        },
        {
            'name': 'Oversized Blazer',
            'brand': 'Zara',
            'price': 89.90,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.zara.com/example',
            'sizes': ['XS', 'S', 'M', 'L', 'XL'],
            'colors': ['Beige', 'Black', 'Navy'],
            'styles': 'minimal, clean, modern, professional, elegant, oversized',
            'category': 'Outerwear',
            'description': 'A timeless oversized blazer perfect for professional and casual looks'
        },
        {
            'name': 'Linen Midi Dress',
            'brand': 'Reformation',
            'price': 148.00,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.thereformation.com/example',
            'sizes': ['0', '2', '4', '6', '8', '10'],
            'colors': ['White', 'Cream', 'Light Blue'],
            'styles': 'clean, minimal, romantic, soft, feminine, flowy dress',
            'category': 'Dresses',
            'description': 'Breathable linen midi dress with a relaxed fit'
        },
        {
            'name': 'Cropped Cardigan',
            'brand': 'Reformation',
            'price': 78.00,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.thereformation.com/example',
            'sizes': ['XS', 'S', 'M', 'L'],
            'colors': ['Sage', 'Cream', 'Lavender'],
            'styles': 'cottagecore, romantic, vintage, soft, feminine, cozy, cardigan',
            'category': 'Tops',
            'description': 'Soft cropped cardigan with pearl buttons'
        },
        {
            'name': 'Wide Leg Trousers',
            'brand': 'Madewell',
            'price': 128.00,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.madewell.com/example',
            'sizes': ['0', '2', '4', '6', '8', '10', '12', '14'],
            'colors': ['Black', 'Navy', 'Cream'],
            'styles': 'classic, elegant, professional, clean, minimal, timeless, pants',
            'category': 'Bottoms',
            'description': 'High-waisted wide leg trousers with pleats'
        },
        {
            'name': 'Puff Sleeve Blouse',
            'brand': '& Other Stories',
            'price': 69.00,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.stories.com/example',
            'sizes': ['2', '4', '6', '8', '10', '12'],
            'colors': ['White', 'Pink', 'Yellow'],
            'styles': 'romantic, feminine, cottagecore, vintage, soft, floral, blouse',
            'category': 'Tops',
            'description': 'Romantic blouse with puff sleeves and tie neck'
        },
        {
            'name': 'Minimalist Tote Bag',
            'brand': 'Everlane',
            'price': 165.00,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.everlane.com/example',
            'sizes': ['One Size'],
            'colors': ['Black', 'Tan', 'Cognac'],
            'styles': 'minimal, clean, timeless, professional, elegant, simple, bag',
            'category': 'Accessories',
            'description': 'Italian leather tote with clean lines'
        },
        {
            'name': 'Ribbed Knit Set',
            'brand': 'Eileen Fisher',
            'price': 198.00,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.eileenfisher.com/example',
            'sizes': ['XS', 'S', 'M', 'L', 'XL'],
            'colors': ['Oatmeal', 'Charcoal', 'Navy'],
            'styles': 'minimal, clean, cozy, soft, timeless, elegant, knit',
            'category': 'Sets',
            'description': 'Matching ribbed knit top and pants set'
        },
        {
            'name': 'Denim Jacket',
            'brand': 'Patagonia',
            'price': 119.00,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.patagonia.com/example',
            'sizes': ['XS', 'S', 'M', 'L', 'XL'],
            'colors': ['Light Wash', 'Medium Wash', 'Dark Wash'],
            'styles': 'casual, classic, timeless, versatile, outdoor, durable, jacket',
            'category': 'Outerwear',
            'description': 'Sustainable denim jacket with organic cotton'
        },
        {
            'name': 'Floral Maxi Dress',
            'brand': 'Reformation',
            'price': 218.00,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.thereformation.com/example',
            'sizes': ['0', '2', '4', '6', '8', '10', '12'],
            'colors': ['Floral Print', 'Pastel'],
            'styles': 'boho, bohemian, romantic, cottagecore, floral, maxi dress, feminine',
            'category': 'Dresses',
            'description': 'Flowy floral maxi dress perfect for boho chic style'
        },
        {
            'name': 'Leather Jacket',
            'brand': 'Zara',
            'price': 149.90,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.zara.com/example',
            'sizes': ['XS', 'S', 'M', 'L', 'XL'],
            'colors': ['Black', 'Brown'],
            'styles': 'edgy, streetwear, modern, cool, leather jacket, urban',
            'category': 'Outerwear',
            'description': 'Classic leather jacket with silver hardware'
        },
        {
            'name': 'Slip Dress',
            'brand': 'Reformation',
            'price': 158.00,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.thereformation.com/example',
            'sizes': ['0', '2', '4', '6', '8', '10'],
            'colors': ['Black', 'Champagne', 'Emerald'],
            'styles': 'elegant, minimal, clean girl, feminine, silky, slip dress',
            'category': 'Dresses',
            'description': 'Silky slip dress with adjustable straps'
        },
        {
            'name': 'Cargo Pants',
            'brand': 'H&M',
            'price': 44.99,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.hm.com/example',
            'sizes': ['2', '4', '6', '8', '10', '12', '14'],
            'colors': ['Olive', 'Black', 'Khaki'],
            'styles': 'streetwear, urban, casual, cargo pants, utility, trendy',
            'category': 'Bottoms',
            'description': 'Utility cargo pants with multiple pockets'
        },
        {
            'name': 'Cashmere Sweater',
            'brand': 'Everlane',
            'price': 130.00,
            'currency': 'USD',
            'image_url': '/placeholder.svg?height=400&width=300',
            'product_url': 'https://www.everlane.com/example',
            'sizes': ['XS', 'S', 'M', 'L', 'XL'],
            'colors': ['Cream', 'Grey', 'Navy', 'Camel'],
            'styles': 'minimal, clean, timeless, cozy, elegant, cashmere, sweater',
            'category': 'Tops',
            'description': 'Luxurious cashmere crewneck sweater'
        }
    ]
    
    print("Starting database seeding...")
    for product in sample_products:
        product_id = db.insert_product(product)
        print(f"✓ Inserted: {product['name']} - {product['brand']} (ID: {product_id})")
    
    print(f"\n✓ Successfully seeded {len(sample_products)} products!")
    print(f"Database path: {Config.DATABASE_PATH}")

if __name__ == '__main__':
    seed_database()
