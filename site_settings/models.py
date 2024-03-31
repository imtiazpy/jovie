from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from wagtail.admin.panels import FieldPanel, InlinePanel

@register_setting(icon="mobile-alt")
class ContactInfo(BaseGenericSetting):
    phone = models.CharField(verbose_name="Phone", max_length=20, blank=True, null=True)
    email = models.CharField(verbose_name="Email", max_length=100, blank=True, null=True)
    address = models.TextField(verbose_name="Address", max_length=500, blank=True, null=True)

    panels = [
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('address')
    ]


@register_setting(icon="doc-full")
class CompanySettings(BaseGenericSetting):
    header_logo = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    footer_logo = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    summary = models.CharField(verbose_name="Summary", max_length=400, blank=True, null=True)
    copyright = models.CharField(verbose_name="Copy Right", max_length=100, blank=True, null=True)

    panels = [
        FieldPanel("header_logo"),
        FieldPanel("footer_logo"),
        FieldPanel("summary"),
        FieldPanel("copyright")
    ]



@register_setting(icon="globe")
class SocialMediaSettings(ClusterableModel, BaseGenericSetting):
    panels = [
        InlinePanel('social_media_links', label="Social Media Links"),
    ]


class SocialMediaLink(Orderable):
    setting = ParentalKey(
        SocialMediaSettings, on_delete=models.CASCADE, related_name='social_media_links')
    name = models.CharField(verbose_name="Name", max_length=100)
    link = models.URLField(verbose_name="Link", max_length=500)
    icon_class = models.CharField(verbose_name="Icon", max_length=100, help_text="add box icon class name: e.g: bxl-facebook")

    def save(self, *args, **kwargs):
        # Convert the 'name' field to lowercase
        self.name = self.name.lower()

        super(SocialMediaLink, self).save(*args, **kwargs)

    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
        FieldPanel('icon_class')
    ]
