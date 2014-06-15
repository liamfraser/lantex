class LantexBase(object):
    def __init__(self):
        self.identifier = None
        self.description = None
        self.notes = None
        self.properties = [ 'description', 'notes' ]

    def __repr__(self):
        out = "{0} {1}:\n".format(type(self).__name__, self.identifier)

        for p in self.properties:
            out += "{0}: {1}\n".format(p, getattr(self, p))

        return out + "\n"

    def valid_property(self, p):
        return p in self.properties

class Port(LantexBase):
    def __init__(self, index):
        super().__init__()

        self.identifier = index
        self.vlans = None
        self.pvid = None

        self.properties.append('vlans')
        self.properties.append('pvid')

class Switch(LantexBase):
    def __init__(self):
        super().__init__()

        self._managed = None
        self._ports = None
        self._default_pvid = None
        
        self.properties.append('managed')
        self.properties.append('ports')
        self.properties.append('default_pvid')

    @property
    def managed(self):
        return self._managed
    
    @managed.setter
    def managed(self, value):
        # Expecting a string either true or false
        if value.lower() == 'true':
            self._managed = True
        elif value.lower() == 'false':
            self._managed = False
        else:
            raise ValueError("Invalid value {0} for property managed".format(value))

    @property
    def ports(self):
        return self._ports

    @ports.setter
    def ports(self, number):
        try:
            number = int(number)
        except:
            raise ValueError("Can't convert port number {0} to an int".format(number))

        self._ports = []

        for i in range(0, number):
            self._ports.append(Port(i))

    @property
    def default_pvid(self):
        return self._default_pvid

    @default_pvid.setter
    def default_pvid(self, pvid):
        try:
            pvid = int(pvid)
        except:
            raise ValueError("Can't convert pvid {0} to an int".format(number))
        
        self._default_pvid = pvid

        for p in self._ports:
            if p.pvid == None:
                p.pvid = pvid

class AccessPoint(LantexBase):
    def __init__(self):
        super().__init__()

class Network(LantexBase):
    def __init__(self):
        super().__init__()

class Tunnel(LantexBase):
    def __init__(self):
        super().__init__()

class Host(LantexBase):
    def __init__(self):
        super().__init__()

primitives = { 'Switch'      : Switch,
               'AccessPoint' : AccessPoint,
               'Network'     : Network,
               'Tunnel'      : Tunnel,
               'Host'        : Host }
