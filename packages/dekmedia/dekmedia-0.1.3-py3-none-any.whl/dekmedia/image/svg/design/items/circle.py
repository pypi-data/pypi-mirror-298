from ..base import Element, manager


@manager.element
class Circle(Element):
    spec = dict(
        c='black', f='none', w=1,
        x=lambda w: w / 2, y=lambda _, h: h / 2,
        a=lambda w: w / 2, b=lambda _, h: h / 2,
    )

    def draw(self, proxy):
        return {
            'circle': {
                "cx": proxy.x,
                "cy": proxy.y,
                "stroke": proxy.c,
                "fill": proxy.f,
            }
        }
