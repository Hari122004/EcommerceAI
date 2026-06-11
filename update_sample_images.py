import json
from pathlib import Path

repo_path = Path('assets/sample_products.json')
download_path = Path('c:/Users/jagad/Downloads/sample_products_real_images.json')

repo_data = json.loads(repo_path.read_text(encoding='utf-8'))
download_data = json.loads(download_path.read_text(encoding='utf-8'))

if len(repo_data) != len(download_data):
    raise SystemExit(f'Length mismatch: repo={len(repo_data)} download={len(download_data)}')

for repo_item, down_item in zip(repo_data, download_data):
    if repo_item.get('product_id') != down_item.get('product_id'):
        raise SystemExit(
            f'ID mismatch: {repo_item.get("product_id")} != {down_item.get("product_id")}')
    repo_item['image_url'] = down_item.get('image_url', repo_item.get('image_url', ''))

repo_path.write_text(json.dumps(repo_data, indent=4, ensure_ascii=False), encoding='utf-8')
print('Updated', len(repo_data), 'products with downloaded image_url values.')
