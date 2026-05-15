class Graph:
    def __init__(self, zones, connections):
        self.graph = {}
        self.zones = zones
        self.connections = connections
    
    def cost(self, type_zon):
        if type_zon != 'normal':
            type_zon = type_zon.value
        print(type_zon)
        if type_zon == 'priority':
            return 0.9
        elif type_zon == 'normal':
            return 1
        elif type_zon == 'restricted':
            return 2
        else:
            return 99999

    def zone_type(self, zone_name):
        for z in self.zones:
            if z.name == zone_name:
                print(zone_name, z.type)
                return (z.type)
    def build_graph(self):
        for z in self.zones:
            self.graph[z.name] = []
            for c in self.connections:
                if c.zon1 == z.name:
                    self.graph[z.name].append((c.zon2, self.cost(self.zone_type(c.zon2))))
                elif c.zon2 == z.name:
                    self.graph[z.name].append((c.zon1, self.cost(self.zone_type(c.zon1))))

