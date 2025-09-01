from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_quote, name="random_quote"),
    path('add/', views.add_quote, name="add_quote"),
    path('quote/<int:quote_id>/like/', views.toggle_like, name='toggle_like'),
    path('quote/<int:quote_id>/dislike/', views.toggle_dislike, name='toggle_dislike'),
    path('quote/<int:quote_id>/', views.quote_detail, name='quote_detail'),
    path('top/', views.top_quotes, name="top_quotes"),
    path('refresh/', views.refresh_quotes, name='refresh_quotes'),
    path('dashboard/', views.dashboard, name="dashboard"),
]
