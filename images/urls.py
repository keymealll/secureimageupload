from django.urls import path
from . import views

urlpatterns = [
    path('gallery/', views.gallery_view, name='gallery'),
    path('upload/', views.upload_image, name='upload_image'),
    path('view/<int:image_id>/', views.view_image, name='view_image'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
]
