# vertex class, each vertex represents a delivery address
# based on the Graph and Vertex classes introduced in the Zybooks text, section 6.6
# # Data Structures and Algorithms by authors Roman Lysecky and Frank Vahid
# in the hub, distance and pred_hub are for implementing dijkstra's


class Hub:
    address: object

    def __init__(self, address):
        self.address = address
        self.distance = float('inf')
        self.pred_hub = None

    def __eq__(self, other):
        return self.address == other.address

    def __hash__(self):
        return hash(self.address)

    def __str__(self):
        return self.address

    # map class, creates an undirected graph from the distance between hubs


class Map:
    # creates two dictionaries - adjacency list and edge weights
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    # code to add hubs and edges
    def add_hub(self, new_hub):
        # O(N)
        if new_hub not in self.adjacency_list.keys():
            self.adjacency_list[new_hub] = []

    def add_directed_edge(self, from_hub, to_hub, weight):
        # ensures that hubs always reference the same object
        # O(N)
        all_hubs = self.adjacency_list.keys()
        for hub in all_hubs:
            if from_hub == hub:
                from_hub = hub
            if to_hub == hub:
                to_hub = hub
        self.edge_weights[(from_hub, to_hub)] = weight
        self.adjacency_list[from_hub].append(to_hub)

    def add_undirected_edge(self, hub_a, hub_b, weight):
        self.add_directed_edge(hub_a, hub_b, weight)
        self.add_directed_edge(hub_b, hub_a, weight)
