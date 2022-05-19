from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('<slug:item_type_slug>', views.store, name='items_by_category'),
    path('<slug:item_type_slug>/<slug:item_slug>/', views.item_detail, name='item_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:item_id>/', views.submit_review, name='submit_review'),
]
