from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'khar@khartar.com',
            password='secret'
        )
        self.post = Post.objects.create(
            title = 'Goodt title',
            body = 'nice body',
            author = self.user
        )
    def test_string_representation(self):
        post = Post(title='A Sample title')
        self.assertEqual(str(post), post.title)
    def test_contents(self):
        self.assertEqual(f'{self.post.title}','Goodt title'),
        self.assertEqual(f'{self.post.author}','testuser'),
        self.assertEqual(f'{self.post.body}','nice body')
    def test_post_list_view(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'nice body')
        self.assertTemplateUsed(response, 'home.html')
    def test_post_detail_view (self):
        response = self.client.get('/post/1')
        no_response = self.client.get('/post/1000000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Goodt title')
        self.assertTemplateUsed(response, 'post_detail.html')
    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1')
    def test_post_create_view(self):
        response = self.client.post(reverse('new_post'), {
            'title': 'New title',
            'body': 'New Text',
            'author': self.user
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New Text')
    def test_post_update_view(self):
        response = self.client.post(reverse('edit_post', args='1'),{
            'title': 'title Update',
            'body': 'text Update'
        })
        self.assertEqual(response.status_code, 302)
    def test_post_delete_view(self):
        response = self.client.post(reverse('delete_post', args='1'))
        self.assertEqual(response.status_code, 200)    


# Create your tests here.
