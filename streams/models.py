from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel


@register_snippet
class Category(models.Model):
    """Global Category snippet for using across the project"""

    CATEGORY_TYPES = (
        ('job', 'Job'),
        ('company', 'Company')
    )
    ICONS = (
        ('flaticon-accounting', 'Accounting'),
        ('flaticon-graduation-cap', 'Graduation cap'),
        ('flaticon-wrench-and-screwdriver-in-cross', 'Wrench and screwdriver'),
        ('flaticon-consultation', 'Business'),
        ('flaticon-heart', 'Health'),
        ('flaticon-computer', "Computer"),
        ('flaticon-worker', 'Worker'),
        ('flaticon-auction', 'Legal'),
        ('flaticon-user', 'User'),
        ('flaticon-employee', 'Employee'),
        ('flaticon-portfolio', 'Portfolio'),
        ('flaticon-results', 'Results'),
        ('flaticon-recruitment', 'Recruitment')
    )

    category_type = models.CharField(
        max_length=10, choices=CATEGORY_TYPES, default='job', help_text="Select the type of category")

    title = models.CharField(
        max_length=100, help_text="The title of the category")
    icon = models.CharField(max_length=100, choices=ICONS,
                            default='flaticon-user', help_text="Select the icon you want")

    panels = [
        FieldPanel('category_type'),
        FieldPanel('title'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return f'{self.category_type}-{self.title}'

    class Meta:
        verbose_name_plural = 'categories'
