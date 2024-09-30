import requests

def _get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise ValueError(f"Error fetching the URL: {e}")
