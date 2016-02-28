import markdown2

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

# --------------------------------
# Helper Functions
# --------------------------------

def createLightBoxLinks(markdownText, images):
    counter = 1
    image_link = ""

    for image in images:
        image_url = image.image.url
        image_caption = image.comment
        image_ref = '![%s][]' % (image)
        image_lb_link = '<a href="%s" data-lightbox="image-%s" data-title="%s">![%s][]</a>' % (image_url, counter, image_caption, image)
        markdownText = str.replace(markdownText, image_ref, image_lb_link)
        counter = counter + 1

        image_link = '%s\n[%s]: %s "%s"' % (image_link, image, image_url, image_caption)

    md = "%s\n%s" % (markdownText, image_link)

    return md

def insertImageRefLinks(markdownText, images):
    image_ref = ""

    for image in images:
        image_url = image.image.url
        image_caption = image.comment
        image_ref = '%s\n[%s]: %s "%s"' % (image_ref, image, image_url, image_caption)

    md = "%s\n%s" % (markdownText, image_ref)
    return md

# --------------------------------
# Define models
# --------------------------------

class PostQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def published(self):
        return self.active().filter(published_date__lte=timezone.now())

# -- Categories --
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=40, unique=True)
    accent_image = models.ImageField(upload_to='categories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unicode(self.name))
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/category/%s/" % (self.slug)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

# -- Tags --
class Tag(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unicode(self.name))
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/tag/%s/" % (self.slug)

    def __str__(self):
        return self.name

# -- Images --
class Image(models.Model):
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='%Y/%m/%d', width_field='image_width', height_field='image_height')
    image_width = models.IntegerField()
    image_height = models.IntegerField()
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def image_thumbnail(self):
        return u'<img src="%s" width=250 />' % (self.image.url)
    image_thumbnail.short_description = 'Thumbnail'
    image_thumbnail.allow_tags = True

    class Meta:
        ordering = ["-upload_date"]
        verbose_name_plural = 'images'

# -- Posts --
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(
        help_text= (
            "Tick to make this entry live (see also the publication date). "
            "Note that administrators (like yourself) are allowed to preview "
            "inactive entries whereas the general public aren't."
        ),
        default=False,
    )
    published_date = models.DateTimeField(
        verbose_name= ("Publication date"),
        help_text= (
            "For an entry to be published, it must be active and its "
            "publication date must be in the past."
        ),
        blank=True,
        null=True
    )
    slug = models.SlugField(max_length=200, unique=True)
    site = models.ForeignKey('sites.Site')
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    header_image = models.ImageField(upload_to='%Y/%m/%d')
    images = models.ManyToManyField(Image, blank=True)

    objects = PostQuerySet.as_manager()

    def is_published(self):
        """
        Return True if the entry is publicly accessible.
        """
        return self.is_active and self.published_date <= timezone.now()
    is_published.boolean = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/archive/%s/%s/%s/" % (self.published_date.strftime("%Y"), self.published_date.strftime("%m"), self.slug)

    def textWithLightboxLinks(self):
        return createLightBoxLinks(self.text, self.images.all())

    def textWithImageLinks(self):
        return insertImageRefLinks(self.text, self.images.all())

    class Meta:
        ordering = ["-published_date"]
        verbose_name_plural = 'posts'
        get_latest_by = 'published_date'
