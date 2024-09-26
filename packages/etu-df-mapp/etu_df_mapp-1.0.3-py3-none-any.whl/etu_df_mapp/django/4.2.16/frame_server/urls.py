"""
URL configuration for frame_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf import settings

from app.views.cas_admin import views as cas_views
from app.views.comm.health_view import GetHealthCheckView
from app.views.user.members_view import APIGetTokenView
from frontend.views.common import common_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', common_view.login, name='login'),
    path('logout', common_view.logout, name='logout'),
    path('gettoken', APIGetTokenView.as_view()),
    path('health/check', GetHealthCheckView.as_view()),
]

urlpatterns += [
    path('cas/login', cas_views.CasLoginView.as_view(), name='cas_ng_login'),
    path('cas/logout', cas_views.CasLogoutView.as_view(), name='cas_ng_logout'),
]

if settings.DEBUG is True:
    from drf_spectacular.views import SpectacularJSONAPIView, SpectacularRedocView, SpectacularSwaggerView
    urlpatterns += [
        path('swagger/json/', SpectacularJSONAPIView.as_view(), name='schema'),
        # Optional UI:
        path('swagger/ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('swagger/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        # YOUR PATTERNS
    ]

from frontend.views.home import home_view
urlpatterns += [
    re_path(r'^api/', include('app.urls')),
    re_path(r'^sub-server/', include('app.sub_urls')),
    re_path(r'^frd/', include('frontend.urls')),
    path('', home_view.index, name='home_index'),
]
