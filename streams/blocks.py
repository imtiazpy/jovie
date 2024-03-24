from wagtail import blocks


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
    icon_class = blocks.CharBlock(label="Icon Class Name", max_length=100, required=False, help_text="ex: flaticon-resume")
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
