from flask import Flask
from flask import request, render_template

from algorithms import TwoApprox, Greedy, KMeans, TabuSearch, Grasp

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def api():
    if request.method == 'POST': 
        data = request.get_json()
        plist = data["mlist"]
        k = data["knum"]
        options = data["options"]
        alg_type = data["algorithm"]

        algorithms = {
            'two_approx': TwoApprox,
            'greedy': Greedy,
            'k_means': KMeans,
            'tabu_search': TabuSearch,
            'grasp': Grasp
        }

        algorithm = algorithms.get(alg_type, lambda: "Invalid algorithm name")(plist, k, options)
        k_list = algorithm.run_algorithm()
        p_list = algorithm.get_l_list()
        path = algorithm.get_max_distance()

        return {
            "klist": k_list,
            "plist": p_list,
            "path": path
        }
    elif request.method == 'GET':
        return render_template('index.html')
    else:
        return {
            "error": 'Not POST or GET method'
        }
