from django.urls import path
from . import views

urlpatterns = [
    path('', views.film_list, name='film_list'),
    path('<int:id>/', views.film_detail, name='film_detail'),
    path('watchlist/add/<int:film_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:film_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
]