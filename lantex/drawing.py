import svgwrite
import json

class Drawing():
    def __init__(self):
        with open('lantex/colors.json', 'r') as fh:
            decoder = json.JSONDecoder()
            self.colors = decoder.decode(fh.read())

    def render(self, output):
        dwg = svgwrite.Drawing(output, profile='tiny')
        # Drawing bits go here
        dwg.save()
