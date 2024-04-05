from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Article, Department
from .forms import SignUpForm, ArticleForm

def login_view(request):
    if request.method == 'POST':
        # Handle login form submission
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            department_name = form.cleaned_data.get('department')
            department, created = Department.objects.get_or_create(name=department_name)
            user.profile.department = department
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def index(request):
    articles = Article.objects.all().order_by('-created_at')
    departments = Department.objects.all()
    if 'department' in request.GET:
        department_id = request.GET['department']
        if department_id:
            articles = articles.filter(author__profile__department=department_id)
    return render(request, 'index.html', {'articles': articles, 'departments': departments})

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('index')
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})
