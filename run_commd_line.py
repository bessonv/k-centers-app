import sys, getopt, json, time
from algorithms import TwoApprox, Greedy, KMeans, TabuSearch, Grasp

def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:k:",["ifile=", "knum="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run_commd_line.py -i <input-file> -k <k-num>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-k", "--knum"):
            k_num = int(arg)
    # with open('./static/json/' + inputfile) as json_file:
    #     data = json.load(json_file)
    #     plist = data["vertexes"]

    algorithms = {
        'two_approx': TwoApprox,
        'greedy': Greedy,
        'k_means': KMeans,
        'tabu_search': TabuSearch,
        'grasp': Grasp
    }

    # print('Vertexes:', len(plist))
    k_nums = []
    for i in range(k_num):
        # k_nums = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        k_nums.append((i+1))
    print(k_nums)

    iterations = 10;
    # max_iterations = 100;
    # iterations = []
    # for i in range(max_iterations):
    #     iterations.append(i+1)
    plist_set = []
    
    for i in range(10):
        with open('./static/json/' + inputfile + '_' + str(i) + '.json') as json_file:
            data = json.load(json_file)
            plist_set.append(data["vertexes"])

    alg_results = {
        'two_approx': [],
        'greedy': [],
        'k_means': [],
        'tabu_search': [],
        'grasp': []
    }
    
    for alg_type in algorithms:
        # distance = ''
        print('-----------')
        print('Algorithm:', alg_type)
        alg_results = []
        for k_number in k_nums:
            knum_results = []
            for i in range(10):
                # print('K-Centers: ', k_num)
                # for iteration in iterations:
                algorithm = algorithms.get(alg_type, lambda: "Invalid algorithm name")(plist_set[i], k_number, [{'name': 'iterations', 'value': iterations}])
                # tic = time.perf_counter()
                k_list = algorithm.run_algorithm()
                # toc = time.perf_counter()
                # l_list = algorithm.get_l_list()
                max_distance = algorithm.get_max_distance()
                knum_results.append(max_distance['distance'])
            avg = sum(knum_results) / len(knum_results)
            alg_results.append(round(avg, 3))
            print(k_number, 'center is done')
        for result in alg_results:
            print(result)
        # distance = distance + ' ' + str(round(max_distance['distance'], 3))
        # print(f"{toc - tic:0.4f}")
                # print('Max edge distance: ')
        # print(round(max_distance['distance'], 3))


if __name__ == "__main__":
    main(sys.argv[1:])
