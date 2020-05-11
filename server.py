import sys
sys.path.append(".")

from flask import Flask
from flask import request, render_template

from algorithms import Algorithm, Vertex

app = Flask(__name__)

def findNorthPoint(plist):
    first = plist[0]
    max_y_coord = plist[0]["coordinates"][0]
    for point in plist:
        if point["coordinates"][0] > max_y_coord:
            first = point
            max_y_coord = point["coordinates"][0]
    return first

def findSouthPoint(plist):
    first = plist[0]
    min_y_coord = plist[0]["coordinates"][0]
    for point in plist:
        if point["coordinates"][0] < min_y_coord:
            first = point
            min_y_coord = point["coordinates"][0]
    return first

def find_K_north_points(plist, k):
    south_point = findSouthPoint(plist)
    klist = [south_point]
    max_y_coord = south_point["coordinates"][0]
    for point in plist:
        if point["coordinates"][0] > max_y_coord:
            klist.insert(0, point)
            if (len(klist) > k):
                klist.pop()
            max_y_coord = point["coordinates"][0]
    return klist


@app.route('/', methods=['POST', 'GET'])
def api():
    if request.method == 'POST': 
        data = request.get_json()
        plist = data["mlist"]
        k = data["knum"]

        algorithm = Algorithm(plist, k)
        k_list = algorithm.greedyApprox()
        l_list = algorithm.get_l_list()

        # l_groups = []
        # k_list = find_K_north_points(plist, k)
        
        # for k_point in k_list:
        #     l_list = []
        #     for point in plist:
        #         l_list.append([k_point["coordinates"], point["coordinates"]])
        #     l_groups.append(l_list)

        return {
            "klist": k_list,
            "llist": l_list
            # "lgroups": l_groups
        }
    elif request.method == 'GET':
        return render_template('index.html')
    else:
        return {
            "error": 'Not POST or GET method'
        }
