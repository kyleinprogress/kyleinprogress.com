from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from blog.models import Post, Category, Tag

import factory.django
import feedparser
import markdown2 as markdown

# Factories
class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site
        django_get_or_create = (
            'name',
            'domain'
        )
    name = 'example.com'
    domain = 'example.com'

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = (
            'name',
            'description',
            'slug'
        )
    name = 'python'
    description = 'The Python programming language'
    slug = 'python'

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = (
            'name',
            'description',
            'slug'
        )
    name = 'python'
    description = 'The Python programming language'
    slug = 'python'

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username','email', 'password',)
    username = 'testuser'
    email = 'user@example.com'
    password = 'password'

class FlatPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FlatPage
        django_get_or_create = (
            'url',
            'title',
            'content'
        )
    url = '/about/'
    title = 'About me'
    content = 'All about me'

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
        django_get_or_create = (
            'title',
            'text',
            'slug',
            'published_date'
        )
    title = 'My First Post'
    text = 'This is my first blog post.'
    slug = 'my-first-post'
    created_date = timezone.now()
    published_date = timezone.now()
    author = factory.SubFactory(AuthorFactory)
    site = factory.SubFactory(SiteFactory)
    category = factory.SubFactory(CategoryFactory)
    header_image = factory.django.ImageField(format='JPEG')

# Create your tests here.
class PostTest(TestCase):

    def test_create_category(self):
        # Create the category
        category = CategoryFactory()

        # Check we can find it
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEquals(only_category, category)

        # Check attributes
        self.assertEquals(only_category.name, 'python')
        self.assertEquals(only_category.description, 'The Python programming language')
        self.assertEquals(only_category.slug, 'python')

    def test_create_tag(self):
        # Create the tag
        tag = TagFactory()

        # Check we can find it
        all_tags = Tag.objects.all()
        self.assertEquals(len(all_tags), 1)
        only_tag = all_tags[0]
        self.assertEquals(only_tag, tag)

        # Check attributes
        self.assertEquals(only_tag.name, 'python')
        self.assertEquals(only_tag.description, 'The Python programming language')
        self.assertEquals(only_tag.slug, 'python')

    def test_create_post(self):
        # Create The Post
        post = PostFactory()

        # Create The Tag
        tag = TagFactory()

        # Add The Tag
        post.tags.add(tag)

        # Check We Can Find The Post
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Check The Post Attributes
        self.assertEquals(only_post.author.username, 'testuser')
        self.assertEquals(only_post.author.email, 'user@example.com')
        self.assertEquals(only_post.title, 'My First Post')
        self.assertEquals(only_post.text, 'This is my first blog post.')
        self.assertEquals(only_post.slug, 'my-first-post')
        self.assertEquals(only_post.created_date.day, post.created_date.day)
        self.assertEquals(only_post.created_date.month, post.created_date.month)
        self.assertEquals(only_post.created_date.year, post.created_date.year)
        self.assertEquals(only_post.created_date.hour, post.created_date.hour)
        self.assertEquals(only_post.created_date.minute, post.created_date.minute)
        self.assertEquals(only_post.created_date.second, post.created_date.second)
        self.assertEquals(only_post.published_date.day, post.published_date.day)
        self.assertEquals(only_post.published_date.month, post.published_date.month)
        self.assertEquals(only_post.published_date.year, post.published_date.year)
        self.assertEquals(only_post.published_date.hour, post.published_date.hour)
        self.assertEquals(only_post.published_date.minute, post.published_date.minute)
        self.assertEquals(only_post.published_date.second, post.published_date.second)
        self.assertEquals(only_post.category.name, 'python')
        self.assertEquals(only_post.category.description, 'The Python programming language')

        # Check tags
        post_tags = only_post.tags.all()
        self.assertEquals(len(post_tags), 1)
        only_post_tag = post_tags[0]
        self.assertEquals(only_post_tag, tag)
        self.assertEquals(only_post_tag.name, 'python')
        self.assertEquals(only_post_tag.description, 'The Python programming language')

class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

class AdminTest(BaseAcceptanceTest):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()

    def test_login(self):
        # Get Login Page
        response = self.client.get('/admin/', follow=True)

        # Check Response Code
        self.assertEquals(response.status_code, 200)

        # Check 'Log In' In Response
        self.assertTrue('Log in' in response.content)

        # Log The User In
        self.client.login(username='loginuser', password='password')

        # Check Response Code
        response = self.client.get('/admin/', follow=True)
        self.assertEquals(response.status_code, 200)

        # Check 'Log Out' In Response
        self.assertTrue('Log out' in response.content)

    def test_logout(self):
        # Log In
        self.client.login(username='loginuser', password='password')

        # Check Response Code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log Out' In Response
        self.assertTrue('Log out' in response.content)

        # Log Out
        self.client.logout()

        # Check Response Code
        response = self.client.get('/admin/', follow=True)
        self.assertEquals(response.status_code, 200)

        # Check 'Log in' In Response
        self.assertTrue('Log in' in response.content)

    def test_create_category(self):
        # Log in
        self.client.login(username='loginuser', password="password")

        # Check response code
        response = self.client.get('/admin/blog/category/add/')
        self.assertEquals(response.status_code, 200)

        # Create the new category
        response = self.client.post('/admin/blog/category/add/', {
            'name': 'python',
            'description': 'The Python programming language'
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content)

        # Check new category now in database
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)

    def test_edit_category(self):
        # Create the category
        category = CategoryFactory()

        all_categories = Category.objects.all()
        category_id = all_categories[0].id

        # Log in
        self.client.login(username='loginuser', password="password")

        # Edit the category
        response = self.client.post('/admin/blog/category/' + str(category.pk) + '/', {
            'name': 'perl',
            'description': 'The Perl programming language'
            }, follow=True)
        self.assertEquals(response.status_code, 200)


        # Check changed successfully
        self.assertTrue('changed successfully' in response.content)

        # Check category amended
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEquals(only_category.name, 'perl')
        self.assertEquals(only_category.description, 'The Perl programming language')

    def test_delete_category(self):
        # Create the category
        category = CategoryFactory()

        all_categories = Category.objects.all()
        category_id = all_categories[0].id

        # Log in
        self.client.login(username='loginuser', password="password")

        # Delete the category
        response = self.client.post('/admin/blog/category/' + str(category.pk) + '/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)

        # Check category deleted
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 0)

    def test_create_tag(self):
        # Log in
        self.client.login(username='loginuser', password='password')

        # Check response code
        response = self.client.get('/admin/blog/tag/add/')
        self.assertEquals(response.status_code, 200)

        # Create the new tag
        response = self.client.post('/admin/blog/tag/add/', {
            'name': 'python',
            'description': 'The Python programming language'
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content)

        # Check new tag now in database
        all_tags = Tag.objects.all()
        self.assertEquals(len(all_tags), 1)

    def test_edit_tag(self):
        # Create the tag
        tag = TagFactory()

        all_tags = Tag.objects.all()
        tag_id = all_tags[0].id

        # Log in
        self.client.login(username='loginuser', password='password')

        # Edit the tag
        response = self.client.post('/admin/blog/tag/' + str(tag.pk) + '/', {
            'name': 'perl',
            'description': 'The Perl programming language'
            }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('changed successfully' in response.content)

        # Check tag amended
        all_tags = Tag.objects.all()
        self.assertEquals(len(all_tags), 1)
        only_tag = all_tags[0]
        self.assertEquals(only_tag.name, 'perl')
        self.assertEquals(only_tag.description, 'The Perl programming language')

    def test_delete_tag(self):
        # Create the tag
        tag = TagFactory()

        all_tags = Tag.objects.all()
        tag_id = all_tags[0].id

        # Log in
        self.client.login(username='loginuser', password='password')

        # Delete the tag
        response = self.client.post('/admin/blog/tag/' + str(tag.pk) + '/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)

        # Check tag deleted
        all_tags = Tag.objects.all()
        self.assertEquals(len(all_tags), 0)

    def test_create_post(self):
        # Create the category
        category = CategoryFactory()

        # Create the tag
        tag = TagFactory()

        all_categories = Category.objects.all()
        category_id = all_categories[0].id

        all_tags = Tag.objects.all()
        tag_id = all_tags[0].id

        # Log In
        self.client.login(username='loginuser', password='password')

        # Check Response Code
        response = self.client.get('/admin/blog/post/add/')
        self.assertEquals(response.status_code, 200)

        # Create The New Post
        response = self.client.post('/admin/blog/post/add/', {
            'title': 'My First Post',
            'text': 'This is my first post.',
            'created_date_0': '2015-04-18',
            'created_date_1': '18:00:00',
            'slug': 'my-first-post',
            'site': '1',
            'category': category_id,
            'tags': tag_id
        },
        follow=True)
        self.assertEquals(response.status_code, 200)

        # Check New Post Now In Database
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

    def test_create_post_without_tag(self):
        # Create the category
        category = CategoryFactory()

        all_categories = Category.objects.all()
        category_id = all_categories[0].id

        # Log In
        self.client.login(username='loginuser', password='password')

        # Check Response Code
        response = self.client.get('/admin/blog/post/add/')
        self.assertEquals(response.status_code, 200)

        # Create The New Post
        response = self.client.post('/admin/blog/post/add/', {
            'title': 'My First Post',
            'text': 'This is my first post.',
            'created_date_0': '2015-04-18',
            'created_date_1': '18:00:00',
            'slug': 'my-first-post',
            'site': '1',
            'category': category_id
        },
        follow=True)
        self.assertEquals(response.status_code, 200)

        # Check New Post Now In Database
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

    def test_edit_post(self):
        # Create The Post
        post = PostFactory()

        # Create The Tag
        tag = TagFactory()

        # Add The Tag
        post.tags.add(tag)

        # Log In
        login = self.client.login(username='loginuser', password='password')

        all_categories = Category.objects.all()
        category_id = all_categories[0].id

        # Edit The Post
        response = self.client.post('/admin/blog/post/' + str(post.pk) + '/', {
            'title': 'My second post',
            'text': 'This is my second post.',
            'created_date_0': '2015-04-18',
            'created_date_1': '18:00:00',
            'slug': 'my-second-post',
            'site': '1',
            'category': category_id,
            'tags': str(tag.pk)
        }, follow=True )
        self.assertEquals(response.status_code, 200)

        # Check Post Changed Successfully
        self.assertTrue('changed successfully' in response.content)

        # Check Amended Post
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post.title, 'My second post')
        self.assertEquals(only_post.text, 'This is my second post.')

    def test_delete_post(self):
        # Create The Post
        post = PostFactory()

        # Create The Tag
        tag = TagFactory()

        # Add The Tag
        post.tags.add(tag)

        # Get The Newly Created Post ID
        all_posts = Post.objects.all()
        post_id = all_posts[0].id

        # Check New Post Is Saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

        # Log In
        login = self.client.login(username='loginuser', password='password')
        self.assertTrue(login)

        # Delete The Post
        response = self.client.post('/admin/blog/post/' + str(post.pk) + '/delete/', {
            'post': 'yes'
        },
        follow=True)
        self.assertEquals(response.status_code, 200)

        # Check Deleted Successfully
        self.assertTrue('deleted successfully' in response.content)

        # Check Post Gone From Database
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 0)

class PostViewTest(BaseAcceptanceTest):
    def setup(self):
        self.client = Client()

    def test_index(self):
        # Create The Post
        post = PostFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')

        # Create The Tag
        tag = TagFactory()

        # Add The Tag
        post.tags.add(tag)

        # Check The New Post Is Saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

        # Fetch The Index Page
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        # Check The Post Data In Response
        self.assertTrue(post.title in response.content)
        self.assertTrue(markdown.markdown(post.text) in response.content)
        self.assertTrue(str(post.published_date.year) in response.content)
        self.assertTrue(post.published_date.strftime('%b') in response.content)
        self.assertTrue(str(post.published_date.day) in response.content)
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)
        self.assertTrue(post.category.name in response.content)

        # Check the post tag is in the response
        # -- Current Layout Doesn't Show Tags on Homepage
        # post_tag = all_posts[0].tags.all()[0]
        # self.assertTrue(post_tag.name in response.content)

    def test_post_page(self):
        # Create The Post
        post = PostFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')

        # Create The Tag
        tag = TagFactory()

        # Add The Tag
        post.tags.add(tag)

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Get the post URL
        post_url = only_post.get_absolute_url()

        # Fetch the post
        response = self.client.get(post_url)
        self.assertEquals(response.status_code, 200)

        # Check the post title is in the response
        self.assertTrue(post.title in response.content)

        # Check the post category is in the response
        self.assertTrue(post.category.name in response.content)

        # Check the post tag is in the response
        post_tag = all_posts[0].tags.all()[0]
        self.assertTrue(post_tag.name in response.content)

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.published_date.year) in response.content)
        self.assertTrue(post.published_date.strftime('%b') in response.content)
        self.assertTrue(str(post.published_date.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_category_page(self):
        # Create The Post
        post = PostFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')

        # Create The Tag
        tag = TagFactory()

        # Add The Tag
        post.tags.add(tag)

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Get the category URL
        category_url = post.category.get_absolute_url()

        # Fetch the category
        response = self.client.get(category_url)
        self.assertEquals(response.status_code, 200)

        # Check the category name is in the response
        self.assertTrue(post.category.name in response.content)

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.published_date.year) in response.content)
        self.assertTrue(post.published_date.strftime('%b') in response.content)
        self.assertTrue(str(post.published_date.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_nonexistent_category_page(self):
        category_url = '/category/blah/'
        response = self.client.get(category_url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('No posts found' in response.content)

    def test_tag_page(self):
        # Create The Post
        post = PostFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')

        # Create The Tag
        tag = TagFactory()

        # Add The Tag
        post.tags.add(tag)

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Get the tag URL
        tag_url = post.tags.all()[0].get_absolute_url()

        # Fetch the tag
        response = self.client.get(tag_url)
        self.assertEquals(response.status_code, 200)

        # Check the tag name is in the response
        # -- Current Layout Doesn't Show Tags on Individual Posts
        # self.assertTrue(post.tags.all()[0].name in response.content)

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.published_date.year) in response.content)
        self.assertTrue(post.published_date.strftime('%b') in response.content)
        self.assertTrue(str(post.published_date.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_nonexistent_tag_page(self):
        tag_url = '/tag/blah/'
        response = self.client.get(tag_url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('No posts found' in response.content)


class FeedTest(BaseAcceptanceTest):
    def test_all_post_feed(self):
        # Create The Post
        post = PostFactory(text='This is my *first* blog post')

        # Create The Tag
        tag = TagFactory()

        # Add The Tag
        post.tags.add(tag)

        # Check we can find it
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Fetch the feed
        response = self.client.get('/feeds/posts/')
        self.assertEquals(response.status_code, 200)

        # Parse the feed
        feed = feedparser.parse(response.content)

        # Check length
        self.assertEquals(len(feed.entries), 1)

        # Check post retrieved is the correct one
        feed_post = feed.entries[0]
        self.assertEquals(feed_post.title, post.title)
        self.assertTrue('This is my <em>first</em> blog post' in feed_post.description)

class FlatPageViewTest(BaseAcceptanceTest):
    def test_create_flat_page(self):
        # Create flat page
        page = FlatPageFactory()
        page.save()

        # Add the site
        page.sites.add(Site.objects.all()[0])
        page.save()

        # Check new page saved
        all_pages = FlatPage.objects.all()
        self.assertEquals(len(all_pages), 1)
        only_page = all_pages[0]
        self.assertEquals(only_page, page)

        # Check data correct
        self.assertEquals(only_page.url, '/about/')
        self.assertEquals(only_page.title, 'About me')
        self.assertEquals(only_page.content, 'All about me')

        # Get URL
        page_url = str(only_page.get_absolute_url())

        # Get the page
        response = self.client.get(page_url)
        self.assertEquals(response.status_code, 200)

        # Check title and content in response
        self.assertTrue('About me' in response.content)
        self.assertTrue('All about me' in response.content)

class SitemapTest(BaseAcceptanceTest):
    def test_sitemap(self):
        # Create a post
        post = PostFactory()

        # Create a flat page
        page = FlatPageFactory()

        # Get sitemap
        response = self.client.get('/sitemap.xml')
        self.assertEquals(response.status_code, 200)

        # Check post is present in sitemap
        self.assertTrue('my-first-post' in response.content)

        # Check page is present in sitemap
        self.assertTrue('/about/' in response.content)
