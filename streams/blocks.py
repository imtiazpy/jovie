from django import forms
from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.images.blocks import ImageChooserBlock

from streams.models import Category


class LinkStructValue(blocks.StructValue):
    """for using as a value in any block where link_url and link_page attr are available"""
    def url(self):
        link_url = self.get('link_url')
        link_page = self.get('link_page')

        return {
            'src': link_page.url if link_page else link_url or '#',
            'open_in_new': bool(link_url) and not link_page
        }


class ButtonBlock(blocks.StructBlock):
    """Block for buttons to add in StreamField of any pages"""
    btn_label = blocks.CharBlock(label="Label", max_length=20, required=False)
    link_url = blocks.URLBlock(label="external URL", required=False)
    link_page = blocks.PageChooserBlock(required=False)

    class Meta:
        value_class = LinkStructValue
        icon = "link"
        label = "Button"


class WhyUsCard(blocks.StructBlock):
    """Card for Why Us section"""
    icon_class = blocks.CharBlock(label="Flat Icon Class Name", max_length=100, required=False, help_text="ex: flaticon-resume")
    title = blocks.CharBlock(label="Title", max_length=100, required=False)
    content = blocks.TextBlock(required=False, help_text="Content of the card")


class WhyUsSectionBlock(blocks.StructBlock):
    """Block for the why choose us section"""
    title = blocks.CharBlock(label="Title", max_length=200, required=False)
    subtitle = blocks.CharBlock(label="Subtitle", max_length=400, required=False)
    cards = blocks.ListBlock(WhyUsCard(required=False))

    class Meta:
        template = "streams/why_us_block.html"
        icon = "check"
        label = "Why Us"


class WayToUseItem(blocks.StructBlock):
    flat_icon_class = blocks.CharBlock(label="Flat Icon Class Name", max_length=100, required=False, help_text="ex: flaticon-website")
    title = blocks.CharBlock(label="Title", max_length=200, required=False)
    content = blocks.TextBlock(label="Content", max_length=400, required=False)

class WayToUseBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Heading", max_length=200, required=False)
    items = blocks.ListBlock(WayToUseItem(required=False))

    class Meta:
        template = "streams/way_to_use_block.html"
        icon = "info-circle"
        label = "Way To Use"



class FlexSectionBlock(blocks.StructBlock):
    """
    block for a flex section with text and image side by side, 
    image position can be changed from left to right and vice versa.
    """
    title = blocks.CharBlock(label="Title", max_length=200, required=False)
    content = blocks.TextBlock(label="Content", max_length=2000, required=False)
    image = ImageChooserBlock(required=False)
    image_position = blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')], required=False, default='right', label="Image Position")
    link_url = blocks.URLBlock(label="external URL", required=False)
    link_page = blocks.PageChooserBlock(required=False)
    btn_label = blocks.CharBlock(label="Label", max_length=20, required=False)

    class Meta:
        template = "streams/flex_section_block.html"
        icon = "folder"
        label = "Flex Section"
        value_class = LinkStructValue




class TestimonialInfo(blocks.StructBlock):
    testimonial = blocks.TextBlock(label="Testimonial", max_length=2000, required=False)
    client_name = blocks.CharBlock(label="Client Name", max_length=100, required=False)
    designation = blocks.CharBlock(label="Designation", max_length=100, required=False)

class TestimonialsBlock(blocks.StructBlock):
    """Block for showing client testimonials"""
    title = blocks.CharBlock(label="Title", max_length=200, required=False)
    subtitle = blocks.CharBlock(label="Subtitle", max_length=400, required=False)
    testimonials = blocks.ListBlock(TestimonialInfo(required=False))

    class Meta:
        template = "streams/testimonials_block.html"
        icon = "info"
        label = "Testimonials"



class CategorySectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Heading", max_length=400, required=False)
    sub_heading = blocks.CharBlock(label="Sub heading", max_length=500, required=False)
    categories = blocks.ListBlock(SnippetChooserBlock(Category))

    class Meta:
        template = "streams/category_section_block.html"
        icon = "tick-inverse"
        label = "Categories"
