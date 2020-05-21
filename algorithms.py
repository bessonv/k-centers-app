from math import radians, cos, sin, asin, sqrt
import random

class Algorithm:
    def __init__(self, points, k_num):
        self.k_num = k_num
        self.vertexes = []
        self.k_centers = []
        self.distance_matrix = []
        for point in points:
            vertex = Vertex(point["coordinates"], point["id"])
            self.vertexes.append(vertex)
        self.start_vertexes = self.vertexes[:]
        # print('Computing matrix')
        self.compute_distance_matrix()
        # print('Matrix computed')
        # print('From matrix' ,self.get_distance(self.vertexes[0], self.vertexes[29]))
        # print('From vert', self.vertexes[0].distance(self.vertexes[29]))
        # print(self.distance_matrix)

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

    def max_distance(self, k_centers, vertexes):
        max_dist = 0
        for vertex in vertexes:
            min_dist = self.get_distance(k_centers[0], vertex)
            for center in k_centers:
                center_dist = self.get_distance(center, vertex)
                if (center_dist < min_dist):
                    min_dist = center_dist
            max_vertex_dist = min_dist
            if (max_vertex_dist > max_dist):
                max_dist = max_vertex_dist
        return max_dist

    def get_max_distance(self):
        return self.max_distance(self.k_centers, self.vertexes)

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


class TwoApprox(Algorithm):
    def __init__(self, points, k_num):
        super().__init__(points, k_num)

    def run_algorithm(self):
        self.add_to_k_centers(self.vertexes[random.randint(0, len(self.vertexes)-1)])
        for i in range(self.k_num-1):
            max_dist = 0
            for vertex in self.vertexes:
                subset_dist = self.subset_distance(vertex)
                if (max_dist <= subset_dist):
                    max_dist = subset_dist
                    further_vertex = vertex
            self.add_to_k_centers(further_vertex)
            # print('Num of vert', len(self.vertexes))
            # print('Num of k_cent', len(self.k_centers))
        return self.get_k_centers()

    def subset_distance(self, vertex):
        # min_dist = self.k_centers[0].distance(vertex)
        min_dist = self.get_distance(self.k_centers[0], vertex)
        center_dist = min_dist
        for center in self.k_centers:
            center_dist = self.get_distance(center, vertex)
            # center_dist = center.distance(vertex)
            if (center_dist <= min_dist):
                min_dist = center_dist
        return center_dist


class Greedy(Algorithm):
    def __init__(self, points, k_num):
        super().__init__(points, k_num)

    def set_center(self, k_centers, vertexes, i):
        if (len(k_centers) >= self.k_num):
            return k_centers
        min_distance = False
        for inx, vertex in enumerate(vertexes):
            p_k_centers = k_centers[:]
            p_vertexes = vertexes[:]
            p_k_centers.append(vertex)
            p_vertexes.remove(vertex)
            distance = self.max_distance(p_k_centers, p_vertexes)
            if (distance < min_distance or not min_distance):
                min_distance = distance
                p_center = vertexes[inx-1]
        
        k_centers.append(p_center)
        vertexes.remove(p_center)
        
        return self.set_center(k_centers, vertexes, i+1)

    def run_algorithm(self):
        # print("before k_centers", len(self.k_centers))
        # print("before vertexs", len(self.vertexes))
        self.k_centers = self.set_center(self.k_centers, self.vertexes, 1)
        return self.get_k_centers()


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
