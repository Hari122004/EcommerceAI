import json
from pathlib import Path

path = Path('assets/sample_products.json')
products = json.loads(path.read_text(encoding='utf-8'))
category_images = {
    'Electronics': [
        'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1512499617640-c2f99922cc54?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1501889088092-3f0ca44d3f74?auto=format&fit=crop&w=800&q=80',
    ],
    'Home & Kitchen': [
        'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1494965128831-5d52f4b664c6?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=800&q=80',
    ],
    'Beauty & Personal Care': [
        'https://images.unsplash.com/photo-1512418490979-92798cec0f55?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1517686469429-8f52cf9f24a7?auto=format&fit=crop&w=800&q=80',
    ],
    'Clothing & Shoes': [
        'https://images.unsplash.com/photo-1520975911842-20cb635af552?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1520614073990-dd6022f6a99f?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80',
    ],
}

def pick_image(prod):
    images = category_images.get(prod.get('category'))
    if not images:
        return 'https://images.unsplash.com/photo-1510557880182-3c5ed1d4dbc8?auto=format&fit=crop&w=800&q=80'
    try:
        numeric = ''.join(ch for ch in prod.get('product_id', '') if ch.isdigit())
        idx = int(numeric) if numeric else 0
    except ValueError:
        idx = 0
    return images[idx % len(images)]

for prod in products:
    prod['image_url'] = pick_image(prod)

path.write_text(json.dumps(products, indent=4, ensure_ascii=False), encoding='utf-8')
print(f'Updated {len(products)} products to fixed image URLs.')
