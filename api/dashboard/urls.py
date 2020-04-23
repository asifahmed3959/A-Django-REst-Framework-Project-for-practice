from django.urls import path,include
from rest_framework import routers
from django import urls
from rest_framework_nested import routers

from . import views


router = routers.SimpleRouter()
router.register(r'quotes', views.QuoteModelViewSet, basename='quote')


quote_router = routers.NestedSimpleRouter(router, r'quotes',lookup='quote')
quote_router.register(r'publications', views.PublicationModelViewSet, basename='publication')

quote_router.register(r'approvedmembers', views.ApprovedMemberViewSet, basename='approved')

app_name = 'dashboard'

urlpatterns = [
    path('',include(router.urls)),
    path('',include(quote_router.urls)),
]