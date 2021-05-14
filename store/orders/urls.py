from django.urls import path

from .views import StoreView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('store/', StoreView.as_view(), name='home'),
    path('orders/', OrderDetailView.as_view(), name='orders'),
]
