import requests
import hashlib
import os
from urllib.parse import urlparse, urljoin
from PIL import Image
from io import BytesIO
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class FaviconService:
    """Service for fetching, processing, and caching favicons from URLs"""
    
    # Common favicon paths to try
    FAVICON_PATHS = [
        '/favicon.ico',
        '/favicon.png',
        '/apple-touch-icon.png',
        '/apple-touch-icon-precomposed.png',
        '/static/favicon.ico',
        '/assets/favicon.ico',
    ]
    
    # Supported image formats
    SUPPORTED_FORMATS = ['ico', 'png', 'jpg', 'jpeg', 'gif', 'svg']
    
    # Maximum file size (1MB)
    MAX_FILE_SIZE = 1024 * 1024
    
    # Favicon dimensions
    FAVICON_SIZE = (32, 32)
    
    @classmethod
    def get_favicon_url(cls, url):
        """Get the most likely favicon URL for a given website URL"""
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = 'https://' + url
                parsed_url = urlparse(url)
            
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            favicon_url = cls._get_favicon_from_html(base_url)
            if favicon_url:
                return favicon_url
            
            for path in cls.FAVICON_PATHS:
                favicon_url = urljoin(base_url, path)
                if cls._check_favicon_exists(favicon_url):
                    return favicon_url
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting favicon URL for {url}: {str(e)}")
            return None
    
    @classmethod
    def _get_favicon_from_html(cls, base_url):
        """Try to extract favicon URL from HTML meta tags"""
        try:
            response = requests.get(base_url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            content = response.text.lower()
            
            favicon_patterns = [
                'rel="icon"',
                'rel="shortcut icon"',
                'rel="apple-touch-icon"',
                'rel="apple-touch-icon-precomposed"'
            ]
            
            for pattern in favicon_patterns:
                if pattern in content:
                    import re
                    match = re.search(rf'{pattern}[^>]*href=["\']([^"\']+)["\']', content)
                    if match:
                        favicon_url = match.group(1)
                        if favicon_url.startswith('//'):
                            favicon_url = 'https:' + favicon_url
                        elif favicon_url.startswith('/'):
                            favicon_url = urljoin(base_url, favicon_url)
                        elif not favicon_url.startswith('http'):
                            favicon_url = urljoin(base_url, favicon_url)
                        
                        if cls._check_favicon_exists(favicon_url):
                            return favicon_url
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing HTML for favicon: {str(e)}")
            return None
    
    @classmethod
    def _check_favicon_exists(cls, url):
        """Check if a favicon URL exists and is accessible"""
        try:
            response = requests.head(url, timeout=5, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            return response.status_code == 200
        except:
            return False
    
    @classmethod
    def fetch_and_process_favicon(cls, url):
        """Fetch favicon from URL and process it"""
        try:
            favicon_url = cls.get_favicon_url(url)
            if not favicon_url:
                return None, None
            
            # Fetch the favicon
            response = requests.get(favicon_url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            # Check file size
            if len(response.content) > cls.MAX_FILE_SIZE:
                logger.warning(f"Favicon too large: {len(response.content)} bytes")
                return None, None
            
            # Process the image
            processed_image = cls._process_favicon(response.content)
            if not processed_image:
                return None, None
            
            return processed_image, 'image/png'
            
        except Exception as e:
            logger.error(f"Error fetching favicon for {url}: {str(e)}")
            return None, None
    
    @classmethod
    def _generate_cache_key(cls, url):
        """Generate a unique cache key for a favicon URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    @classmethod
    def _process_favicon(cls, image_data):
        """Process favicon image: resize, convert to PNG, optimize"""
        try:
            image = Image.open(BytesIO(image_data))
            
            if image.mode in ('RGBA', 'LA'):
                pass
            elif image.mode == 'P':
                image = image.convert('RGBA')
            else:
                image = image.convert('RGB')
            
            image = image.resize(cls.FAVICON_SIZE, Image.Resampling.LANCZOS)
            
            output = BytesIO()
            image.save(output, format='PNG', optimize=True)
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error processing favicon: {str(e)}")
            return None
    
