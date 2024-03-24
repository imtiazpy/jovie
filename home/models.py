from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from streams.blocks import ButtonBlock, WhyUsSectionBlock

class HomePage(Page):
    parent_page_types = [
        'wagtailcore.Page',
    ]
    max_count = 1

    banner_bg = models.ForeignKey(
        'wagtailimages.Image', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="+"
    )
    banner_image = models.ForeignKey(
        'wagtailimages.Image', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="+"
    )
    banner_tagline = models.CharField(max_length=200, blank=True, null=True)
    banner_title = models.CharField(max_length=300, blank=True, null=True)
    banner_subtitle = models.CharField(max_length=400, blank=True, null=True)
    buttons = StreamField(
        [('btn', ButtonBlock()),],
        null=True,
        blank=True
    )

    why_us = StreamField(
        [('why_us', WhyUsSectionBlock())],
        block_counts = {
            'why_us': {'max_num': 1}
        },
        null=True,
        blank=True
    )

    
    

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("banner_bg"),
            FieldPanel("banner_image"),
            FieldPanel("banner_tagline"),
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            FieldPanel("buttons"),
        ], heading="Banner Section"),
        FieldPanel("why_us"),

    ]




