from lantex.types import *
from parser.grako import *
from parser.semantics import LantexSemantics
import logging

class LantexParser(object):
    """
    Simple class responsible for kicking off the grako parser
    """

    def __init__(self, filename, trace=False, loglevel=logging.ERROR):
        self.filename = filename
        self.trace = trace
        self.loglevel = loglevel

    def parse(self):
        with open(self.filename) as f:
            text = f.read()
        parser = lantexParser(parseinfo=False)
        semanticsInstance = LantexSemantics(self.loglevel)

        ast = parser.parse(
              text,
              "start",
              filename=self.filename,
              trace=self.trace,
              semantics=semanticsInstance,
              whitespace="")

        self.entities = semanticsInstance.entities
        self.unresolved_identifiers = semanticsInstance.unresolved_identifiers
        UnresolvedIdentifier.resolve_all(self.entities,
                                         self.unresolved_identifiers)
