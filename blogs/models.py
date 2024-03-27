from django.db import models
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.models import Page, ClusterableModel
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from wagtailcaptcha.models import WagtailCaptchaForm
from wagtail.contrib.forms.models import AbstractFormField
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel


@register_snippet
class BlogCategory(models.Model):
    """Category for Blog"""
    name = models.CharField(max_length=100, unique=True)

    panels = [
        FieldPanel('name')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Blog categories'


@register_snippet
class BlogAuthor(ClusterableModel):
    name = models.CharField(max_length=100)

    panels = [
        FieldPanel('name')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Blog authors'


@register_snippet
class BlogComment(models.Model):
    blog = models.ForeignKey(
        'BlogPage', on_delete=models.CASCADE, related_name='blog_comments')
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    comment = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='replies'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.headline}"


class CommentForm(AbstractFormField):
    page = ParentalKey('BlogPage', on_delete=models.CASCADE,
                       related_name='form_fields')


class BlogPage(WagtailCaptchaForm):
    parent_page_types = [
        'blogs.BlogIndexPage'
    ]
    subpage_types = []
    template = 'blogs/blog_page.html'

    headline = models.CharField(max_length=500, blank=True, null=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    content = RichTextField(blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    categories = ParentalManyToManyField(
        BlogCategory,
        blank=True,
        related_name="category_blogs",
        help_text="Select any category or create one from the snippet"
    )
    author = ParentalKey(
        BlogAuthor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="author_blogs",
        help_text="Select author or create one from the snippet"
    )
    view_count = models.IntegerField(default=0)

    content_panels = WagtailCaptchaForm.content_panels + [
        FieldPanel('headline'),
        FieldPanel('banner_image'),
        FieldPanel('content'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('author'),
        InlinePanel('form_fields', label="Form fields for comment")
    ]

    def increment_view_count(self):
        self.view_count += 1
        self.save()

    def get_popular_blogs(self, limit=4):
        return BlogPage.objects.live().order_by('-view_count')[:limit]


    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST)
            if form.is_valid():
                comment_data = form.cleaned_data
                comment_data.pop('cap', None)
                comment_data.pop('wagtailcaptcha', None)
                comment = BlogComment(**comment_data)
                comment.blog = self
                comment.save()
                return HttpResponseRedirect(request.path)
            else:
                comments = BlogComment.objects.filter(blog=self)
                popular_blogs = self.get_popular_blogs()
                context = {
                    'self': self,
                    'form': form,
                    'comments': comments,
                    'popular_blogs': popular_blogs,
                    'error_msg': "There was an error in the form submission. Please correct it and try again."
                }
                return render(request, self.template, context)
        else:
            self.increment_view_count()
            form = self.get_form()
            context = {
                'self': self,
                'form': form,
                'comments': BlogComment.objects.filter(blog=self),
                'popular_blogs': self.get_popular_blogs()
            }

            return render(request, self.template, context)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class BlogIndexPage(Page):
    parent_page_types = [
        'home.HomePage',
    ]
    subpage_types = [
        'blogs.BlogPage'
    ]
    template = 'blogs/blog_index_page.html'

    heading = models.CharField(max_length=255, blank=True, null=True)
    subheading = models.CharField(max_length=255, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('subheading'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        # Get all live blog pages under this BlogIndexPage
        blog_pages = BlogPage.objects.child_of(self).live()

        # Pagination
        paginator = Paginator(blog_pages, 6)  # Show 6 blogs per page
        page = request.GET.get('page')

        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            blogs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            blogs = paginator.page(paginator.num_pages)

        context['blogs'] = blogs

        return context
