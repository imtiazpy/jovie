from django.db import models
from django.core.exceptions import ValidationError
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel



class MenuItem(Orderable):
    menu_label = models.CharField(
        blank=True,
        null=True,
        max_length=50
    )
    link_url = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("Menu", related_name="menu_items", on_delete=models.CASCADE, blank=True, null=True)

    panels = [
        FieldPanel("menu_label"),
        FieldPanel("link_url"),
        FieldPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'

    @property
    def label(self):
        if self.link_page and not self.menu_label:
            return self.link_page.title
        elif self.menu_label:
            return self.menu_label
        return 'Missing Label'


@register_snippet
class Menu(ClusterableModel):

    MENU_TYPES = (
        ('main', 'Main Menu'),
        ('footer', 'Footer Menu'),
    )
    menu_type = models.CharField(max_length=10, choices=MENU_TYPES, default='main', help_text="Select the type of menu")

    panels = [
        FieldPanel("menu_type"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def clean(self):
		# Check if a menu with the same type already exists
        existing_menu = Menu.objects.filter(menu_type=self.menu_type).exclude(pk=self.pk).first()
        if existing_menu:
            raise ValidationError(f"A menu with type '{self.menu_type}' already exists.")

    def __str__(self):
        return f"{self.menu_type}"
