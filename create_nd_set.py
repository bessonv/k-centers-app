import numpy
import sys, json, random

num = int(sys.argv[1])
amount = int(sys.argv[2])
n = num
a = amount
for a in range(amount):
    random.seed(a)
    lat = round(random.uniform(50.0, 65.0), 6)
    lon = round(random.uniform(15.0, 90.0), 6)
    normal_dist = numpy.random.normal(loc=[lon, lat], scale=[15, 5], size=(int(num), 2))

    data = {}
    data['vertexes'] = []
    i = 0
    for n in normal_dist:
        data['vertexes'].append({
            'id': i,
            'coordinates': [abs(n[1]), abs(n[0])]
        })
        i = i + 1
    # for i in normal_dist:
    #     print('(' + str(round(i[0], 3)) + ', ' + str(round(i[1], 3)) + ')')
    name = 'normal_vertex_set_' + str(num) + '_' + str(a)
    with open('./static/json/' + name + '.json', 'w') as outfile:
            json.dump(data, outfile)
