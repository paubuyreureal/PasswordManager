from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64
import hashlib
from django.conf import settings
from django.core.files.base import ContentFile


class Account(models.Model):
    username = models.CharField(max_length=100)
    password = models.TextField()  # Encrypted password
    url = models.URLField()
    notes = models.TextField(blank=True, null=True)
    icon = models.URLField(blank=True, null=True)  # Legacy field for manual icon URLs
    favicon = models.BinaryField(blank=True, null=True)  # Cached favicon as binary data
    favicon_content_type = models.CharField(max_length=50, blank=True, null=True)  # MIME type
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")

    def __str__(self):
        return f"{self.username} @ {self.url}"
    
    def set_password(self, plain_password):
        """Encrypt and store the password"""
        if not self.author_id:
            raise ValueError("Account must have an author before setting password")
        
        key = self._get_encryption_key()
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(plain_password.encode())
        self.password = base64.b64encode(encrypted_password).decode()
    
    def get_password(self):
        """Decrypt and return the password"""
        if not self.password:
            return ""
        
        try:
            key = self._get_encryption_key()
            fernet = Fernet(key)
            encrypted_password = base64.b64decode(self.password.encode())
            decrypted_password = fernet.decrypt(encrypted_password)
            return decrypted_password.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt password: {str(e)}")
    
    def _get_encryption_key(self):
        """Generate encryption key based on user ID and secret"""
        if not self.author_id:
            raise ValueError("Account must have an author to generate encryption key")
            
        secret = getattr(settings, 'ENCRYPTION_SECRET', 'default-secret-key-change-this')
        user_key = f"{self.author_id}_{secret}".encode()
        # Hash to get consistent 32-byte key
        key_hash = hashlib.sha256(user_key).digest()
        return base64.urlsafe_b64encode(key_hash)
    
    def get_favicon_url(self):
        """Get the URL for the favicon (either cached or manual icon)"""
        if self.icon:
            return self.icon
        
        if self.favicon and self.favicon_content_type:
            import base64
            favicon_b64 = base64.b64encode(self.favicon).decode('utf-8')
            return f"data:{self.favicon_content_type};base64,{favicon_b64}"
        
        return None
    
    def fetch_favicon(self):
        """Fetch and cache favicon for this account's URL"""
        from .favicon_service import FaviconService
        
        try:
            favicon_data, content_type = FaviconService.fetch_and_process_favicon(self.url)
            if favicon_data:
                self.favicon = favicon_data
                self.favicon_content_type = content_type
                self.save(update_fields=['favicon', 'favicon_content_type'])
                return True
        except Exception:
            pass
        
        return False
    
    def delete_favicon(self):
        """Delete the cached favicon data"""
        if self.favicon:
            self.favicon = None
            self.favicon_content_type = None
            self.save(update_fields=['favicon', 'favicon_content_type'])
