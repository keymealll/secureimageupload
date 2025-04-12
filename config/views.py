from django.shortcuts import render


def handler403(request, exception=None):
    """
    Custom 403 Forbidden handler - Access Denied
    """
    return render(request, 'error.html', {
        'error_code': '403',
        'title': 'Access Denied',
        'message': 'You do not have permission to access this resource.'
    }, status=403)


def handler404(request, exception=None):
    """
    Custom 404 Not Found handler
    """
    return render(request, 'error.html', {
        'error_code': '404',
        'title': 'Page Not Found',
        'message': 'The page you requested could not be found.'
    }, status=404)


def handler500(request):
    """
    Custom 500 Server Error handler
    """
    return render(request, 'error.html', {
        'error_code': '500',
        'title': 'Server Error',
        'message': 'There was an error processing your request. Our team has been notified.'
    }, status=500)
