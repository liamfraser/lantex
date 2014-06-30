import svgwrite
import json
from lantex.types import Drawable

class Color(object):
    def __init__(self, name, rgb):
        self.name = name
        self.rgb = rgb
        self.assigned = False

    def __repr__(self):
        return "Color: {0} {1}".format(self.name, self.rgb)

    @staticmethod
    def from_json(json):
        """
        Returns a dictionary of dictionaries for background and foreground
        color instances
        """

        out = {'bg' : {}, 'fg' : {}}

        for col in json['colors']:
            rgb_string = "rgb({0}, {1}, {2})".format(col['rgb'][0],
                                                     col['rgb'][1],
                                                     col['rgb'][2])
            c = Color(col['name'], rgb_string)
            if 'base' in c.name:
                out['bg'][c.name] = c
            else:
                out['fg'][c.name] = c

        return out

class Font(object):
    def __init__(self, name, width, height):
        self.name = name,
        self.width = width # Width in pixels per character
        self.height = height # Height in pixels per character

class DrawEnv(object):
    def __init__(self, dwg, font, colors, x, y):
        self.dwg = dwg
        self.font = font
        self.colors = colors

        # x and y is where the object should insert itself
        self.x = x
        self.y = y

class Drawing(object):
    def __init__(self, output, parser_data):
        self.parser_data = parser_data

        with open('lantex/theme.json', 'r') as fh:
            decoder = json.JSONDecoder()
            theme = decoder.decode(fh.read())
            self.font = Font(theme['font']['name'],
                             theme['font']['width'],
                             theme['font']['height'])
            self.colors = Color.from_json(theme)

        self.ff = "font-family: '{0}';  font-size='20px'".format(self.font.name)
        self.dwg = svgwrite.Drawing(output,
                                    profile='full',
                                    style=self.ff)

    def render(self):
        de = DrawEnv(self.dwg, self.font, self.colors, 5, 5)

        for entity in self.parser_data.entities:
            if issubclass(entity.__class__, Drawable):
                w, h = entity.calc_size(de)
                entity.draw(de)

        self.dwg.save()
