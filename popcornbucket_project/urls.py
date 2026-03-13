<<<<<<< HEAD
"""popcornbucket_project URL Configuration
=======
"""popcornbucket URL Configuration
>>>>>>> user/simi

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from popcornbucket import views
<<<<<<< HEAD
=======
from django.conf import settings
from django.conf.urls.static import static
>>>>>>> user/simi

urlpatterns = [
    path('films/', include('popcornbucket.urls')),
    path('<int:film_id>/', views.film_detail, name='film_detail'),
    path('writereview/', views.write_review, name='write_review'),
    path('admin/', admin.site.urls),
    path('films/', include('popcornbucket.urls')),
    path('<int:film_id>/', views.film_detail, name='film_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)