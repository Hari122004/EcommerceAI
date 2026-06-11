import re
from urllib.parse import quote_plus, urlparse, urlunparse

UNSPLASH_BASE = "https://source.unsplash.com/600x400/"
IMAGE_KEYS = (
    "image_url", "image", "img_url", "image_src",
    "photo_url", "thumbnail", "photo",
)

FALLBACK_IMAGE_QUERIES = {
    "Electronics": "electronics,gadget",
    "Clothing & Shoes": "fashion,shoes",
    "Home & Kitchen": "kitchen,appliance",
    "Beauty & Personal Care": "beauty,skincare",
    "Fashion": "fashion,shoes",
    "Home": "kitchen,appliance",
    "Beauty": "beauty,skincare",
}

DEFAULT_FALLBACK_QUERY = "shopping,bestseller"


def _build_unsplash_search_url(query: str, base: str = UNSPLASH_BASE) -> str:
    query = re.sub(r"[^a-zA-Z0-9 ]+", " ", query)
    query = re.sub(r"\s+", " ", query).strip()
    if not query:
        return ""
    return f"{base}?{quote_plus(query)}"


def _build_unsplash_search_url_from_candidate(candidate: str, query: str) -> str:
    parsed = urlparse(candidate)
    base = urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", "", "", ""))
    return _build_unsplash_search_url(query, base=base)


def _get_title_query(prod: dict) -> str:
    title = str(prod.get("title") or prod.get("name") or "").strip()
    if not title:
        return ""
    category = str(prod.get("category") or "").strip()
    return f"{title} {category}" if category else title


def _is_unsplash_url(url: str) -> bool:
    return any(domain in url for domain in ("source.unsplash.com", "images.unsplash.com"))


def get_fallback_image_url(category: str) -> str:
    category = str(category or "").strip()
    query = FALLBACK_IMAGE_QUERIES.get(category) or FALLBACK_IMAGE_QUERIES.get(category.title())
    if not query:
        return _build_unsplash_search_url(DEFAULT_FALLBACK_QUERY)
    return _build_unsplash_search_url(query)


def get_product_image_url(prod: dict) -> str:
    """Return the best available product image URL for a product dict."""
    title_query = _get_title_query(prod)
    for key in IMAGE_KEYS:
        val = prod.get(key)
        if not isinstance(val, str) or not val.strip():
            continue
        candidate = val.strip()
        if candidate.startswith("http://") or candidate.startswith("https://"):
            if _is_unsplash_url(candidate) and title_query:
                return _build_unsplash_search_url_from_candidate(candidate, title_query)
            return candidate
        return candidate

    if title_query:
        return _build_unsplash_search_url(title_query)

    return get_fallback_image_url(prod.get("category", ""))
