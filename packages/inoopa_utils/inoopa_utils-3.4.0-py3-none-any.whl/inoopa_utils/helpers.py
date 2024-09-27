from tldextract import extract

def extract_domain(url: str) -> str:
    """Extract the domain from a url."""
    return extract(url).registered_domain