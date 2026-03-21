from django.urls import path
from . import views

urlpatterns = [
    path('', views.film_list, name='film_list'),
    path('<int:id>/', views.film_detail, name='film_detail'),
    path('watchlist/add/<int:film_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:film_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('friends/add/<int:user_id>/', views.add_friend, name='add_friend'),
    path('friends/remove/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]