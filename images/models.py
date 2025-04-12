import os
import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify


def secure_upload_path(instance, filename):
    """Generate a secure path for uploaded images"""
    # Get file extension (validate it later)
    ext = filename.split('.')[-1].lower()

    # Generate random filename with UUID to prevent guessing
    random_filename = f"{uuid.uuid4().hex}.{ext}"

    # Organize by user and date
    return os.path.join(
        'images',
        str(instance.user.id),
        random_filename
    )


class Image(models.Model):
    """Model to store secure image data"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Store the encrypted image
    encrypted_image = models.BinaryField()

    # Store file metadata separately
    original_filename = models.CharField(max_length=255)
    file_size = models.IntegerField()  # in bytes
    mime_type = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)

    # For identifying the encryption key used (in actual implementation)
    encryption_key_id = models.CharField(max_length=100)

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.title} ({self.user.username})"
