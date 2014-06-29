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

class Drawing(object):
    def __init__(self, output, parser_data):
        self.parser_data = parser_data

        with open('lantex/theme.json', 'r') as fh:
            decoder = json.JSONDecoder()
            theme = decoder.decode(fh.read())
            self.font = theme['font']
            self.colors = Color.from_json(theme)

        self.ff = "font-family: '{0}'".format(self.font)
        self.dwg = svgwrite.Drawing(output,
                                    profile='full',
                                    style=self.ff)

    def render(self):
        for entity in self.parser_data.entities:
            if issubclass(entity.__class__, Drawable):
                entity.draw(self.dwg, self.colors)

        self.dwg.save()
