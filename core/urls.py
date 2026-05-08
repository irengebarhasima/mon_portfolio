from django.urls import path
from . import views_likes as likes
from . import views_comment
from . import views  # ← ajoute cette ligne

urlpatterns = [
    path('like-simple/<int:project_id>/', views.toggle_like_simple, name='toggle_like_simple'),
    path('api/like/', views.api_toggle_like, name='api_toggle_like'),
    path('comment-ajax/', views_comment.add_comment_ajax, name='add_comment_ajax'),
    path('comment-simple/<str:model_name>/<int:object_id>/', views.add_comment_simple, name='add_comment_simple'),
    path('rate-project/<int:project_id>/', views.rate_project, name='rate_project'), 
]
