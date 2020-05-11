from math import radians, cos, sin, asin, sqrt

class Algorithm:
    def __init__(self, points, k_num):
        self.k_num = k_num
        self.vertexes = []
        for point in points:
            vertex = Vertex(point["coordinates"], point["id"])
            self.vertexes.append(vertex)

    def greedyApprox(self):
        self.k_centers = []
        self.add_to_k_centers(self.vertexes[0])
        for i in range(self.k_num-1):
            max_dist = 0
            for vertex in self.vertexes:
                subset_dist = self.subset_distance(vertex)
                if (max_dist <= subset_dist):
                    max_dist = subset_dist
                    further_vertex = vertex
            self.add_to_k_centers(further_vertex)
        return self.get_k_centers()

    def add_to_k_centers(self, vertex):
        self.k_centers.append(vertex)
        if vertex in self.vertexes:
            self.vertexes.remove(vertex)
            return True
        return False

    def subset_distance(self, vertex):
        min_dist = self.k_centers[0].distance(vertex)
        center_dist = min_dist
        for center in self.k_centers:
            center_dist = center.distance(vertex)
            if (center_dist <= min_dist):
                min_dist = center_dist
        return center_dist

    def get_k_centers(self):
        result = []
        for vertex in self.k_centers:
            center = vertex.get_dict()
            result.append(center)
        return result

    def get_l_list(self):
        result = []
        i = 0
        for vertex in self.vertexes:
            i = i + 1
            # print('vertex ', i, ': ')
            min_dist = self.k_centers[0].distance(vertex)
            vertex_center = self.k_centers[0]
            for center in self.k_centers:
                center_dist = center.distance(vertex)
                # print('center_dist :', center_dist, center.id)
                if (center_dist < min_dist):
                    min_dist = center_dist
                    vertex_center = center
                    # print('min_dist :', min_dist)
            result.append([[vertex_center.y, vertex_center.x], [vertex.y, vertex.x]])
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
