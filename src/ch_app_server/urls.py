"""ch_app_server URL Configuration

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
from django.urls import include, path
from rest_framework import routers
from challenges.urls import router as challenges_router
from users.urls import router as users_router, urlpatterns as user_urls
from topics.urls import router as topics_router,  topics_nested_router
from posts.urls import router as posts_router

router = routers.SimpleRouter()
router.registry.extend(challenges_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(posts_router.registry)

urlpatterns = [
    path('', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')),
    path('chaining/', include('smart_selects.urls')),
    path('api/', include(router.urls)),
    path('api/', include(topics_router.urls)),
    path('api/', include(topics_nested_router.urls)),
    path('explorer-view/', include('explorer.urls')),
] + user_urls
