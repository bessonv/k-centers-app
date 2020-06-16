import numpy
import sys, json, random

num = int(sys.argv[1])
amount = int(sys.argv[2])
n = num
a = amount

clasters = {
    'c1': {
        'prob': 0.5,
        'coord': {
            'lat': [],
            'lon': []
        }
    }
}

prob2 = [
    [0.10, 0.17, 0.19, 0.25, 0.29],
    [0.06, 0.07, 0.12, 0.21, 0.54],
    [0.09, 0.14, 0.16, 0.17, 0.44],
    [0.02, 0.05, 0.09, 0.70, 0.14],
    [0.07, 0.10, 0.12, 0.22, 0.49],
    [0.03, 0.11, 0.15, 0.17, 0.54],
    [0.06, 0.13, 0.14, 0.28, 0.39],
    [0.04, 0.05, 0.07, 0.29, 0.55],
    [0.03, 0.13, 0.20, 0.21, 0.43],
    [0.11, 0.13, 0.16, 0.18, 0.42]
]

prob = [
    [[0, 0.1], [0.1, 0.27], [0.27, 0.46], [0.46, 0.71], [0.71, 1.0]], 
    [[0, 0.06], [0.06, 0.13], [0.13, 0.25], [0.25, 0.45999999999999996], [0.45999999999999996, 1.0]], 
    [[0, 0.09], [0.09, 0.23], [0.23, 0.39], [0.39, 0.56], [0.56, 1.0]], 
    [[0, 0.02], [0.02, 0.07], [0.07, 0.16], [0.16, 0.86], [0.86, 1.0]], 
    [[0, 0.07], [0.07, 0.17], [0.17, 0.29000000000000004], [0.29000000000000004, 0.51], [0.51, 1.0]], 
    [[0, 0.03], [0.03, 0.14], [0.14, 0.29000000000000004], [0.29000000000000004, 0.4600000000000001], [0.4600000000000001, 1.0]], 
    [[0, 0.06], [0.06, 0.19], [0.19, 0.33], [0.33, 0.6100000000000001], [0.6100000000000001, 1.0]], 
    [[0, 0.04], [0.04, 0.09], [0.09, 0.16], [0.16, 0.44999999999999996], [0.44999999999999996, 1.0]], 
    [[0, 0.03], [0.03, 0.16], [0.16, 0.36], [0.36, 0.57], [0.57, 1.0]], 
    [[0, 0.11], [0.11, 0.24], [0.24, 0.4], [0.4, 0.5800000000000001], [0.5800000000000001, 1.0]]
]

# prob = [[0.10, 0.17, 0.19, 0.25, 0.29]]
# res = []
# for pr in prob:
#     result = []
#     a = 0
#     for p in pr:
#         b = a + p
#         result.append([a, b])
#         a = b
#     res.append(result)

# print(res)

claster_coords = [
    {'lat': [56.0, 62.0], 'lon': [30.0, 45.0]},
    {'lat': [50.0, 56.0], 'lon': [30.0, 46.0]},
    {'lat': [50.0, 56.0], 'lon': [46.0, 63.0]},
    {'lat': [56.0, 63.0], 'lon': [63.0, 80.0]},
    {'lat': [53.0, 63.0], 'lon': [80.0, 92.0]}
]

for a in range(amount):
    data = {}
    data['vertexes'] = []
    random.seed(a)
    for n in range(num):
        rand = round(random.uniform(0, 1), 3)
        for i, p in enumerate(prob[a]):
            if (p[0] < rand < p[1] or (i == len(prob[a]) - 1)):
                coords = claster_coords[i]
                lat = round(random.uniform(coords['lat'][0], coords['lat'][1]), 6)
                lon = round(random.uniform(coords['lon'][0], coords['lon'][1]), 6)
                data['vertexes'].append({
                    'id': n,
                    'coordinates': [lat, lon]
                })
                break
# print(len(data['vertexes']))
    # for i in data['vertexes']:
    #     print('(' + str(round(i['coordinates'][1], 3)) + ', ' + str(round(i['coordinates'][0], 3)) + ')')
    name = 'claster_vertex_set_' + str(num) + '_' + str(a)
    with open('./static/json/' + name + '.json', 'w') as outfile:
        json.dump(data, outfile)