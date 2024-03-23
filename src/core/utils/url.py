
from urllib.parse import urlparse 

def parse_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc 
    path = parsed_url.path
    return domain, path