import os
import re
from dektools.func import FuncAnyArgs
from dektools.yaml import yaml
from dektools.file import read_text


class Node:
    def __init__(self, manager, width, height):
        self.manager = manager
        self.width = width
        self.height = height

    def render(self, params):
        raise NotImplementedError()


class Generator(Node):
    default_wh = [1024, 1024]

    def __init__(self, manager, width, height, params, name, body):
        super().__init__(manager, width, height)
        self.name = name
        self.body = body
        self.params = params

    @staticmethod
    def _translate_data(params, data):
        result = {}
        for k, v in data.items():
            if isinstance(v, str):
                r = re.match(r"^\$\$[0-9a-zA-Z_]+$", v)
                if r:
                    v = params.get(r.group())
            if v is not None:
                result[k] = v
        return result

    def render(self, params):
        def transform(s):
            for k, v in transform_map.items():
                if s.startswith(k):
                    return f"{v}({s[len(k):].replace(',', ' ')})"
            return ""

        transform_map = {'t': 'translate', 's': 'scale', 'sk': 'skew'}

        params = {**self.params, **params}
        result = ""
        for key, value in self.body.items():
            value = value or {}
            kl = key.split("", 1)
            name = kl[0]
            if len(kl) == 2:
                items = [transform(x) for x in kl[1].split() if x]
            else:
                items = []
            content = self.manager.render(name, self._translate_data(params, value), self.width, self.height)
            if items:
                trans = f'transform="{" ".join(items)}"'
            else:
                trans = ""
            result += f"""<g{" " if trans else ""}{trans}>{content}</g>"""
        return result


class Element(Node):
    name = None
    spec = {}

    class Proxy:
        def __init__(self):
            self.params = {}

        def __getattr__(self, item):
            return self.params[item]

        def __setitem__(self, key, value):
            self.params[key] = value

    def new_proxy(self, params):
        proxy = self.Proxy()
        params = {**self.spec, **params}
        for k, v in params.items():
            if callable(v):
                v = FuncAnyArgs(v)(self.width, self.height, proxy)
            proxy[k] = v
        return proxy

    def render(self, params):
        return self.manager.render_by_struct(self.draw(self.new_proxy(params)))

    def draw(self, proxy):
        raise NotImplementedError()


class Manager:
    default_width = 1024
    default_height = default_width
    generator_cls = Generator

    @classmethod
    def parse_label(cls, label):
        kl = label.split("", 1)
        name = kl[0]
        if len(kl) == 2:
            rest = kl[1]
            rr = re.match(r"^[0-9. ]+", rest)
            if rr:
                wh = rr.group()
                sp = rest[len(wh):]
            else:
                wh = ""
                sp = rest
            params = dict([y.strip() for y in x.split(":", 1)] for x in sp.split(","))
        else:
            wh = ""
            params = {}
        items = [x.strip() for x in wh.strip().split()]
        items = items + (2 - len(items)) * [""]
        items = [int([cls.default_width, cls.default_height][i] if x == "" else x) for i, x in enumerate(items)]
        return items[0], items[1], name, params

    def __init__(self):
        self.generator_map = {}
        self.svg_map = {}
        self.element_map = {}

    def make_svg(self, name):
        node = self.get_node(name)
        return f"""
<svg viewBox="0 0 {node.width} {node.height}"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">{self.render(name, {})}</svg>""".replace("\n", "")

    def get_node(self, name, width=None, height=None):
        return self.generator_map.get(name) or \
            self.svg_map.get(name) or \
            self.element_map[name](
                self,
                self.default_width if width is None else width,
                self.default_height if height is None else height,
            )

    def render(self, name, params, width=None, height=None):
        node = self.get_node(name, width, height)
        if node:
            return node.render(params)
        return self.render_by_struct({name: params})

    @classmethod
    def render_by_struct(cls, data):
        if isinstance(data, str):
            return data
        result = ""
        for tag, attrs in data.items():
            children = attrs.pop('children', None)
            sa = " ".join(f'{k}="{v}"' for k, v in attrs.items())
            if children is None:
                result += f"<{tag} {sa}/>"
            else:
                result += f"<{tag} {sa}>{cls.render_by_struct(children)}</{tag}>"
        return result

    def load_file_yaml(self, path):
        data_map = yaml.load(path)
        for label, body in data_map.items():
            width, height, name, params = self.parse_label(label)
            self.generator_map[name] = self.generator_cls(self, width, height, params, name, body)

    def load_file_svg(self, path):
        name = os.path.basename(path)
        self.svg_map[name] = read_text(path)

    def element(self, element_cls):
        if element_cls.name:
            name = element_cls.name
        else:
            name = element_cls.__name__
        self.element_map[name] = element_cls
        return element_cls


manager = Manager()
