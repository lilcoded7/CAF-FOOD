from django.contrib import admin
from django.urls import path, include

# static settings 
from django.conf import settings 
from django.conf.urls.static import static 

# third part settings 
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        #  add your swagger doc title
        title="CAF-FOOD",
        #  version of the swagger doc
        default_version='v1',
        # first line that appears on the top of the doc
        description="CAF-FOOD",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CAFFOOD.urls')),
    path('account/', include('account.urls'))
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)