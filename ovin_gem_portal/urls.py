from django.contrib import admin
from django.urls import path
from extractor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/clients/', views.get_all_clients, name='get_all_clients'),
    path('api/update-client/', views.update_client, name='update_client'),
    path('api/delete-client/', views.delete_client, name='delete_client'),
    path('api/save-custom-category/', views.save_custom_category, name='save_custom_category'),
    path('api/save-custom-state/', views.save_custom_state, name='save_custom_state'),
    path('api/refresh-categories/', views.refresh_categories, name='refresh_categories'),
    path('api/get-categories/', views.get_categories, name='get_categories'),
]