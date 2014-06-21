from parser.grako import *
from parser.semantics import LantexSemantics

class LantexParser(object):
    """
    Simple class responsible for kicking off the grako parser
    """

    def __init__(self, filename, trace=False):
        self.filename = filename
        self.trace = trace
        self.entities = None

    def parse(self):
        with open(self.filename) as f:
            text = f.read()
        parser = lantexParser(parseinfo=False)
        semanticsInstance = LantexSemantics()

        ast = parser.parse(
              text,
              "start",
              filename=self.filename,
              trace=self.trace,
              semantics=semanticsInstance,
              whitespace="")

        self.entities = semanticsInstance.entities
