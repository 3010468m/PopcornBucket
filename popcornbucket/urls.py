from django.urls import path
from . import views

urlpatterns = [
    path('', views.film_list, name='film_list'),
    path('<int:film_id>/', views.film_detail, name='film_detail'),
<<<<<<< HEAD
    path('writereview/', views.write_review, name='write_review'),
    
=======
>>>>>>> user/simi
]