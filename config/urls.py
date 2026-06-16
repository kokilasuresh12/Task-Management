"""
URL configuration for config project.
"""

import mimetypes
from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.core.exceptions import SuspiciousFileOperation
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import FileResponse, Http404, JsonResponse
from django.urls import include, path


def api_health(request):
    return JsonResponse({'message': 'Task Management API is running!'})


def frontend_response(file_path, content_type=None):
    if content_type is None:
        content_type, _ = mimetypes.guess_type(file_path.name)
    if file_path.suffix == '.js':
        content_type = 'text/javascript'
    return FileResponse(file_path.open('rb'), content_type=content_type or 'application/octet-stream')


def frontend_app(request):
    index_path = settings.STATIC_ROOT / 'frontend' / 'index.html'
    if not index_path.exists():
        index_path = settings.BASE_DIR / 'static' / 'frontend' / 'index.html'

    if not index_path.exists():
        return JsonResponse({
            'message': 'Frontend is not built yet. Run: cd frontend && npm run build'
        }, status=503)
    return frontend_response(index_path, content_type='text/html')


def frontend_static(request, asset_path):
    try:
        collected_path = staticfiles_storage.path(f'frontend/{asset_path}')
    except (NotImplementedError, SuspiciousFileOperation, ValueError):
        collected_path = None

    if collected_path:
        collected_path = Path(collected_path)
        if collected_path.is_file():
            return frontend_response(collected_path)

    for frontend_root in [
        settings.STATIC_ROOT / 'frontend',
        settings.BASE_DIR / 'static' / 'frontend',
    ]:
        frontend_root = frontend_root.resolve()
        file_path = (frontend_root / asset_path).resolve()

        try:
            file_path.relative_to(frontend_root)
        except ValueError:
            continue

        if file_path.is_file():
            return frontend_response(file_path)

    raise Http404('Frontend asset not found.')


urlpatterns = [
    path('', frontend_app, name='frontend_app'),
    path('static/frontend/<path:asset_path>', frontend_static, name='frontend_static'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('api/health/', api_health, name='api_health'),
    path('api/', include('accounts.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
