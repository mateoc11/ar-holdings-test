from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('shopify_webhook_endpoint', csrf_exempt(views.addLog), name='addLog') #Endpoint URL
]