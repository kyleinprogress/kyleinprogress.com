from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class PostQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def published(self):
        return self.active().filter(published_date__lte=timezone.now())

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

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

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

    def __unicode__(self):
        return self.name

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

    class Meta:
        ordering = ["-published_date"]
        verbose_name_plural = 'posts'
        get_latest_by = 'published_date'
