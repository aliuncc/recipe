from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Recipe, Comment, User, Blog, BlogComment, Tag, UserFollowing
from .forms import RecipeForm, MyUserCreationForm, BlogForm, UserProfileForm

# Home Page (Display Recipes)
from django.shortcuts import render
from django.db.models import Q, Count
from .models import Recipe
from django.utils import timezone
from datetime import timedelta

def home(request):
    q = request.GET.get('q', '')  # Get search query, default to empty string if none
    tag_slug = request.GET.get('tag', '')  # Get tag filter

    recipes = Recipe.objects.all()
    
    if q:
        recipes = recipes.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(cuisine__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct()
    
    if tag_slug:
        recipes = recipes.filter(tags__slug=tag_slug)
    
    recipes = recipes.order_by('-created_at')
    users = User.objects.all()
    tags = Tag.objects.all()

    return render(request, 'base/home.html', {
        'recipes': recipes, 
        'q': q, 
        'users': users,
        'tags': tags,
        'selected_tag': tag_slug
    })

def popular_recipes(request):
    recipes = Recipe.objects.annotate(
        total_likes=Count('likes'),
        total_comments=Count('comments')
    ).order_by('-total_likes', '-total_comments', '-created_at')
    return render(request, 'base/home.html', {'recipes': recipes, 'title': 'Popular Recipes'})

def newest_recipes(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'base/home.html', {'recipes': recipes, 'title': 'Newest Recipes'})

def trending_cuisines(request):
    # Get the most common cuisines
    popular_cuisines = Recipe.objects.values('cuisine').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Get recipes for each popular cuisine
    recipes = []
    for cuisine in popular_cuisines:
        cuisine_recipes = Recipe.objects.filter(cuisine=cuisine['cuisine'])[:3]
        recipes.extend(cuisine_recipes)
    
    return render(request, 'base/home.html', {
        'recipes': recipes,
        'title': 'Trending Cuisines',
        'popular_cuisines': popular_cuisines
    })

def top_rated(request):
    # Get recipes with most likes
    recipes = Recipe.objects.annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:10]
    
    context = {
        'recipes': recipes,
        'title': 'Top Rated Recipes',
        'users': User.objects.all()
    }
    return render(request, 'base/home.html', context)

# Recipe Detail Page + Add Comment
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    comments = recipe.comments.all().order_by('-created_at')  # Get newest comments first

    if request.method == "POST" and request.user.is_authenticated:
        comment_body = request.POST.get("comment_body")
        if comment_body:
            Comment.objects.create(user=request.user, recipe=recipe, body=comment_body)
            return redirect('recipe_detail', pk=recipe.id)

    # Process ingredients list
    ingredients = [ing.strip() for ing in recipe.ingredients.split('\n') if ing.strip()]

    context = {
        'recipe': recipe,
        'comments': comments,
        'ingredients': ingredients,
    }
    
    return render(request, 'base/recipe_detail.html', context)

# Create a Recipe (Authenticated Users Only)
@login_required
def create_recipe(request):
    form = RecipeForm()

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            form.save_m2m()  # Save the many-to-many relationships (tags)
            return redirect('home')

    tags = Tag.objects.all()  # Get all available tags
    return render(request, 'base/recipe_form.html', {'form': form, 'tags': tags})

# Update Recipe
@login_required
def update_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'base/recipe_form.html', {'form': form, 'recipe': recipe})

# Delete Recipe
@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == 'POST':
        recipe.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'recipe': recipe})

# Login View
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            # Use authenticate with email as username since we set USERNAME_FIELD = 'email'
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                return render(request, "base/login_register.html", {
                    "page": "login",
                    "page_title": "Login",
                    "error": "Invalid email or password"
                })
        except User.DoesNotExist:
            return render(request, "base/login_register.html", {
                "page": "login",
                "page_title": "Login",
                "error": "Invalid email or password"
            })

    return render(request, "base/login_register.html", {"page": "login", "page_title": "Login"})

# Register View
def register_user(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    return render(request, "base/login_register.html", {"page": "register", "page_title": "Register", "form": form})

# Logout View
def logout_user(request):
    logout(request)
    return redirect("home")

def profile(request, username):
    user = get_object_or_404(User, username=username)
    created_recipes = Recipe.objects.filter(user=user).order_by('-created_at')
    liked_recipes = Recipe.objects.filter(likes=user).order_by('-created_at')
    blog_comments = BlogComment.objects.filter(user=user).order_by('-created_at')
    recipe_comments = Comment.objects.filter(user=user).order_by('-created_at')
    liked_blogs = Blog.objects.filter(likes=user).order_by('-created_at')

    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = UserFollowing.objects.filter(user=request.user, following_user=user).exists()
    followers_count = UserFollowing.objects.filter(following_user=user).count()
    following_count = UserFollowing.objects.filter(user=user).count()

    context = {
        'user': user,
        'created_recipes': created_recipes,
        'liked_recipes': liked_recipes,
        'blog_comments': blog_comments,
        'recipe_comments': recipe_comments,
        'liked_blogs': liked_blogs,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'base/profile.html', context)

@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user:
        UserFollowing.objects.get_or_create(user=request.user, following_user=target_user)
    return redirect('profile', username=username)

@login_required
def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    UserFollowing.objects.filter(user=request.user, following_user=target_user).delete()
    return redirect('profile', username=username)

def blog(request):
    q = request.GET.get('q', '')
    tag_slug = request.GET.get('tag', '')
    
    blogs = Blog.objects.all()
    
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct()
    
    if tag_slug:
        blogs = blogs.filter(tags__slug=tag_slug)
    
    blogs = blogs.order_by('-created_at')
    tags = Tag.objects.all()
    
    return render(request, 'blog.html', {
        'blogs': blogs,
        'tags': tags,
        'q': q,
        'selected_tag': tag_slug
    })

def tag_blogs(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    blogs = Blog.objects.filter(tags=tag).order_by('-created_at')
    tags = Tag.objects.all()
    
    return render(request, 'blog.html', {
        'blogs': blogs,
        'tags': tags,
        'selected_tag': tag_slug,
        'tag_name': tag.name
    })

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

@login_required
def create_blog(request):
    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            form.save_m2m()  # Save the many-to-many relationships (tags)
            return redirect('blog_detail', blog_id=blog.id)
    return render(request, 'create_blog.html', {'form': form})

@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
    return redirect('blog_detail', blog_id=blog_id)

@login_required
def add_blog_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            BlogComment.objects.create(user=request.user, blog=blog, content=content)
    return redirect('blog_detail', blog_id=blog_id)

@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Check if the user is the owner of the blog
    if request.user != blog.user:
        return redirect('blog')
    
    form = BlogForm(instance=blog)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', blog_id=blog.id)
    
    return render(request, 'edit_blog.html', {'form': form})

@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Check if the user is the owner of the blog
    if request.user != blog.user:
        return redirect('blog')
    
    if request.method == "POST":
        blog.delete()
        return redirect('blog')
    
    return render(request, 'delete_blog.html', {'blog': blog})

def tag_recipes(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    recipes = Recipe.objects.filter(tags=tag)
    return render(request, 'base/home.html', {
        'recipes': recipes,
        'tag_name': tag.name,
        'selected_tag': tag_slug
    })

@login_required
def like_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        if request.user in recipe.likes.all():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)
    return redirect('recipe_detail', pk=pk)

@login_required
def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        comment_body = request.POST.get('comment_body')
        if comment_body:
            Comment.objects.create(user=request.user, recipe=recipe, body=comment_body)
    return redirect('recipe_detail', pk=pk)

@login_required
def edit_profile(request):
    user = request.user
    form = UserProfileForm(instance=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    
    return render(request, 'base/edit_profile.html', {'form': form})

def social(request):
    return render(request, 'social.html')
