from django import forms
from .models import Image

class ImageUploadForm(forms.ModelForm):
    """Form for secure image upload"""
    
    # Add a file field for the image upload
    image = forms.ImageField(
        required=True,
        error_messages = {
            'required': 'Please select an image to upload',
            'invalid': 'Please upload a valid image file',
            'missing': 'No file was submitted',
            'empty': 'The submitted file is empty',
            'max_length': 'Filename is too long',
            'invalid_image': 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.'
        }
    )
    
    class Meta:
        model = Image
        fields = ['title', 'description']
        
    def clean_title(self):
        """Sanitize title field"""
        title = self.cleaned_data.get('title')
        if title:
            # Remove potentially dangerous characters
            title = ''.join(c for c in title if c.isalnum() or c in ' -_.,!?')
            # Limit length
            if len(title) > 100:
                title = title[:100]
        return title
            
    def clean_description(self):
        """Sanitize description field"""
        description = self.cleaned_data.get('description')
        if description:
            # Basic sanitization
            # In production, use a proper HTML sanitizer
            # This is just a simple example
            description = description.replace('<', '&lt;').replace('>', '&gt;')
        return description