import sys, getopt, json
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
    with open('./static/json/' + inputfile) as json_file:
        data = json.load(json_file)
        plist = data["vertexes"]

    algorithms = {
        'two_approx': TwoApprox,
        'greedy': Greedy,
        'k_means': KMeans,
        'tabu_search': TabuSearch,
        'grasp': Grasp
    }

    print('Vertexes:', len(plist))
    print('K-Centers: ', k_num)
    
    for alg_type in algorithms:
        algorithm = algorithms.get(alg_type, lambda: "Invalid algorithm name")(plist, k_num, [{'name': 'iterations', 'value': 5}])
        k_list = algorithm.run_algorithm()
        # l_list = algorithm.get_l_list()
        max_distance = algorithm.get_max_distance()

        print('-----------')
        print('Algorithm:', alg_type)
        print('Max edge distance: ', max_distance)

if __name__ == "__main__":
    main(sys.argv[1:])
