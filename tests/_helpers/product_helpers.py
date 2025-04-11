from urllib.parse import urlparse, parse_qs


def extract_product_id_from_url(url: str) -> str:
    params = parse_qs(urlparse(url).query)
    id = params.get("post", [None])[0]
    return id