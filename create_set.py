import sys, json, random

data = {}
num = int(sys.argv[1])
data['vertexes'] = []

for n in range(num):
    lat = round(random.uniform(50.0, 65.0), 6)
    lon = round(random.uniform(15.0, 90.0), 6)
    data['vertexes'].append({
        'id': n,
        'coordinates': [lat, lon]
    })
name = 'vertex_set_' + str(num)

with open('./static/json/' + name + '.json', 'w') as outfile:
    json.dump(data, outfile)
