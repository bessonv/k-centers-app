import sys, json, random
from datetime import datetime

data = {}
num = int(sys.argv[1])
amount = int(sys.argv[2])
for a in range(amount):
    data['vertexes'] = []
    random.seed(a)
    for n in range(num):
        lat = round(random.uniform(50.0, 65.0), 6)
        lon = round(random.uniform(15.0, 90.0), 6)
        data['vertexes'].append({
            'id': n,
            'coordinates': [lat, lon]
        })
    name = 'vertex_set_' + str(num) + '_' + str(a)

    with open('./static/json/' + name + '.json', 'w') as outfile:
        json.dump(data, outfile)
