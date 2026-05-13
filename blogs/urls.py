
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views import home,about,post,category,login_view,logout_view,contact,travel,food,photography,fitness,terms,register,forgot_password,add_comment,like_post
from .views import search_view


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
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('search/', search_view, name='search'),
    path('add_comment/<int:content_type_id>/<int:object_id>/', add_comment, name='add_comment'),
    path('like_post/<int:post_id>/', like_post, name='like_post')
    
   
]
