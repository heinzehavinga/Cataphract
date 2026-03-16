from django import template

register = template.Library()

@register.filter
def coords(hex):
    size = 72
    x = hex.x * (size*.75)
    y = hex.y * size
    if hex.x%2==1:
        y += size/2
    return (
        f"{x+18},{y+0} "
        f"{x+54},{y+0} "
        f"{x+size},{y+36} "
        f"{x+54},{y+size} "
        f"{x+18},{y+size} "
        f"{x+0},{y+36}"
    )
