from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from blogs.models import Post,Category, User,Contact
from .models import *
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm,ContactForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from .models import UserOtp


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
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
        return redirect('login')  
    else:
        return render(request, 'login.html')
    

def logout_view(request):
    logout(request)
    return redirect('login')  

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


def post(request, url):
    post = get_object_or_404(Post, url=url)
    cats = Category.objects.all()
    content_type = ContentType.objects.get_for_model(Post)
    comments = Comment.objects.filter(content_type=content_type, object_id=post.post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type
            comment.object_id = post.post_id
            comment.save()
            return redirect('post', url=post.url)
    else:
        form = CommentForm()
    
    return render(request, 'post.html', {
        'post': post, 
        'cats': cats, 
        'comments': comments, 
        'form': form,
        'content_type': content_type
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('post', url=comment.content_object.url)

def category(request, url):
    cat = Category.objects.get(url=url)
    posts = Post.objects.filter(cat=cat)
    return render(request, "category.html", {'cat': cat, 'posts': posts})

def about(request):
    return render(request,'about.html')

@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def travel(request):
    cats = Category.objects.all()
    return render(request,'travel.html',{'cats': cats})

def food(request):
    cats = Category.objects.all()
    return render(request,'food.html',{'cats':cats})

def photography(request):
    cats = Category.objects.all()
    return render(request,'photography.html',{'cats':cats})

def fitness(request):
    cats = Category.objects.all()
    return render(request,'fitness.html',{'cats':cats})

def terms(request):
    return render(request,'terms.html')

def forgot_password(request):
   return render(request, 'forgot_password.html')




def send_otp(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = random.randint(100000, 999999)
                UserOtp.objects.create(user=user, otp=otp)
                send_mail(
                    'Your OTP code',
                    f'Use this OTP to reset your password: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return redirect('reset_password')
            except User.DoesNotExist:
                form.add_error('email', 'User with this email does not exist')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'forgot_password.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = CustomSetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = form.cleaned_data['otp']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            
            if password != confirm_password:
                form.add_error('confirm_password', 'Passwords do not match')
            else:
                try:
                    user = User.objects.get(email=email)
                    user_otp = UserOtp.objects.filter(user=user).latest('timestamp')
                    if user_otp.otp == int(otp) and timezone.now() <= user_otp.timestamp + timedelta(minutes=5):
                        user.set_password(password)
                        user.save()
                        return redirect('login')
                    else:
                        form.add_error('otp', 'Invalid OTP or OTP has expired')
                except User.DoesNotExist:
                    form.add_error('email', 'User not found')
    else:
        form = CustomSetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})





from .forms import PostForm

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form_data_dict = form.cleaned_data
            print(form_data_dict)
            #form.save()
            blg = Post.objects.create(
                title=form_data_dict.get("title",''),
                content = form_data_dict.get("content",''),
                url=form_data_dict.get('url',''),
                cat=form_data_dict.get('cat',''),
                image=form_data_dict.get('image',''),
                author=request.user
            )
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})




# search function
def search_view(request):
    query = request.GET.get('q',None)
    print(query)
    #category = request.GET.get('category')

    # if query is not None:
    #     posts = Post.objects.filter(category__title=query)
    # else:
    #     posts = Post.objects.filter(category__title=query)

    # return render(request, 'home.html', {'posts': posts})
    if query=="food":
        return redirect("food")
    if query=="travel":
        return redirect("travel")
    if query=="photography":
        return redirect("photography")
    if query=="fitness":
        return redirect("fitness")
    else:
        return redirect("home")










#comment section
@login_required
def add_comment(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    content_object = get_object_or_404(content_type.model_class(), post_id=object_id)
    

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type
            comment.object_id = object_id
            comment.save()
            return redirect('post', url=content_object.url)
    else:
        form = CommentForm()

    comments = Comment.objects.filter(content_type=content_type, object_id=object_id)

    return render(request, 'comments.html', {'content_object': content_object, 'comments': comments, 'form': form})

@login_required
def like_post(request):
    post_id = request.GET.get('post_id', None)
    if post_id is not None:
        post = get_object_or_404(Post, post_id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
        return redirect('post', url=post.url)
    return redirect('home')


def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    return render(request, 'user_posts.html', {'user': user, 'posts': posts})


