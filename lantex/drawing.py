import svgwrite
import json

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
    def __init__(self):
        with open('lantex/colors.json', 'r') as fh:
            decoder = json.JSONDecoder()
            self.colors = Color.from_json(decoder.decode(fh.read()))

    def render(self, output):
        dwg = svgwrite.Drawing(output, profile='tiny')
        # Drawing bits go here
        col = self.colors['fg']['blue'].rgb
        dwg.add(svgwrite.text.Text('Hello World', insert=(0, 20), fill=col))
        dwg.save()
