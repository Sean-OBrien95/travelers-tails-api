from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post
from comments.models import Comment

class CommentTestCase(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.post1 = Post.objects.create(owner=self.user1, content='Post 1 content')
        self.post2 = Post.objects.create(owner=self.user2, content='Post 2 content')

    def test_comment_creation(self):
        # Create a comment
        comment = Comment.objects.create(owner=self.user1, post=self.post1, content='This is a comment')
        
        # Check if the comment is created and related to the correct user and post
        self.assertTrue(Comment.objects.filter(owner=self.user1, post=self.post1, content='This is a comment').exists())
        self.assertEqual(comment.owner, self.user1)
        self.assertEqual(comment.post, self.post1)
        self.assertEqual(comment.content, 'This is a comment')

    def test_comment_str_representation(self):
        comment = Comment.objects.create(owner=self.user1, post=self.post1, content='This is a comment')
        self.assertEqual(str(comment), 'This is a comment')

    def test_comment_ordering(self):
        comment1 = Comment.objects.create(owner=self.user1, post=self.post1, content='First comment')
        comment2 = Comment.objects.create(owner=self.user2, post=self.post1, content='Second comment')
        
        # Assuming comment2 was created after comment1
        comments = list(Comment.objects.filter(post=self.post1))
        self.assertEqual(comments[0], comment2)
        self.assertEqual(comments[1], comment1)

    def test_comment_update(self):
        comment = Comment.objects.create(owner=self.user1, post=self.post1, content='Original comment')
        comment.content = 'Updated comment'
        comment.save()
        
        # Refresh from database and check updated content
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated comment')
