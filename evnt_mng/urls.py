from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from user.views import activate_user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/',include('event.urls')),
    path('',include('core.urls')),
    path('user/',include('user.urls')),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
