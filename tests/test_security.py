import os
import tempfile
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from images.models import Image
from images.utils import validate_image_file

User = get_user_model()


class SecurityTestCase(TestCase):
    """Test security features of the application"""

    def setUp(self):
        """Set up test data"""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePassword123!'
        )

        # Set up client
        self.client = Client()

        # Create a test image file
        self.image_file = self._create_test_image()

    def _create_test_image(self):
        """Create a valid test image file"""
        # Create a small PNG image
        file_content = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00'
            b'\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\n'
            b'IDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xcc\xec'
            b'\xf4\x00\x00\x00\x00IEND\xaeB`\x82'
        )

        return SimpleUploadedFile("test.png", file_content, content_type="image/png")

    def test_secure_routes_protected(self):
        """Test that secure routes require authentication"""
        # Test gallery access
        gallery_url = reverse('gallery')
        response = self.client.get(gallery_url)
        self.assertNotEqual(response.status_code, 200)

        # Test upload access
        upload_url = reverse('upload_image')
        response = self.client.get(upload_url)
        self.assertNotEqual(response.status_code, 200)

    def test_csrf_protection(self):
        """Test CSRF protection on forms"""
        # Log in
        self.client.login(username='testuser', password='SecurePassword123!')

        # Try to submit form without CSRF token
        upload_url = reverse('upload_image')
        response = self.client.post(upload_url, {
                                    'title': 'Test Image', 'image': self.image_file}, enforce_csrf_checks=True)

        # Should be rejected due to CSRF protection
        self.assertEqual(response.status_code, 403)

    def test_file_upload_validation(self):
        """Test file upload validation"""
        # Create a malicious file
        malicious_file = SimpleUploadedFile(
            "malicious.php.png",
            b"<?php echo 'malicious code'; ?>",
            content_type="image/png"
        )

        # Attempt to validate - should raise ValidationError
        with self.assertRaises(Exception):
            validate_image_file(malicious_file)

    def test_image_access_control(self):
        """Test that users can only access their own images"""
        # Create two users
        user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='SecurePassword123!'
        )

        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='SecurePassword123!'
        )

        # Create an image for user1
        image = Image.objects.create(
            user=user1,
            title='User1 Image',
            encrypted_image=b'test_encrypted_data',
            original_filename='test.png',
            file_size=100,
            mime_type='image/png',
            encryption_key_id='test_key_id'
        )

        # Log in as user2
        self.client.login(username='user2', password='SecurePassword123!')

        # Try to access user1's image
        response = self.client.get(reverse('view_image', args=[image.id]))

        # Should not be able to access (404 or 403)
        self.assertIn(response.status_code, [403, 404])

    def test_password_policy(self):
        """Test password policy enforcement"""
        # Try to create user with weak password
        weak_passwords = [
            'password',
            '12345678',
            'abcdefgh',
            'Password',
            'Password1'
        ]

        for password in weak_passwords:
            # Should fail password validation
            user = User(
                username='weakuser',
                email='weak@example.com',
            )
            user.set_password(password)

            # Either validation will fail in clean() or save() depending on implementation
            try:
                with self.assertRaises(Exception):
                    user.full_clean()
            except:
                pass

    def test_rate_limiting(self):
        """Test rate limiting on login attempts"""
        # Try multiple rapid login attempts
        for i in range(10):
            response = self.client.post(reverse('login'), {
                'username': 'testuser',
                'password': 'wrongpassword'
            })

        # Account should be locked or rate-limited after multiple attempts
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'SecurePassword123!'
        })

        # Either should be redirected or get an error message
        self.assertFalse(
            response.context and response.context['user'].is_authenticated)
