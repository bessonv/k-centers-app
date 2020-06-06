from .algorithm import Algorithm, Vertex
from random import randint, sample

class KMeans(Algorithm):
    def __init__(self, points, k_num):
        super().__init__(points, k_num)
        self.cluster_centers = []
        self.clusters = []

    def set_initial_centers(self):
        self.clusters = []
        self.cluster_centers = [] 
        subset = sample(self.vertexes, self.k_num)
        # print('Start clusters:', len(subset))
        for center in subset:
            cluster = Cluster(center, [])
            self.clusters.append(cluster)
            # self.k_centers.append(center)
            self.cluster_centers.append(center)
        self.k_centers = self.cluster_centers[:]
        # random_pull = []
        # for i in range(self.k_num):
        #     random_int = random.randint(0, len(self.vertexes)-1)
        #     if (random in random_pull):
        #         random_int = random.randint(0, len(self.vertexes)-1)
        #     random_pull.append(random_int)
        #     self.claster_centers.append(self.vertexes[random_int])
        
    def set_clusters(self):
        for v in self.vertexes:
            nearest_cluster = self.clusters[0]
            min_distance = self.get_distance(v, self.clusters[0].center)
            for cluster in self.clusters:
                distance = self.get_distance(v, cluster.center)
                if (distance < min_distance):
                    min_distance = distance
                    nearest_cluster = cluster
            nearest_cluster.add_to_cluster(v)
    
    def change_weights(self):
        new_centers = []
        for cluster in self.clusters:
            cluster.calculate_weights()
            new_centers.append(cluster.get_center())
            cluster.reset_points() # clear clusters points
        if (new_centers == self.cluster_centers):
            return False
        else:
            self.cluster_centers = new_centers
            return True

    def run_algorithm(self):
        l_num = 5 # number of iterations
        for _ in range(l_num):
            self.set_initial_centers()
            not_equal = True
            while not_equal:
                self.set_clusters()
                not_equal = self.change_weights() # change weight for every claster
            if (self.max_distance(self.cluster_centers, self.vertexes) < self.max_distance(self.k_centers, self.vertexes)):
                self.k_centers = self.cluster_centers[:]
            # print('Ineration clusters:', len(self.clusters))
        return self.get_k_centers()

class Cluster:
    def __init__(self, center, points):
        self.center = center
        self.cluster_points = points
        self.cluster_points.append(center)

    def get_center(self):
        return self.center

    def add_to_cluster(self, point):
        if (point not in self.cluster_points):
            self.cluster_points.append(point)

    def reset_points(self):
        self.cluster_points = []
        self.cluster_points.append(self.center)

    def calculate_weights(self):
        x = 0
        y = 0
        n = len(self.cluster_points)
        for vertex in self.cluster_points:
            x = x + vertex.x
            y = y + vertex.y
        new_weight = Vertex([y/n, x/n], 'c')
        new_center = self.cluster_points[0]
        min_distance = self.cluster_points[0].distance(new_weight)
        for p in self.cluster_points:
            distance = p.distance(new_weight)
            if (distance < min_distance):
                min_distance = distance
                new_center = p
        self.center = new_center
        