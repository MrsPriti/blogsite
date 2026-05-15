from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from blogs.models import Post,Category
from .models import Person
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm, PostForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import ListView,DetailView
from .models import Like
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
import uuid

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url) 
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
    comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(Post), object_id=post.post_id)
    
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, post=post).exists()
    
    data = {
        'post': post,
        'cats': cats,
        'comments': comments,
        'is_liked': is_liked,
        'like_count': post.likes.count(),
        'content_type_id': ContentType.objects.get_for_model(Post).id
    }
    return render(request,'post.html', data)

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
    cat = Category.objects.filter(title='Food').first()
    posts = Post.objects.filter(cat=cat) if cat else []
    return render(request,'food.html', {'posts': posts})

def photography(request):
    cat = Category.objects.filter(title='Photography').first()
    posts = Post.objects.filter(cat=cat) if cat else []
    return render(request,'photography.html', {'posts': posts})

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
@login_required
def add_comment(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    content_object = get_object_or_404(content_type.model_class(), pk=object_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                user=request.user,
                content_type=content_type,
                object_id=object_id,
                content=content
            )
            messages.success(request, 'Comment added!')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Check if the user is the author or a staff member
    if request.user == comment.user or request.user.is_staff:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    like_qs = Like.objects.filter(user=request.user, post=post)
    
    if like_qs.exists():
        like_qs.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True
        
    return JsonResponse({
        'count': post.likes.count()
    })

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author
            
            # Generate unique URL slug
            base_slug = slugify(post.title)
            unique_slug = base_slug
            num = 1
            while Post.objects.filter(url=unique_slug).exists():
                unique_slug = f'{base_slug}-{num}'
                num += 1
            
            post.url = unique_slug
            post.save()
            messages.success(request, 'Blog post published successfully!')
            return redirect('post', url=post.url)
    else:
        form = PostForm()
    
    return render(request, 'add_post.html', {'form': form})

@login_required
def edit_post(request, url):
    post = get_object_or_404(Post, url=url)
    
    # Permission check: Only author or staff can edit
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('post', url=url)
        
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post', url=post.url)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    
    # Permission check: Only author or staff can delete
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to delete this post.")
        return redirect('post', url=post.url)
        
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('home')







