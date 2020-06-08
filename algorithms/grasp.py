from .algorithm import Algorithm, Vertex
from random import randint, sample, choice

class Grasp(Algorithm):
    def __init__(self, points, k_num, options):
        super().__init__(points, k_num, options)
        self.best_so = []

    def greedy_solution(self, k_centers, vertexes, i):
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
                p_center = vertexes[inx]
        
        k_centers.append(p_center)
        vertexes.remove(p_center)
        return self.greedy_solution(k_centers, vertexes, i+1)

    def local_search(self, solution, distance):
        old_center = choice(solution)
        candidate = solution[:]
        candidate.remove(old_center)
        min_dist = distance
        # new_v = False
        for v in self.vertexes:
            if (v is not old_center and v not in candidate):
                new_candidate = candidate + [v]
                cand_dist = self.max_distance(new_candidate, self.vertexes)
                if (cand_dist < min_dist):
                    min_dist = cand_dist
                    solution = new_candidate[:]
                    # new_v = v
        # if (new_v):
        #     self.vertexes.remove(new_v)
        #     self.vertexes.append(old_center)
        if (min_dist >= distance):
            return solution
        else:
            return self.local_search(solution, min_dist)
    
    def run_algorithm(self):
        solution = self.greedy_solution(self.k_centers, self.vertexes, 1)
        greedy_dist = self.max_distance(solution, self.vertexes)
        local_solution = self.local_search(solution, greedy_dist)
        self.k_centers = local_solution
        return self.get_k_centers()