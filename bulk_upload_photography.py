import os
import django
import uuid
from django.utils.text import slugify
from django.core.files import File
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogsite.settings')
django.setup()

from blogs.models import Post, Category
from django.contrib.auth.models import User

def upload_images():
    # 1. Get Category
    cat = Category.objects.filter(title='Photography').first()
    if not cat:
        print("Error: Category 'Photography' not found.")
        return

    # Try to get a default admin user for the author
    author = User.objects.filter(is_superuser=True).first()
    
    # 2. List of images to upload
    images_to_upload = [
        'p1.jpg', 'p2.jpg', 'p3.jpg', 'p4.jpg', 'p5.jpg', 
        'p6.jpg', 'p7.jpg', 'p8.jpg', 'p9.jpg',
        'pexels-lucasallmann-612891.jpg',
        'pexels-kelly-1179532-2918152.jpg',
        'pexels-nandhukumar-450441.jpg',
        's1.jpg', 's2.jpg', 's3.jpg', 's4.jpg', 's5.jpg', 's6.jpg'
    ]
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, 'static', 'images')
    
    for filename in images_to_upload:
        filepath = os.path.join(images_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: File not found {filepath}")
            continue
            
        # Create a nice title
        title_base = filename.split('.')[0].replace('-', ' ').title()
        title = f"Gallery: {title_base}"
        
        # Create unique URL
        unique_url = f"{slugify(title)}-{str(uuid.uuid4())[:8]}"
        
        print(f"Uploading {filename} to Cloudinary...")
        
        # Open file and save to Post
        with open(filepath, 'rb') as f:
            post = Post(
                title=title,
                content="Beautiful photography captured by our community.",
                url=unique_url,
                cat=cat,
                author=author
            )
            # The save=True here will automatically upload to Cloudinary via cloudinary_storage
            post.image.save(filename, File(f), save=True)
            
        print(f"Successfully created Post: {title}")

if __name__ == '__main__':
    upload_images()
    print("Done!")
