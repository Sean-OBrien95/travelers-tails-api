from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post
from likes.models import Like
from django.db.utils import IntegrityError

class LikeTestCase(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.post1 = Post.objects.create(owner=self.user1, content='Post 1 content')
        self.post2 = Post.objects.create(owner=self.user2, content='Post 2 content')

    def test_like_creation(self):
        # Create a like
        like = Like.objects.create(owner=self.user1, post=self.post1)
        
        # Check if the like is created and related to the correct user and post
        self.assertTrue(Like.objects.filter(owner=self.user1, post=self.post1).exists())
        self.assertEqual(like.owner, self.user1)
        self.assertEqual(like.post, self.post1)

    def test_like_unique_constraint(self):
        # Create the first like
        Like.objects.create(owner=self.user1, post=self.post1)
        
        # Attempt to create a duplicate like
        with self.assertRaises(IntegrityError):
            Like.objects.create(owner=self.user1, post=self.post1)

    def test_like_str_representation(self):
        like = Like.objects.create(owner=self.user1, post=self.post1)
        self.assertEqual(str(like), f'{self.user1} {self.post1}')

    def test_like_ordering(self):
        like1 = Like.objects.create(owner=self.user1, post=self.post1)
        like2 = Like.objects.create(owner=self.user2, post=self.post2)
        
        # Assuming like2 was created after like1
        likes = list(Like.objects.all())
        self.assertEqual(likes[0], like2)
        self.assertEqual(likes[1], like1)
