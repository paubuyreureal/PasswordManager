from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account


class AccountModelTest(TestCase):
    """Tests for the Account model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_account_creation_and_password_encryption(self):
        """Test that accounts are created correctly and passwords are encrypted"""
        account = Account.objects.create(
            username='john_doe',
            password='',
            url='https://example.com',
            notes='Test account',
            author=self.user
        )
        account.set_password('test_password')
        account.save()
        
        self.assertEqual(account.username, 'john_doe')
        self.assertEqual(account.url, 'https://example.com')
        self.assertEqual(account.author, self.user)
        self.assertEqual(str(account), 'john_doe @ https://example.com')
        self.assertEqual(account.get_password(), 'test_password')
        self.assertNotEqual(account.password, 'test_password')  # Should be encrypted


class AccountAPITest(APITestCase):
    """Tests for the Account API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        
        self.account_data = {
            'username': 'john_doe',
            'password': 'encrypted_password',
            'url': 'https://example.com',
            'notes': 'Test account',
            'icon': 'https://example.com/favicon.ico'
        }
    
    def test_create_account(self):
        """Test creating a new account via API"""
        url = reverse('account-list')
        response = self.client.post(url, self.account_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        
        account = Account.objects.get()
        self.assertEqual(account.username, 'john_doe')
        self.assertEqual(account.author, self.user)
    
    def test_list_accounts_user_isolation(self):
        """Test that users only see their own accounts (data isolation)"""
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        
        # Create account for other user
        other_account = Account.objects.create(
            username='other_account',
            password='',
            url='https://other.com',
            author=other_user
        )
        other_account.set_password('other_password')
        other_account.save()
        
        # Create account for current user
        my_account = Account.objects.create(
            username='my_account',
            password='',
            url='https://my.com',
            author=self.user
        )
        my_account.set_password('my_password')
        my_account.save()
        
        url = reverse('account-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'my_account')
    
    def test_delete_account(self):
        """Test deleting an account"""
        account = Account.objects.create(
            username='john_doe',
            password='',
            url='https://example.com',
            author=self.user
        )
        account.set_password('test_password')
        account.save()
        
        url = reverse('delete-account', kwargs={'pk': account.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)
    
    def test_unauthorized_access(self):
        """Test that unauthenticated users cannot access accounts"""
        self.client.credentials()  # Remove authentication
        
        url = reverse('account-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AccountSearchFilterTest(APITestCase):
    """Tests for search and filtering functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        
        # Create test accounts
        account1 = Account.objects.create(
            username='john_doe',
            password='',
            url='https://gmail.com',
            notes='My Gmail account for work',
            author=self.user
        )
        account1.set_password('gmail_password')
        account1.save()
        
        account2 = Account.objects.create(
            username='jane_smith',
            password='',
            url='https://github.com',
            notes='GitHub for coding projects',
            author=self.user
        )
        account2.set_password('github_password')
        account2.save()
    
    def test_search_by_username(self):
        """Test searching accounts by username"""
        url = reverse('account-list')
        response = self.client.get(url, {'search': 'john'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'john_doe')
    
    def test_search_by_notes(self):
        """Test searching accounts by notes"""
        url = reverse('account-list')
        response = self.client.get(url, {'search': 'coding'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['notes'], 'GitHub for coding projects')
    
    def test_domain_filter(self):
        """Test filtering by domain"""
        url = reverse('account-list')
        response = self.client.get(url, {'domain': 'gmail.com'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['url'], 'https://gmail.com')


class AccountDetailTest(APITestCase):
    """Tests for account detail view and updates"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        
        self.account = Account.objects.create(
            username='john_doe',
            password='',
            url='https://gmail.com',
            notes='My Gmail account',
            icon='https://gmail.com/favicon.ico',
            author=self.user
        )
        self.account.set_password('original_password')
        self.account.save()
    
    def test_retrieve_account_detail(self):
        """Test retrieving individual account details"""
        url = reverse('account-detail', kwargs={'pk': self.account.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'john_doe')
        self.assertEqual(response.data['url'], 'https://gmail.com')
        self.assertEqual(response.data['notes'], 'My Gmail account')
        self.assertEqual(response.data['decrypted_password'], 'original_password')
    
    def test_update_account_details(self):
        """Test updating account details"""
        url = reverse('account-detail', kwargs={'pk': self.account.pk})
        update_data = {
            'username': 'john_updated',
            'url': 'https://updated-gmail.com',
            'notes': 'Updated Gmail account'
        }
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'john_updated')
        self.assertEqual(response.data['url'], 'https://updated-gmail.com')
        
        # Verify the account was actually updated in the database
        self.account.refresh_from_db()
        self.assertEqual(self.account.username, 'john_updated')
        self.assertEqual(self.account.url, 'https://updated-gmail.com')
    
    def test_update_account_password(self):
        """Test updating account password"""
        url = reverse('account-detail', kwargs={'pk': self.account.pk})
        update_data = {
            'password': 'new_secure_password'
        }
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the password was encrypted and updated
        self.account.refresh_from_db()
        self.assertEqual(self.account.get_password(), 'new_secure_password')
        self.assertNotEqual(self.account.password, 'new_secure_password')  # Should be encrypted


class PasswordResetTest(APITestCase):
    """Tests for password reset functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_password_reset_request_valid_username(self):
        """Test password reset request with valid username"""
        url = reverse('password-reset-request')
        data = {'username': 'testuser'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_password_reset_request_invalid_username(self):
        """Test password reset request with invalid username"""
        url = reverse('password-reset-request')
        data = {'username': 'nonexistentuser'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
    
    def test_password_reset_confirm_valid(self):
        """Test password reset confirmation with valid token"""
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        
        # Generate token
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        combined_token = f"{uid}-{token}"
        
        url = reverse('password-reset-confirm')
        data = {
            'token': combined_token,
            'password': 'new_secure_password123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        
        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_secure_password123'))


class SecurityTest(APITestCase):
    """Tests for security features and data isolation"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        
        # Create accounts for both users
        self.account1 = Account.objects.create(
            username='account1',
            password='',
            url='https://example1.com',
            author=self.user1
        )
        self.account1.set_password('password1')
        self.account1.save()
        
        self.account2 = Account.objects.create(
            username='account2',
            password='',
            url='https://example2.com',
            author=self.user2
        )
        self.account2.set_password('password2')
        self.account2.save()
    
    def test_user_data_isolation(self):
        """Test that users can only access their own data"""
        # Get token for user1
        token1 = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token1.access_token}')
        
        # User1 should only see their own accounts
        url = reverse('account-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'account1')
        
        # User1 should not be able to access user2's account
        url = reverse('account-detail', kwargs={'pk': self.account2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_password_encryption_per_user_isolation(self):
        """Test that password encryption keys are user-specific"""
        same_password = 'same_password_123'
        
        # Create accounts with same password for both users
        account1 = Account.objects.create(
            username='same_user1',
            password='',
            url='https://same.com',
            author=self.user1
        )
        account1.set_password(same_password)
        account1.save()
        
        account2 = Account.objects.create(
            username='same_user2',
            password='',
            url='https://same.com',
            author=self.user2
        )
        account2.set_password(same_password)
        account2.save()
        
        # The encrypted passwords should be different (different user keys)
        self.assertNotEqual(account1.password, account2.password)
        
        # But both should decrypt to the same plaintext
        self.assertEqual(account1.get_password(), same_password)
        self.assertEqual(account2.get_password(), same_password)
    
    def test_invalid_jwt_token_rejection(self):
        """Test that invalid JWT tokens are rejected"""
        invalid_tokens = [
            'invalid.token.here',
            'Bearer invalid_token',
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.invalid.signature',
            ''
        ]
        
        for invalid_token in invalid_tokens:
            if invalid_token:
                self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {invalid_token}')
            else:
                self.client.credentials(HTTP_AUTHORIZATION='')
            
            url = reverse('account-list')
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                           f"Invalid token '{invalid_token}' should be rejected")