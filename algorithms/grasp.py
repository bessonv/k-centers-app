from .algorithm import Algorithm, Vertex
from random import randint, sample, choice

class Grasp(Algorithm):
    def __init__(self, points, k_num, options):
        super().__init__(points, k_num, options)
        self.best_so = []
        self.alfa = 0

    # def greedy_solution(self):
    #     self.add_to_k_centers(self.vertexes[randint(0, len(self.vertexes)-1)])
    #     for _ in range(self.k_num-1):
    #         max_dist = 0
    #         for vertex in self.vertexes:
    #             subset_dist = self.subset_distance(vertex)
    #             if (max_dist <= subset_dist):
    #                 max_dist = subset_dist
    #                 further_vertex = vertex
    #         self.add_to_k_centers(further_vertex)
    #     return self.k_centers

    # def subset_distance(self, vertex):
    #     # min_dist = self.k_centers[0].distance(vertex)
    #     min_dist = self.get_distance(self.k_centers[0], vertex)
    #     center_dist = min_dist
    #     for center in self.k_centers:
    #         center_dist = self.get_distance(center, vertex)
    #         # center_dist = center.distance(vertex)
    #         if (center_dist <= min_dist):
    #             min_dist = center_dist
    #     return center_dist


    def greedy_solution(self, k_centers, vertexes, i):
        if (len(k_centers) >= self.k_num):
            return k_centers
        # min_distance = self.max_distance(k_centers, p_vertexes) #False
        min_distance = False
        # max_distance = min_distance #0
        # rcl_centers = []
        # print('iteration')
        for inx, vertex in enumerate(vertexes):
            p_k_centers = k_centers[:]
            p_vertexes = vertexes[:]
            p_k_centers.append(vertex)
            p_vertexes.remove(vertex)
            distance = self.max_distance(p_k_centers, p_vertexes)
            if (distance < min_distance or not min_distance):
                min_distance = distance
                p_center = vertexes[inx]
            # if (distance > max_distance or not max_distance):
            #     max_distance = distance
        # for inx, vertex in enumerate(vertexes):
        #     p_k_centers = k_centers[:]
        #     p_vertexes = vertexes[:]
        #     p_k_centers.append(vertex)
        #     p_vertexes.remove(vertex)
        #     distance = self.max_distance(p_k_centers, p_vertexes)
        #     if (distance == min_distance):# + self.alfa*(max_distance - min_distance)):
        #         rcl_centers.append(vertexes[inx])
        #         # print( min_distance)
        # p_center = choice(rcl_centers)
        # # print(len(rcl_centers))
        k_centers.append(p_center)
        vertexes.remove(p_center)
        return self.greedy_solution(k_centers, vertexes, i+1)

    def local_search(self, solution, distance):
        old_center = choice(solution)
        # for old_center in solution:
        candidate = solution[:]
        candidate.remove(old_center)
        min_dist = distance
        # new_v = False
        # new_solution = solution
        for v in self.vertexes:
            if (v is not old_center and v not in candidate):
                new_candidate = candidate + [v]
                cand_dist = self.max_distance(new_candidate, self.vertexes)
                if (cand_dist < min_dist):
                    min_dist = cand_dist
                    solution = new_candidate[:]
                    # new_v = v
            # if (self.max_distance(new_solution, self.vertexes) < self.max_distance(solution, self.vertexes)):
            #     solution = new_solution[:]
        # if (new_v):
        #     self.vertexes.remove(new_v)
        #     self.vertexes.append(old_center)
        if (min_dist >= distance):
            return solution
        else:
            return self.local_search(solution, min_dist)
    
    def run_algorithm(self):
        solution = self.greedy_solution(self.k_centers, self.vertexes, 1)
        # solution = self.greedy_solution()
        greedy_dist = self.max_distance(solution, self.vertexes)
        self.vertexes = self.start_vertexes[:]
        local_solution = self.local_search(solution, greedy_dist)
        local_dist = self.max_distance(local_solution, self.vertexes)
        self.vertexes = self.start_vertexes[:]
        if (greedy_dist <= local_dist):
            # local_solution = greedy_solution
            while local_dist < greedy_dist:
                local_solution = self.local_search(solution, greedy_dist)
                local_dist = self.max_distance(local_solution, self.vertexes)
                self.vertexes = self.start_vertexes[:]
        self.k_centers = local_solution
        return self.get_k_centers()