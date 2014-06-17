from grako.exceptions import *  # noqa
from lantex import types

class lantexSemantics(object):
    def __init__(self):
        self.entities = []
        self.last_istring = None

    def fail(self, error):
        """
        Used for debugging
        """

        print("fail: {0}".format(error))
        print("last istring: {0}".format(self.last_istring))
        print("entities: {0}".format(self.entities))

    @staticmethod
    def flatten(container):
        for i in container:
            if isinstance(i, list) or isinstance(i, tuple):
                for j in lantexSemantics.flatten(i):
                    yield j
            else:
                yield i

    def primitive(self, ast):
        pstring = "".join(self.flatten(ast))

        if pstring in types.primitives:
            new_prim = types.primitives[pstring]()
            self.entities.append(new_prim)
        else:
            self.fail("{0} is not a valid type".format(pstring))

        return ast

    def identifier(self, ast):
        """
        Identifier matches most text assign types so need to be careful
        """

        istring = "".join(self.flatten(ast))

        # If the latest thing in the entity list is a primitive without an
        # identifier, then set one.
        if self.entities[-1].identifier == None:
            self.entities[-1].identifier = istring
       
        # If it's not an identifier for a new entity, then it might be a property
        # of the entity which will be set once we have the value
        elif self.entities[-1].valid_property(istring) and self.last_istring == None:
            self.last_istring = istring

        # We have found a value that needs to be assigned to something so
        # assign it to the last property if we have one. Otherwise fail.
        elif self.last_istring != None:
            setattr(self.entities[-1], self.last_istring, istring) 
            # Reset last istring
            self.last_istring = None
        
        else:
            self.fail("Unsure what to do with identifier {0}".format(istring))

        return ast

    def atype(self, ast):
        # We have found a value that needs to be assigned to something so
        # assign it to the last property if we have one. Otherwise fail.

        astring = None

        if self.last_istring != None:
            astring = "".join(self.flatten(ast))
            setattr(self.entities[-1], self.last_istring, astring) 
            # Reset last istring
            self.last_istring = None
        
        elif self.last_istring == None:
            # No idea how we get here but we do. We don't have anything to assign
            # an assign type to so do nothing. Seems to be when ast == None
            pass

        else:
            self.fail("Unsure what to do with assign type {0}".format(astring))

        return ast

    def map(self, ast):
        self.fail("Found a map!")
        self.fail(ast)
