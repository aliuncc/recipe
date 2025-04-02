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
    path('recipe/tag/<slug:tag_slug>/', views.tag_recipes, name='tag_recipes'),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),  
    path('logout/', views.logout_user, name="logout"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('blog/', views.blog, name='blog'),
    path('blog/tag/<slug:tag_slug>/', views.tag_blogs, name='tag_blogs'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/create/', views.create_blog, name='create_blog'),
    path('blog/<int:blog_id>/like/', views.like_blog, name='like_blog'),
    path('blog/<int:blog_id>/comment/', views.add_blog_comment, name='add_blog_comment'),
    path('blog/<int:blog_id>/edit/', views.edit_blog, name='edit_blog'),
    path('blog/<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),
]
