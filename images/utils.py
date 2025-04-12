import os
import imghdr
import magic
from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image as PILImage
import io


def validate_image_file(uploaded_file):
    """
    Comprehensive validation of uploaded image files

    Args:
        uploaded_file: The file from request.FILES

    Raises:
        ValidationError: If file validation fails
    """
    # Check file size (limit to 5MB)
    if uploaded_file.size > 5 * 1024 * 1024:
        raise ValidationError("File size must be no more than 5MB")

    # Read file content
    file_content = uploaded_file.read()
    uploaded_file.seek(0)  # Reset file pointer

    # Whitelist of allowed image types
    ALLOWED_TYPES = ['jpeg', 'jpg', 'png', 'gif']

    # Check MIME type using python-magic
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(file_content)

    if not mime_type.startswith('image/'):
        raise ValidationError("Uploaded file is not a valid image")

    file_type = mime_type.split('/')[1]
    if file_type not in ALLOWED_TYPES:
        raise ValidationError(
            f"Unsupported image format. Allowed formats: {', '.join(ALLOWED_TYPES)}")

    # Double-check with imghdr
    img_type = imghdr.what(None, file_content)
    if img_type not in ALLOWED_TYPES:
        raise ValidationError("File type verification failed")

    # Verify it's actually an image by opening it with PIL
    try:
        img = PILImage.open(io.BytesIO(file_content))
        img.verify()  # Verify it's a valid image

        # Check image dimensions to prevent DoS with large images
        img = PILImage.open(io.BytesIO(file_content))  # Reopen after verify
        width, height = img.size

        if width > 4000 or height > 4000:
            raise ValidationError("Image dimensions too large (max 4000x4000)")

    except Exception as e:
        raise ValidationError(f"Invalid image file: {str(e)}")

    return True


def sanitize_filename(filename):
    """
    Sanitize filename to prevent directory traversal and other attacks

    Args:
        filename (str): Original filename

    Returns:
        str: Sanitized filename
    """
    # Extract the file extension
    extension = os.path.splitext(filename)[1].lower()

    # Generate a safe base filename by removing potentially dangerous characters
    base_name = os.path.splitext(os.path.basename(filename))[0]
    safe_name = ''.join(c for c in base_name if c.isalnum() or c in '-_.')

    # Limit length
    if len(safe_name) > 50:
        safe_name = safe_name[:50]

    # Return sanitized name with extension
    return f"{safe_name}{extension}"
