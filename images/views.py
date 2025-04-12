from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

from images.forms import ImageUploadForm

from .models import Image


@login_required
def gallery_view(request):
    images = Image.objects.filter(user=request.user)
    return render(request, 'images/gallery.html', {'images': images})


@login_required
@csrf_protect
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Make sure you're saving all required fields
            image = form.save(commit=False)
            image.user = request.user
            image.original_filename = request.FILES['image'].name
            image.file_size = request.FILES['image'].size
            image.mime_type = request.FILES['image'].content_type
            image.save()

            messages.success(request, "Image uploaded successfully!")
            return redirect('gallery')
    else:
        form = ImageUploadForm()

    return render(request, 'images/upload.html', {'form': form})


@login_required
def view_image(request, image_id):
    image = get_object_or_404(Image, id=image_id, user=request.user)
    return render(request, 'images/view.html', {'image': image})


@login_required
@csrf_protect
@require_POST
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id, user=request.user)

    image.delete()

    messages.success(request, "Image deleted successfully!")
    return redirect('gallery')
