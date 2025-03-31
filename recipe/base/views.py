from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Recipe, Comment, User
from .forms import RecipeForm, MyUserCreationForm

# Home Page (Display Recipes)
from django.shortcuts import render
from django.db.models import Q
from .models import Recipe

def home(request):
    q = request.GET.get('q', '')  # Get search query, default to empty string if none

    recipes = Recipe.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(cuisine__icontains=q)
    )
    users = User.objects.all()

    return render(request, 'base/home.html', {'recipes': recipes, 'q': q, 'users': users})


# Recipe Detail Page + Add Comment
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.all()

    if request.method == "POST" and request.user.is_authenticated:
        comment_body = request.POST.get("comment_body")
        if comment_body:
            Comment.objects.create(user=request.user, recipe=recipe, body=comment_body)
        return redirect('recipe_detail', recipe_id=recipe.id)

    return render(request, 'base/recipe_detail.html', {'recipe': recipe, 'comments': comments})

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
            return redirect('home')

    return render(request, 'base/recipe_form.html', {'form': form})

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
    user = get_object_or_404(User, username=username)  # Get user or return 404
    return render(request, 'base/profile.html', {'user': user})
