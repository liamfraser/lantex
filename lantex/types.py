import re

class LantexBase(object):
    def __init__(self):
        self.identifier = None
        self.description = None
        self.notes = None
        self.properties = [ 'description', 'notes' ]

    def __repr__(self):
        out = "{0} {1}:\n".format(type(self).__name__, self.identifier)

        for p in self.properties:
            val = getattr(self, p)
            if val != None:
                out += "{0}: {1}\n".format(p, val)

        return out + "\n"

    def valid_property(self, p):
        return p in self.properties

class UnresolvedIdentifier(object):
    """
    Represents a variable that might exist in the future but we can't find
    it yet.
    """

    instance_list = []

    @staticmethod
    def new(identifier):
        """
        If we already have an instance for this identifier, don't make a new
        one
        """
        for i in UnresolvedIdentifier.instance_list:
            if i.identifier == identifier:
                return i

        # Didn't find it so make a new one
        ui = UnresolvedIdentifier(identifier)
        UnresolvedIdentifier.instance_list.append(ui)
        return ui


    def __init__(self, identifier):
        """
        Should only be called by our static method new
        """
        self.identifier = identifier

    def __repr__(self):
        return "UnresolvedIdentifier {0}".format(self.identifier)

class Addressable(LantexBase):
    def __init__(self):
        super().__init__()

        self._v4 = None
        self._v6 = None
        self._v4_gateway = None
        self._v6_gateway = None

        self.properties.append('v4')
        self.properties.append('v6')
        self.properties.append('v4_gateway')
        self.properties.append('v6_gateway')

    @property
    def v4_gateway(self):
        return self._v4_gateway

    @v4_gateway.setter
    def v4_gateway(self, value):
        """
        Can either be an UnresolvedIdentifier or IPv4Addr
        """

        try:
            ip = IPv4Addr(value)
            self._v4_gateway = ip
        except ValueError:
            self._v4_gateway = UnresolvedIdentifier(value)

    @property
    def v6_gateway(self):
        return self._v6_gateway

    @v6_gateway.setter
    def v6_gateway(self, value):
        """
        Can either be an UnresolvedIdentifier or IPv6Addr
        """

        try:
            ip = IPv6Addr(value)
            self._v6_gateway = ip
        except ValueError:
            self._v6_gateway = UnresolvedIdentifier(value)

    @property
    def v4(self):
        return self._v4
    
    @v4.setter
    def v4(self, value):
        ip = IPv4Addr(value)
        self._v4 = ip

    @property
    def v6(self):
        return self._v6
    
    @v6.setter
    def v6(self, value):
        ip = IPv6Addr(value)
        self._v6 = ip

class IPAddr(object):
    def __init__(self, addr):
        self.value = None

        m = re.search(self.regex, addr)
        if m:
            self.value = addr
        else:
            raise ValueError("Invalid {0} {1}".format(self.__class__.__name__,
                                                      addr))

    def __repr__(self):
        return "{0}: {1}".format(self.__class__.__name__, self.value)


class IPv4Addr(IPAddr):
    regex = '(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    def __init__(self, addr):
        super().__init__(addr)

class IPv6Addr(IPAddr):
    regex = '(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'

    def __init__(self, addr):
        super().__init__(addr)

class Port(LantexBase):
    def __init__(self, index):
        super().__init__()

        self.identifier = index
        self.networks = []
        self.pvid = None

        self.properties.append('networks')
        self.properties.append('pvid')

class Ports(object):
    """
    Base class for an object with ports. Will be used with multiple inheritance
    """

    def __init__(self):
        self._ports = None
        self.properties.append('ports')

    @property
    def ports(self):
        return self._ports

    @ports.setter
    def ports(self, number):
        try:
            number = int(number)
        except:
            raise ValueError("Can't convert port number {0}"
                             " to an int".format(number))

        self._ports = []

        for i in range(0, number):
            self._ports.append(Port(i+1))


class Switch(Addressable, Ports):
    def __init__(self):
        Addressable.__init__(self)
        Ports.__init__(self)

        self._managed = None
        self._default_pvid = None
        
        self.properties.append('managed')
        self.properties.append('default_pvid')
        self.properties.append('network_pmap')

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

    @property
    def network_pmap(self):
        """
        Create a dictionary mapping network names to ports / port ranges
        """

        if self._ports == None:
            return None

        out = {}

        for p in self._ports:
            for n in p.networks:
                if n.identifier in out:
                    out[n.identifier].append(p.identifier)
                else:
                    out[n.identifier] = [p.identifier]

        return out

    @network_pmap.setter
    def network_pmap(self, map_dict):

        for network, ports in map_dict.items():
            # Don't care if the network exists for now. We'll try and resolve
            # it later.
            n = UnresolvedIdentifier.new(network)

            # Try and match for a range of numbers like 1-8
            m = re.search('(\d+)-(\d+)', ports)
            if m:
                range_from = int(m.group(1)) - 1
                range_to = int(m.group(2))
                for port in range(range_from, range_to):
                    self._ports[port].networks.append(n)

            else:
                raise ValueError("Not sure what to do with ports"
                                 " {0}".format(ports))

class AccessPoint(Addressable, Ports):
    def __init__(self):
        Addressable.__init__(self)
        Ports.__init__(self)

class Network(Addressable):
    def __init__(self):
        super().__init__()

        self._vlan = None
        self.properties.append('vlan')

    @property
    def vlan(self):
        return self._vlan

    @vlan.setter
    def vlan(self, number):
        try:
            number = int(number)
        except:
            raise ValueError("Can't convert vlan number {0} to an int".format(number))

        self._vlan = number

class Tunnel(Addressable):
    def __init__(self):
        super().__init__()

class Host(Addressable):
    def __init__(self):
        super().__init__()

primitives = { 'Switch'      : Switch,
               'AccessPoint' : AccessPoint,
               'Network'     : Network,
               'Tunnel'      : Tunnel,
               'Host'        : Host }
