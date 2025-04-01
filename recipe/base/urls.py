from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('popular/', views.popular_recipes, name="popular-recipes"),
    path('newest/', views.newest_recipes, name="newest-recipes"),
    path('trending/', views.trending_cuisines, name="trending-cuisines"),
    path('top-rated/', views.top_rated, name="top-rated"),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name="recipe_detail"),
    path('recipe/new/', views.create_recipe, name="create_recipe"),  
    path('recipe/<int:recipe_id>/update/', views.update_recipe, name="update-recipe"),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name="delete-recipe"),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),  
    path('logout/', views.logout_user, name="logout"),
    path('profile/<str:username>/', views.profile, name='profile'),
]
