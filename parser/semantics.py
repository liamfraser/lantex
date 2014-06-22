from grako.exceptions import *  # noqa
from lantex import types
import logging
class LantexSemantics(object):

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.entities = []
        self.stack = []

    def fail(self, error):
        """
        Used for debugging
        """

        self.logger.error("fail: {0}".format(error))
        self.logger.error("stack: {0}".format(self.stack))
        self.logger.error("entities: {0}".format(self.entities))
        raise ValueError(error)

    @staticmethod
    def _flatten_itr(container):
        for i in container:
            if isinstance(i, list) or isinstance(i, tuple):
                for j in LantexSemantics.flatten(i):
                    yield j
            else:
                yield i

    @staticmethod
    def flatten(container):
        return "".join(LantexSemantics._flatten_itr(container))

    def set_prop(self, prop, value):
        """
        Assign a property : value to the newest entity
        """

        if prop in self.entities[-1].properties:
            try:
                setattr(self.entities[-1], prop, value)
            except:
                self.fail("Caught error trying to set value {0}"
                          " for property {1}".format(value, prop))
        else:
            self.fail("Unknown property {0} for "
                      "entity {1}".format(prop, self.entities[-1]))

        self.logger.info("Updated: {0}".format(self.entities[-1]))

    def value_assignment(self, ast):
        if len(self.stack) == 0:
            # We get to this state when we've just added a map
            self.logger.info("Should have just added a map."
                             " Empty value assignment")
            return

        value = self.stack.pop()
        prop = self.stack.pop()
        self.logger.info("Found a value assignment. "
                         "Property: {0}, Value: {1}".format(prop, value))

        self.set_prop(prop, value)
        return ast

    def primitive(self, ast):
        self.stack.append(self.flatten(ast))
        return ast

    def identifier(self, ast):
        """
        Identifier matches most text assign types so need to be careful
        """
        self.stack.append(self.flatten(ast))
        return ast

    def numbers(self, ast):
        self.stack.append(self.flatten(ast))
        return ast

    def ip4(self, ast):
        self.stack.append(self.flatten(ast))
        return ast

    def ip6(self, ast):
        self.stack.append(self.flatten(ast))
        return ast

    def ipmask(self, ast):
        # Stack will have [property, ip, netmask]
        mask = self.stack.pop()
        addr =  self.stack.pop()
        self.stack.append("{0}/{1}".format(addr, mask))

    def number_range(self, ast):
        # We've found a number range so we can pop the previous two
        # numbers off the stack
        self.stack.pop()
        self.stack.pop()

        self.stack.append(self.flatten(ast))
        return ast

    def section_start(self, ast):
        identifier = self.stack.pop()
        primitive = self.stack.pop()
        self.logger.info("Found a section start with primitive {0} "
                         "and identifier {1}".format(primitive, identifier))

        # Validate the primitive
        if primitive in types.primitives:
            # Create an instance of the new type
            new_p = types.primitives[primitive]()
            new_p.identifier = identifier
            self.entities.append(new_p)
            self.logger.info("Created a new primitive object:"
                             " {0}".format(new_p))
        else:
            self.fail("{0} is not a valid primitive".format(primitive))

    def map(self, ast):
        # The stack will be:
        # [property, key, value, key, value,...]

        prop = None
        map_dict = {}

        while len(self.stack) != 0:
            if len(self.stack) == 1:
                # Must be the property we are assigning the map to
                prop = self.stack.pop()

            else:
                # It's a key and a value so add it to the dictionary
                value = self.stack.pop()
                key = self.stack.pop()
                map_dict[key] = value

        self.logger.info("Have a map to assign to {0} with vals {1}".format(prop, map_dict))
        self.set_prop(prop, map_dict)
