from .algorithm import Algorithm, Vertex
from random import randint

class TwoApprox(Algorithm):
    def __init__(self, points, k_num):
        super().__init__(points, k_num)

    def run_algorithm(self):
        self.add_to_k_centers(self.vertexes[randint(0, len(self.vertexes)-1)])
        for _ in range(self.k_num-1):
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
