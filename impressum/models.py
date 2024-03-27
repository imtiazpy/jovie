from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class ImpressumPage(Page):
    parent_page_types = [
        'home.HomePage',
    ]
    subpage_types = []
    template = "impressum/impressum_page.html"

    english_content = RichTextField(blank=True, null=True)
    german_content = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("english_content"),
        FieldPanel("german_content")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Pass the language information to the template context
        context['lang'] = request.GET.get('lang', 'en')
        return context

    class Meta:
        verbose_name = "Impressum page"
        verbose_name_plural = "Impressum pages"