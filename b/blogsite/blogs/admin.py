from django.contrib import admin
from .models import Category,Post, Person,Comment,Like,Contact

# Register your models here.

#for configuration of category admin
class CategoryAdmin(admin.ModelAdmin):
    list_display =('image_tag','title','description','url','add_date')
    search_fields=('title',)
    
class PostAdmin(admin.ModelAdmin):
    list_display =('title',)
    search_fields=('title',)
    list_filter=('cat',)
    list_per_page=50

    class Media:
        js=("https://cdn.tiny.cloud/1/abcd1234/tinymce/6/tinymce.min.js",'script.js',)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'message', 'submitted_at')
    search_fields = ('name', 'email')

admin.site.register(Contact, ContactAdmin)
    

admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Person)
admin.site.register(Comment)
admin.site.register(Like)



