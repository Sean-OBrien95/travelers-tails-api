from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Post
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO

class PostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        url = '/posts/'  # Direct URL for creating a post
        
        # Create fake image to upload
        test_image = Image.new('RGB', (100, 100), color= 'blue')
        image_buffer = BytesIO()
        test_image.save(image_buffer, format='JPEG')
        image_buffer.seek(0)
        image_data = image_buffer.read()
        image = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        
        data = {
            'title': 'Test Post', 
            'content': 'This is a test post content.', 
            'location': 'Ireland', 
            'image': image, 
            'owner': self.user.id}
        response = self.client.post(url, data, format='multipart')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Post')

    def test_retrieve_post_list(self):
        url = '/posts/'  # Direct URL for retrieving post list
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_post(self):
        post = Post.objects.create(title='Test Post', content='This is a test post content.', owner=self.user)
        url = f'/posts/{post.pk}/'  # Direct URL for retrieving a single post
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
