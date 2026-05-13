from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from blogs.models import Post,Category
from .models import Person
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import ListView,DetailView

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')  
    else:
        return render(request, 'login.html')
    

def logout_view(request):
    logout(request)
    return redirect('home')  

def home(request):
    #load all the post from db(10)
    posts=Post.objects.all()[:11]
    #print(posts)
    cats = Category.objects.all()
    data={
        'posts':posts,
        'cats':cats,
        
    }
    return render(request,'home.html',data)


def post(request,url):
    post= Post.objects.get(url=url)
    cats = Category.objects.all()
    return render(request,'post.html',{'post':post,'cats':cats})

def category(request, url):
    cat = Category.objects.get(url=url)
    posts = Post.objects.filter(cat=cat)
    return render(request, "category.html", {'cat': cat, 'posts': posts})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def travel(request):
    return render(request,'travel.html')

def food(request):
    return render(request,'food.html')

def photography(request):
    return render(request,'photography.html')

def fitness(request):
    return render(request,'fitness.html')

def terms(request):
    return render(request,'terms.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')


# search function
def search_view(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    if category:
        posts = Post.objects.filter(content__icontains=query, category__title=category)
    else:
        posts = Post.objects.filter(content__icontains=query)

    return render(request, 'home.html', {'posts': posts})



#comment section
def add_comment(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    content_object = get_object_or_404(content_type.model_class(), id=object_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type
            comment.object_id = object_id
            comment.save()
            return redirect(request.path)
    else:
        form = CommentForm()
    
    comments = Comment.objects.filter(content_type=content_type, object_id=object_id)
    
    return render(request, 'comments.html', {'content_object': content_object, 'comments': comments, 'form': form})







