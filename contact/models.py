from django.db import models
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractFormField
from modelcluster.fields import ParentalKey


class ContactPage(WagtailCaptchaEmailForm):
    parent_page_types = [
        'home.HomePage',
    ]
    subpage_types = []

    template = "contact/contact_page.html"

    phones = StreamField([
        ("phone", blocks.CharBlock(label="Phone", max_length=20, required=False))
    ])

    emails = StreamField([
        ("email", blocks.CharBlock(label="Email", max_length=100, required=False))
    ])

    addresses = StreamField([
        ("address", blocks.CharBlock(label="Address", max_length=100, required=False))
    ])

    content_panels = WagtailCaptchaEmailForm.content_panels + [
        FieldPanel("phones"),
        FieldPanel("emails"),
        FieldPanel("addresses"),
        InlinePanel("form_fields", label="Form fields for contact"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact pages"


class ContactForm(AbstractFormField):
    """Fields to render in the Contact form"""
    page = ParentalKey(ContactPage, on_delete=models.CASCADE, related_name='form_fields')
