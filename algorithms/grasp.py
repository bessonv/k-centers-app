from .algorithm import Algorithm, Vertex
from random import randint, sample, choice

class Grasp(Algorithm):
    def __init__(self, points, k_num):
        super().__init__(points, k_num)
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
                p_center = vertexes[inx-1]
        
        k_centers.append(p_center)
        vertexes.remove(p_center)
        return self.greedy_solution(k_centers, vertexes, i+1)

    def local_search(self, solution, min_distance):
        old_center = choice(solution)
        candidate = solution[:]
        candidate.remove(old_center)
        min_dist = min_distance
        for v in self.vertexes:
            if (v is not old_center and v not in candidate):
                new_candidate = candidate + [v]
                if (min_dist == False):
                    min_dist = self.max_distance(new_candidate, self.vertexes)
                cand_dist = self.max_distance(new_candidate, self.vertexes)
                if (cand_dist < min_dist):
                    min_dist = cand_dist
                    solution = new_candidate[:]
        if (min_dist < min_distance):
            return solution
        else:
            return self.local_search(solution, min_dist)
    
    def run_algorithm(self):
        iterations = 25
        min_dist = -1
        for _ in range(iterations):
            solution = self.greedy_solution(self.k_centers, self.vertexes, 1)
            greedy_dist = self.max_distance(solution, self.vertexes)
            local_solution = self.local_search(solution, greedy_dist)
            dist = self.max_distance(local_solution, self.vertexes)
            if (min_dist < 0):
                min_dist = dist
                self.best_so = local_solution
            if dist < min_dist:
                min_dist = dist
                self.best_so = local_solution

        self.k_centers = self.best_so
        return self.get_k_centers()