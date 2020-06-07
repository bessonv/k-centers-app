from .algorithm import Algorithm, Vertex

class Greedy(Algorithm):
    def __init__(self, points, k_num, options):
        super().__init__(points, k_num, options)

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
