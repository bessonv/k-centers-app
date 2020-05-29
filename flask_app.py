import sys
sys.path.append(".")

from flask import Flask
from flask import request, render_template

from algorithms import Algorithm, Vertex, TwoApprox, Greedy, KMeans

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def api():
    if request.method == 'POST': 
        data = request.get_json()
        plist = data["mlist"]
        k = data["knum"]
        alg_type = data["algorithm"]

        algorithms = {
            'two_approx': TwoApprox,
            'greedy': Greedy,
            'k_means': KMeans
        }

        algorithm = algorithms.get(alg_type, lambda: "Invalid algorithm name")(plist, k)

        # algorithm = TwoApprox(plist, k)
        k_list = algorithm.run_algorithm()
        l_list = algorithm.get_l_list()
        max_distance = algorithm.get_max_distance()

        # l_groups = []
        # k_list = find_K_north_points(plist, k)
        
        # for k_point in k_list:
        #     l_list = []
        #     for point in plist:
        #         l_list.append([k_point["coordinates"], point["coordinates"]])
        #     l_groups.append(l_list)

        return {
            "klist": k_list,
            "llist": l_list,
            "distance": max_distance
        }
    elif request.method == 'GET':
        return render_template('index.html')
    else:
        return {
            "error": 'Not POST or GET method'
        }
