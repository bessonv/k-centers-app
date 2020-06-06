from .algorithm import Algorithm, Vertex
from random import randint, sample, choice

class TabuSearch(Algorithm):
    def __init__(self, points, k_num):
        super().__init__(points, k_num)
        self.tabu_list = []
        self.best_so = []
        self.best_candidate = []

    def set_initial_solution(self):
        self.tabu_list = []
        subset = sample(self.vertexes, self.k_num)
        self.best_so = subset
        self.best_candidate = subset
        self.tabu_list.append(subset)
        self.solution_distance = self.max_distance(self.best_so, self.vertexes)

    def add_to_tabu_list(self, k_centers):
        tabu_length = 5
        self.tabu_list.append(k_centers)
        if (len(self.tabu_list) >= tabu_length):
            self.tabu_list.pop(0)

    def is_in_tabu(self, candidate):
        for tabu_so in self.tabu_list:
            if (set(tabu_so) == set(candidate)):
                return True
        return False

    def change_candidate(self):
        old_center = choice(self.best_candidate)
        candidate = self.best_candidate[:]
        candidate.remove(old_center)
        min_dist = False
        for v in self.vertexes:
            if (v is not old_center and v not in candidate):
                new_candidate = candidate + [v]
                if (min_dist == False):
                    min_dist = self.max_distance(new_candidate, self.vertexes)
                if not self.is_in_tabu(new_candidate):
                    cand_dist = self.max_distance(new_candidate, self.vertexes)
                    if (cand_dist < min_dist):
                        min_dist = cand_dist
                        self.best_candidate = new_candidate
        return min_dist

    def run_algorithm(self):
        self.set_initial_solution()
        iterations = 25
        for _ in range(iterations):
            candidate_distance = self.change_candidate()
            if (self.solution_distance > candidate_distance):
                self.best_so = self.best_candidate
                self.solution_distance = candidate_distance
            self.add_to_tabu_list(self.best_candidate)
        self.k_centers = self.best_so
        return self.get_k_centers()
