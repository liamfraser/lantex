import svgwrite

class Drawing():
    def render(self, output):
        dwg = svgwrite.Drawing(output, profile='tiny')
        # Drawing bits go here
        dwg.save()
