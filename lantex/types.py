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

    @staticmethod
    def resolve_all(entities, instance_list):
        if len(instance_list) == 0:
            raise ValueError("No unresolved identifiers")

        for i in instance_list:
            found = False
            for e in entities:
                if i.identifier == e.identifier:
                    # Found the entity we want
                    i.resolved = e
                    found = True

            if found == False:
                raise ValueError("Couldn't resolve identifier"
                                 " {0}".format(i.identifier))

    def __init__(self, identifier):
        """
        Should only be called by our static method new
        """
        self.identifier = identifier
        self.resolved = None

    def __repr__(self):
        if self.resolved != None:
            return "ResolvedIdentifier {0}".format(self.resolved.__repr__())
        else:
            return "UnresolvedIdentifier {0}".format(self.identifier)

class Connection(object):
    """
    Connects a port of an entity to the port of another entity
    """

    def __init__(self):
        self.from_e = None
        self.to_e = None

        # 1 based port indexes
        self.from_i = None
        self.to_i = None

    def __repr__(self):
        out = "Connection: {0}->{1} : ".format(self.from_e.identifier,
                                               self.from_i)
        if self.to_i == None:
            out += self.to_e.identifier
        else:
            out += "{0}->{1}".format(self.to_e.identifier, self.to_i)

        return out

    def update_ports(self):
        """
        Update the port.networks entries for the relevant entity
        """

        if self.to_i != None:
            self.from_e.ports[self.from_i - 1].networks = self.to_e.ports[self.to_i - 1].networks
        else:
            self.from_e.ports[self.from_i - 1].networks = [self.to_e]

class Addressable(LantexBase):
    def __init__(self):
        super().__init__()

        self._v4 = None
        self._v6 = None
        self._v4_range = None
        self._v6_range = None
        self._v4_gateway = None
        self._v6_gateway = None

        self.properties.append('v4')
        self.properties.append('v6')
        self.properties.append('v4_range')
        self.properties.append('v6_range')
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
    def v4_range(self):
        return self._v4_range

    @v4_range.setter
    def v4_range(self, value):
        ip = IPv4Addr(value)
        self._v4_range = ip

    @property
    def v6_range(self):
        return self._v6_range

    @v6_range.setter
    def v6_range(self, value):
        ip = IPv6Addr(value)
        self._v6_range = ip

    @property
    def v4(self):
        return self._v4

    @v4.setter
    def v4(self, value):
        if self._v4 == None:
            self._v4 = {}

        network = 'unknown'

        if type(value) is tuple:
            if type(value[0]) is Network:
                network = value[0]
                value = value[1]
            else:
                raise ValueError("Bad tuple {0} for v4 address".format(value))

        ip = IPv4Addr(value)

        if network in self._v4:
            self._v4[network].append(ip)
        else:
            self._v4[network] = [ip]

    @property
    def v6(self):
        return self._v6

    @v6.setter
    def v6(self, value):
        if self._v6 == None:
            self._v6 = {}

        network = 'unknown'

        if type(value) is tuple:
            if type(value[0]) is Network:
                network = value[0]
                value = value[1]
            else:
                raise ValueError("Bad tuple {0} for v6 address".format(value))

        ip = IPv6Addr(value)

        if network in self._v6:
            self._v6[network].append(ip)
        else:
            self._v6[network] = [ip]

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

    @property
    def networks(self):
        """
        Return a list of the all of the networks accessible across the entire
        device (i.e. all ports).
        """

        networks = {}

        for p in self._ports:
            for n in p.networks:
                if n not in networks:
                    networks[n] = None

        return list(networks.keys())

class Service(object):
    def __init__(self, stype, notes):
        self.type = stype
        self.notes = notes

class Services(object):
    """
    Base class for any object that can provide services like a web server
    """

    def __init__(self):
        self.services = {}

    def add_service(self, network, service_type, notes=None):
        new_service = Service(service_type, notes)

        if network == 'all':
            network = self.networks
        else:
            network = [network]

        for n in network:
            if n in self.services:
                self.services[n].append(new_service)
            else:
                self.services[n] = [new_service]


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

class AccessPoint(Addressable, Ports, Services):
    def __init__(self):
        Addressable.__init__(self)
        Ports.__init__(self)
        Services.__init__(self)

        self._network_ssidmap = None
        self.properties.append('network_ssidmap')

    @property
    def network_ssidmap(self):
        return self._network_ssidmap

    @network_ssidmap.setter
    def network_ssidmap(self, map_dict):
        # Will have a dictionary mapping a Network to an SSID
        # Networks will be an unresolved identifier for now

        if self._network_ssidmap == None:
            self._network_ssidmap = {}
        else:
            raise ValueError("Network ssidmap already set: {0}".format(
                             self._network_ssidmap))

        for network, ssid in map_dict.items():
            n = UnresolvedIdentifier.new(network)
            if n not in self._network_ssidmap:
                self._network_ssidmap[n] = ssid
            else:
                raise ValueError("Network {0} already exists in network ssidmap: "
                                 "{1}".format(network, self._network_ssidmap))

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

class Host(Addressable, Ports, Services):
    def __init__(self):
        Addressable.__init__(self)
        Ports.__init__(self)
        Services.__init__(self)

primitives = { 'Switch'      : Switch,
               'AccessPoint' : AccessPoint,
               'Network'     : Network,
               'Tunnel'      : Tunnel,
               'Host'        : Host }
