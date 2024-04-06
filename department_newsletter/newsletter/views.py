from django.shortcuts import render, redirect
from .models import Article, Department
from .forms import SignUpForm, ArticleForm
from .utils import send_new_article_notification
from django.contrib.auth import authenticate, login

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
            user.department = department
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.shortcuts import render
from .models import Article, Department

def index(request):
    selected_department = request.GET.get('department')
    search_query = request.GET.get('search')
    sort_order = request.GET.get('sort')  # Get the selected sort order
    articles = Article.objects.all()
    departments = Department.objects.all()  # Retrieve all departments

    if selected_department:
        articles = articles.filter(department_id=selected_department)

    if search_query:
        articles = articles.filter(title__icontains=search_query)

    if sort_order == 'oldest':  # If oldest sort order is selected
        articles = articles.order_by('created_at')
    elif sort_order == 'newest':  # If newest sort order is selected
        articles = articles.order_by('-created_at')

    return render(request, 'index.html', {'articles': articles, 'selected_department': selected_department, 'search_query': search_query, 'departments': departments})


def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            department_name = form.cleaned_data.get('department')
            department, created = Department.objects.get_or_create(name=department_name)
            article.department = department
            article.save()
            send_new_article_notification(article)  # Send email notification
            return redirect('index')
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})