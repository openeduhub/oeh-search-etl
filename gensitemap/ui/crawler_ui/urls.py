"""
URL configuration for crawler_ui project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from crawls.views import FilterRuleViewSet, FilterSetViewSet, CrawlsListView, CrawlDetailView, FilterSetDetailView, FilterSetCreateView, StartCrawlFormView
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .views import index

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'filter_sets', FilterSetViewSet)
router.register(r'filter_rules', FilterRuleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', index, name='index'),
    path('crawls/add/', StartCrawlFormView.as_view(), name='crawl_create'),
    path('crawls/<int:pk>/', CrawlDetailView.as_view(), name='crawl_details'),
    path('crawls/', CrawlsListView.as_view(), name='crawls_list'),
    # filters/1/
    #path('filters/<int:pk>/', index, name='filter_detail'),
    path('filters/add/', FilterSetCreateView.as_view(), name='filterset_create'),
    path('filters/<int:pk>/', FilterSetDetailView.as_view(), name='filter_details'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
