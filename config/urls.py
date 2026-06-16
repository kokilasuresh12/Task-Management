"""
URL configuration for config project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import FileResponse, JsonResponse
from django.urls import include, path


def api_health(request):
    return JsonResponse({'message': 'Task Management API is running!'})


def frontend_app(request):
    index_path = settings.BASE_DIR / 'static' / 'frontend' / 'index.html'
    if not index_path.exists():
        return JsonResponse({
            'message': 'Frontend is not built yet. Run: cd frontend && npm run build'
        }, status=503)
    return FileResponse(index_path.open('rb'), content_type='text/html')


urlpatterns = [
    path('', frontend_app, name='frontend_app'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('api/health/', api_health, name='api_health'),
    path('api/', include('accounts.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
