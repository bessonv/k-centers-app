from math import radians, cos, sin, asin, sqrt

class Algorithm:
    def __init__(self, points, k_num, options = []):
        self.k_num = k_num
        self.options = options
        self.vertexes = []
        self.k_centers = []
        self.distance_matrix = []
        for point in points:
            vertex = Vertex(point["coordinates"], point["id"])
            self.vertexes.append(vertex)
        self.start_vertexes = self.vertexes[:]
        self.compute_distance_matrix()

    def run_algorithm(self):
        pass

    def compute_distance_matrix(self):
        for vertex1 in self.vertexes:
            row = []
            for vertex2 in self.vertexes:
                row.append(vertex1.distance(vertex2))
            self.distance_matrix.append(row)
        return self.distance_matrix

    def get_distance(self, vertex1, vertex2):
        return self.distance_matrix[vertex1.id][vertex2.id]

    def add_to_k_centers(self, vertex):
        self.k_centers.append(vertex)
        if vertex in self.vertexes:
            self.vertexes.remove(vertex)
            return True
        return False

    def max_distance(self, k_centers, vertexes, set_ids = 0):
        max_path_ids = []
        max_dist = 0
        for vertex in vertexes:
            min_dist = self.get_distance(k_centers[0], vertex)
            nearest_center = k_centers[0]
            for center in k_centers:
                center_dist = self.get_distance(center, vertex)
                if (center_dist < min_dist):
                    min_dist = center_dist
                    nearest_center = center
            max_vertex_dist = min_dist
            if (max_vertex_dist > max_dist):
                max_dist = max_vertex_dist
                max_path_ids = [nearest_center.id, vertex.id]
        if (set_ids == 1):
            self.max_path_ids = max_path_ids
        return max_dist

    def get_max_distance(self):
        distance = self.max_distance(self.k_centers, self.vertexes, 1)
        return {
            "distance": distance,
            "ids": self.max_path_ids
        }

    def get_k_centers(self):
        result = []
        for vertex in self.k_centers:
            center = vertex.get_dict()
            result.append(center)
        return result

    def get_l_list(self):
        result = []
        for vertex in self.vertexes:
            min_dist = self.get_distance(self.k_centers[0], vertex)
            vertex_center = self.k_centers[0]
            for center in self.k_centers:
                center_dist = self.get_distance(center, vertex)
                if (center_dist < min_dist):
                    min_dist = center_dist
                    vertex_center = center
            result.append({
                "ids": [vertex_center.id, vertex.id],
                "coordinates": [[vertex_center.y, vertex_center.x], [vertex.y, vertex.x]]
            })
        return result

class Vertex:
    def __init__(self, coordinates, id):
        self.x = coordinates[1]
        self.y = coordinates[0]
        self.id = id

    def decart_distance(self, vertex):
        distance = ((self.x - vertex.x)**2 + (self.y - vertex.y)**2)**(1/2)
        return distance

    def distance(self, vertex): # haversine_distance
        # lon - x
        # lat - y
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [self.x, self.y, vertex.x, vertex.y])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    def get_dict(self):
        result = {
            'coordinates': [self.y, self.x],
            'id': self.id
        }
        return result
