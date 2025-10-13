# nas_project/urls.py 
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Import settings
from django.conf.urls.static import static # Import static

# ⭐ NEW: Import the view function you created in users/views.py
from users.views import auth_client_view 

urlpatterns = [
    # ⭐ NEW: Map the root URL (http://127.0.0.1:8000/) to the client view
    path('', auth_client_view, name='auth_client'),
    
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/users/', include('users.urls')),
    path('api/items/', include('items.urls')),
    path('api/lending/', include('lending.urls')), 
    
    # DRF login/logout views for the browsable API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# --- Media Files Configuration (Development Only) ---
if settings.DEBUG:
    # This pattern serves user-uploaded media files (like profile pictures) 
    # under the URL prefix defined by MEDIA_URL.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)