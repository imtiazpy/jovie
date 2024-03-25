from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from streams.blocks import WayToUseBlock, WhyUsSectionBlock, FlexSectionBlock, TestimonialsBlock


class AboutPage(Page):
    """Page model for the About Page"""

    parent_page_types = [
        'home.HomePage'
    ]
    subpage_types = []

    template = "about/about_page.html"

    about_heading = models.CharField(max_length=200, blank=True, null=True)
    about_content = models.TextField(max_length=1000, blank=True, null=True)
    about_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    way_to_use = StreamField(
        [('way_to_use', WayToUseBlock())],
        block_counts = {
            'way_to_use': {'max_num': 1}
        },
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

    flex_section = StreamField(
        [('flex', FlexSectionBlock())],
        block_counts = {
            'flex': {'max_num': 1}
        },
        null=True,
        blank=True
    )

    testimonials = StreamField(
        [('testimonials', TestimonialsBlock())],
        block_counts = {
            'testimonials': {'max_num': 1}
        },
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("about_heading"),
            FieldPanel("about_content"),
            FieldPanel("about_image"),
        ], heading="About Section"),
        FieldPanel("way_to_use"),
        FieldPanel("why_us"),
        FieldPanel("flex_section"),
        FieldPanel("testimonials"),
    ]

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About pages"


