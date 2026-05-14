from .models import Category

def category_context(request):
    return {
        'cats': Category.objects.all()
    }
