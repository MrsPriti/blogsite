
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views import home,about,post,category,login_view,logout_view,contact,travel,food,photography,fitness,terms,register,forgot_password,add_comment
from .views import search_view, add_post, edit_post, delete_post,like_post,delete_comment, user_posts,send_otp, reset_password
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm



urlpatterns = [
    path('',login_view,name='login'),
    path('register/', register, name='register'),
     path('logout/', logout_view, name='logout'),
    path('home/',home,name='home'),
    path('about/',about,name='about'),
    path('blog/<slug:url>',post,name='post'),
    path('category/<slug:url>',category,name='category'),
    path('contact/',contact,name='contact'),
    path('travel/',travel,name='travel'),
    path('food/',food,name='food'),
    path('photography/',photography,name='photography'),
    path('fitness/',fitness,name='fitness'),
    path('terms/',terms,name='terms'),
    path('search/', search_view, name='search'),
    path('add_post/', add_post, name='add_post'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('like_post', like_post, name='like_post'),
    path('add_comment/<int:content_type_id>/<int:object_id>/', add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('user_posts/<str:username>/', user_posts, name='user_posts'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('send_otp/', send_otp, name='send_otp'),
    path('reset_password/', reset_password, name='reset_password'),
   
]

   

