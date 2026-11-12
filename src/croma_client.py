import requests

SEARCH_URL = "https://api.api.sh/croma/v1/search"

def search_laptops(api_key: str, query: str = "laptop", page: int = 1, sort: str = "relevance") -> dict:
    """Search public Croma listings through API.SH."""
    if not api_key:
        raise ValueError("Missing APISH_KEY. Add your API key to the .env file.")
    headers = {"x-api-key": api_key}
    params = {"q": query, "page": page, "sort": sort}
    response = requests.get(SEARCH_URL, headers=headers, params=params, timeout=120)
    if response.status_code == 401:
        raise RuntimeError("API key rejected (401). Check that APISH_KEY is correct.")
    if response.status_code == 403:
        raise RuntimeError("Access denied (403). Check API access and account credits.")
    response.raise_for_status()
    data = response.json()
    if isinstance(data, dict) and data.get("success") is False:
        raise RuntimeError(data.get("error", "API returned an unsuccessful response."))
    return data
