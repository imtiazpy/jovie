from django import template


from ..models import Menu

register = template.Library()

@register.simple_tag()
def get_menu(menu_type):
    try:
        return Menu.objects.get(menu_type=menu_type)
    except Menu.DoesNotExist:
        return None
    