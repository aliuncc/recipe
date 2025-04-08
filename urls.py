from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('popular-recipes/', views.popular_recipes, name="popular_recipes"),
    path('newest-recipes/', views.newest_recipes, name="newest_recipes"),
    path('trending-cuisines/', views.trending_cuisines, name="trending_cuisines"),
    path('tag/<slug:tag_slug>/', views.tag_recipes, name='tag_recipes'),
    path('recipe/<int:pk>/', views.recipe_detail, name="recipe_detail"),
    path('recipe/create/', views.create_recipe, name="create_recipe"),
    path('recipe/<int:pk>/update/', views.update_recipe, name="update_recipe"),
    path('recipe/<int:pk>/delete/', views.delete_recipe, name="delete_recipe"),
    path('recipe/<int:pk>/like/', views.like_recipe, name="like_recipe"),
    path('recipe/<int:pk>/comment/', views.add_comment, name="add_comment"),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),  
    path('logout/', views.logout_user, name="logout"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
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
