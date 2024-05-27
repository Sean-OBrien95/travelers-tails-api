from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile

class ProfileTestCase(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

    def test_profile_creation(self):
        # Check if profiles are created for the users
        self.assertTrue(Profile.objects.filter(owner=self.user1).exists())
        self.assertTrue(Profile.objects.filter(owner=self.user2).exists())

    def test_profile_str_representation(self):
        profile = Profile.objects.get(owner=self.user1)
        self.assertEqual(str(profile), "user1's profile")

    def test_profile_ordering(self):
        profile1 = Profile.objects.get(owner=self.user1)
        profile2 = Profile.objects.get(owner=self.user2)
        
        # Assuming user1 was created before user2, profile1 should come after profile2
        self.assertGreater(profile2.created_at, profile1.created_at)
        
        profiles = list(Profile.objects.all())
        self.assertEqual(profiles[0], profile2)
        self.assertEqual(profiles[1], profile1)
