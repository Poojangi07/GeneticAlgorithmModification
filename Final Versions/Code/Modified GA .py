# Modified Genetic Algorithm for TSP.
# Map is initialised to Bays29

import copy
import random
import numpy as np
import statistics
from itertools import combinations

# import seaborn as sns
# import matplotlib.plot as plt

theMap = []

power_const = 0


def initialize_the_map():
    global theMap
    theMap = [[0] * 29] * 29
    theMap[0] = [0, 107, 241, 190, 124, 80, 316, 76, 152, 157, 283, 133, 113, 297, 228, 129, 348, 276, 188, 150, 65, 341, 184, 67, 221, 169, 108, 45, 167]
    theMap[1] = [107, 0, 148, 137, 88, 127, 336, 183, 134, 95, 254, 180, 101, 234, 175, 176, 265, 199, 182, 67, 42, 278, 271, 146, 251, 105, 191, 139, 79]
    theMap[2] = [241, 148, 0, 374, 171, 259, 509, 317, 217, 232, 491, 312, 280, 391, 412, 349, 422, 356, 355, 204, 182, 435, 417, 292, 424, 116, 337, 273, 77]
    theMap[3] = [190, 137, 374, 0, 202, 234, 222, 192, 248, 42, 117, 287, 79, 107, 38, 121, 152,  86,  68,  70, 137, 151, 239, 135, 137, 242, 165, 228, 205]
    theMap[4] = [124, 88, 171, 202, 0, 61, 392, 202,  46, 160, 319, 112, 163, 322, 240, 232, 314, 287, 238, 155,  65, 366, 300, 175, 307,  57, 220, 121,  97]
    theMap[5] = [80, 127, 259, 234,  61, 0, 386, 141,  72, 167, 351,  55, 157, 331, 272, 226, 362, 296, 232, 164,  85, 375, 249, 147, 301, 118, 188,  60, 185]
    theMap[6] = [316, 336, 509, 222, 392, 386, 0, 233, 438, 254, 202, 439, 235, 254, 210, 187, 313, 266, 154, 282, 321 ,298, 168, 249,  95, 437, 190, 314, 435]
    theMap[7] = [76, 183, 317, 192, 202, 141, 233, 0, 213, 188, 272, 193, 131, 302, 233,  98, 344, 289 ,177, 216, 141, 346, 108,  57, 190, 245,  43,  81, 243]
    theMap[8] = [152, 134, 217, 248,  46,  72, 438, 213, 0, 206, 365,  89, 209, 368, 286, 278, 360, 333, 284, 201, 111, 412, 321, 221, 353,  72, 266, 132, 111]
    theMap[9] = [157,  95, 232,  42, 160, 167, 254, 188, 206, 0, 159, 220,  57, 149,  80, 132, 193, 127, 100,  28,  95, 193, 241, 131, 169, 200, 161, 189, 163]
    theMap[10] = [283, 254, 491, 117, 319, 351, 202, 272, 365, 159, 0, 404, 176, 106,  79, 161, 165, 141,  95, 187, 254, 103, 279, 215, 117, 359, 216, 308, 322]
    theMap[11] = [133, 180, 312, 287, 112,  55, 439, 193,  89, 220, 404, 0, 210, 384, 325, 279, 415, 349, 285, 217, 138, 428, 310, 200, 354, 169, 241, 112, 238]
    theMap[12] = [113, 101, 280,  79, 163, 157, 235, 131, 209,  57, 176, 210, 0, 186, 117,  75, 231, 165,  81,  85,  92, 230, 184,  74, 150, 208, 104, 158, 206]
    theMap[13] = [297, 234, 391, 107, 322, 331, 254, 302, 368, 149, 106, 384, 186, 0, 69, 191,  59,  35, 125, 167, 255,  44, 309, 245, 169, 327, 246, 335, 288]
    theMap[14] = [228, 175, 412,  38, 240, 272, 210, 233, 286,  80,  79, 325, 117,  69, 0, 122, 122,  56,  56, 108, 175, 113, 240, 176, 125, 280, 177, 266, 243]
    theMap[15] = [129, 176, 349, 121, 232, 226, 187,  98, 278, 132, 161, 279,  75, 191, 122, 0, 244, 178,  66, 160, 161, 235, 118,  62,  92, 277,  55, 155, 275]
    theMap[16] = [348, 265, 422, 152, 314, 362, 313, 344, 360, 193, 165, 415, 231,  59, 122, 244, 0, 66, 178, 198, 286,  77, 362, 287, 228, 358, 299, 380, 319]
    theMap[17] = [276, 199, 356,  86, 287, 296, 266, 289, 333, 127, 141, 349, 165,  35,  56, 178,  66, 0, 112, 132, 220,  79, 296, 232, 181, 292, 233, 314, 253]
    theMap[18] = [188, 182, 355,  68, 238, 232, 154, 177, 284, 100,  95, 285,  81, 125,  56,  66, 178, 112, 0, 128, 167, 169, 179 ,120,  69, 283, 121, 213, 281]
    theMap[19] = [150,  67, 204,  70, 155, 164, 282, 216, 201,  28, 187, 217,  85, 167, 108, 160, 198, 132, 128, 0, 88, 211, 269, 159, 197, 172, 189, 182, 135]
    theMap[20] = [65,  42, 182, 137,  65,  85, 321, 141, 111,  95, 254, 138,  92, 255, 175, 161, 286, 220, 167,  88, 0, 299, 229, 104, 236, 110, 149,  97, 108]
    theMap[21] = [341, 278, 435, 151, 366, 375, 298, 346, 412, 193, 103, 428, 230,  44, 113, 235,  77,  79, 169, 211, 299, 0 ,353, 289, 213, 371, 290, 379, 332]
    theMap[22] = [184, 271, 417, 239, 300, 249, 168, 108, 321, 241, 279, 310, 184, 309, 240, 118, 362, 296, 179, 269, 229, 353, 0, 121, 162, 345,  80, 189, 342]
    theMap[23] = [67, 146, 292, 135, 175, 147, 249,  57, 221, 131, 215, 200,  74, 245, 176,  62, 287, 232, 120, 159, 104, 289, 121, 0, 154, 220,  41,  93, 218]
    theMap[24] = [221, 251, 424, 137, 307, 301,  95, 190, 353, 169, 117, 354, 150, 169, 125,  92, 228, 181,  69, 197, 236, 213, 162, 154, 0, 352, 147, 247, 350]
    theMap[25] = [169, 105, 116, 242,  57, 118, 437, 245,  72, 200, 359, 169, 208, 327, 280, 277, 358, 292, 283, 172, 110, 371, 345, 220, 352, 0, 265, 178,  39]
    theMap[26] = [108, 191, 337, 165, 220, 188, 190,  43, 266, 161, 216, 241, 104, 246, 177,  55, 299, 233, 121, 189, 149, 290,  80,  41, 147, 265, 0, 124, 263]
    theMap[27] = [45, 139, 273, 228, 121,  60, 314,  81, 132, 189, 308, 112, 158, 335, 266, 155, 380, 314, 213, 182,  97, 379, 189,  93, 247, 178, 124, 0, 199]
    theMap[28] = [167,  79,  77, 205,  97, 185, 435, 243, 111, 163, 322, 238, 206, 288, 243, 275, 319, 253, 281, 135, 108, 332, 342, 218, 350,  39, 263, 199, 0]

    theMap

    return theMap


def count_digits(val):
    count = 0
    while val != 0:
        val //= 10
        count += 1
    return count


def getNumofCommonSubstr(str1, str2):  # doesn't understand reverse strings
    lstr1 = len(str1)
    lstr2 = len(str2)
    record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  #
    maxNum = 0  # Maximum matching length
    max_end = 0  # 's termination
    max_start = 0  # match starting bit
    map_maxstr = {}  # key is the starting position, value is the maximum matching string
    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                record[i + 1][j + 1] = record[i][j] + 1
                if record[i + 1][j + 1] > maxNum:  # Get the maximum match length
                    maxNum = record[i + 1][j + 1]  # Record the starting position of the maximum matching length
                    p = i + 1
                    max_start = i + 1 - maxNum
                    map_maxstr[max_start] = str1[p - maxNum:p]
                    maxNum = 0
    # return str1[p - maxNum:p], maxNum
    return map_maxstr


def find_common_subtours(ind1_route, ind2_route):
    subtours = []

    s1 = ''.join(map(str, ind1_route))
    s2 = ''.join(map(str, ind2_route))

    map_maxstr = getNumofCommonSubstr(s1, s2)  # string
    for m in map_maxstr:
        if len(str(map_maxstr.get(m))) > 1:
            s = map_maxstr.get(m)
            s_ls = [x for x in str(s)]
            subtours.append(s_ls)

    return subtours


class Individual:

    def __init__(self):
        self.route = [0]
        self.distance = -1.0
        self.fitness = -1.0

    def create_gene(self):  # gives gene to the individual - i.e. route
        n = len(theMap)
        i = 0
        while i < n - 1:  # 0 is already added in route, hence find n-1 elements.
            ls_all = np.nonzero(theMap[self.route[
                i]])  # should be accessed as possible_vertices[0], because its 0th element consists of the tuple
            possible_vertices = list(filter(lambda x: x not in self.route, ls_all[0]))
            if len(possible_vertices) == 0:
                break
            while True:
                proposed_vertex = random.choice(possible_vertices)  # proposed index of possible_vertices
                if proposed_vertex not in self.route:  # the next city should not be already in route
                    break
            self.route.append(proposed_vertex)
            i += 1

    def append_sub_route(self, subroute):       # subroute is list of cities, ideal_len is no of cities
        subroute = [int(i) for i in subroute]       # subroute elements were strings
        if 0 in subroute:
            self.route.clear()
        self.route = self.route + subroute

    def find_distance(self):
        score = 0.0
        for cur in range(1, len(self.route)):
            score += theMap[self.route[cur - 1]][self.route[cur]]
        score += theMap[0][self.route[-1]]
        self.distance = score

    def find_fitness(self):
        fit = 1 / self.distance
        fit = round(fit, power_const + 2)
        self.fitness = fit * pow(10, power_const)

    def find_attributes(self):
        self.find_distance()
        self.find_fitness()

    def create_a_member(self):
        self.create_gene()
        self.find_attributes()


class Population:

    def __init__(self, size):
        self.populationList = []
        self.size = size

    def create_starting_population(self):
        global power_const

        # create first member
        inv_f = Individual()
        inv_f.create_gene()
        inv_f.find_distance()

        power_const = count_digits(inv_f.distance)
        inv_f.find_fitness()
        self.populationList.append(inv_f)

        for i in range(1, self.size):
            inv = Individual()
            inv.create_a_member()
            self.populationList.append(inv)

    def find_topper(self):
        topper = self.populationList[0]
        for individual in self.populationList:
            if topper.distance > individual.distance:
                topper = individual
        return topper

    def print_population(self):
        for individual in self.populationList:
            print("Route: ", individual.route, "\tDistance: ", individual.distance, "\tFitness: ", individual.fitness)

    def find_total_fitness(self):
        total_sum = 0
        for individual in self.populationList:
            total_sum += individual.fitness
        return total_sum

    def rank_population(self):
        self.populationList.sort(key=lambda x: x.distance)

    def clear_population(self):
        self.populationList.clear()


class Genetic_Algorithm:

    def __init__(self, size):
        self.size = size
        self.current_population = Population(self.size)
        self.new_population = Population(self.size)
        self.elites_set = []                    # array of individuals
        self.subtour_set = []

    def find_routeLength(self):  # routeLength = gene length = no. of cities
        return len(self.current_population.populationList[0].route)

    def perform_natural_selection(self, elitismPercentage):
        elites_number = round(self.size * elitismPercentage)
        for i in range(0, elites_number):
            self.new_population.populationList.append(self.current_population.populationList[i])

    def roulette_wheel_selection(self):
        range_limit = round(self.current_population.find_total_fitness())
        random_int = random.randint(0, range_limit)
        partial_sum = 0.0
        parent = self.current_population.populationList[0]
        for individual in self.current_population.populationList:
            partial_sum += individual.fitness
            if partial_sum >= random_int:
                parent = individual
                break
        return parent

    def crossover_from_otherParent(self, offspring, otherParent, o, p):
        # changing the offspring in this function also changes in the main crossover function.
        # because, the paremeter sent is not a new list, but just a pointer to the existing list. So convinient!
        routeLength = self.find_routeLength()

        if otherParent[p] not in offspring:
            offspring[o] = otherParent[p]
            o = (o + 1) % routeLength
            p = (p + 1) % routeLength
        else:
            p = (p + 1) % routeLength
        return o, p  # return new indices

    def order_crossover(self, parent1, parent2):  # adding probability left

        routeLength = self.find_routeLength()
        offspring1 = Individual()
        offspring2 = Individual()
        offspring1_route = [-1] * routeLength
        offspring2_route = [-1] * routeLength
        cut1 = random.randint(0, int(routeLength / 2))  # int(routeLength/2)
        cut2 = random.randint(int(routeLength / 2), routeLength - 1)

        # loop to add crossover section elements
        for i in range(cut1, cut2 + 1):  # eg. |x x x|a b c|x x x|       Loop to get a,b,c for both offsprings
            offspring1_route[i] = parent1.route[i]
            offspring2_route[i] = parent2.route[i]

        # Counters:
        o1 = (cut2 + 1) % routeLength  # o1, o2 are offspring index counters
        o2 = (cut2 + 1) % routeLength
        p1 = (cut2 + 1) % routeLength  # p1, p2 are parent index counters
        p2 = (cut2 + 1) % routeLength
        while o1 != cut1 or o2 != cut1:  # Loop to get x, i.e., remaining elements
            if o1 != cut1:
                o1, p2 = self.crossover_from_otherParent(offspring1_route, parent2.route, o1, p2)
            if o2 != cut1:
                o2, p1 = self.crossover_from_otherParent(offspring2_route, parent1.route, o2, p1)

        offspring1.route = offspring1_route
        offspring2.route = offspring2_route
        offspring1.find_attributes()
        offspring2.find_attributes()

        return offspring1, offspring2

    def mutation_on_individual(self, individual):
        pt1 = random.randint(1, int(len(individual.route) / 2))
        pt2 = random.randint(pt1 + 1, len(individual.route) - 1)
        while pt1 < pt2:
            individual.route[pt1], individual.route[pt2] = individual.route[pt2], individual.route[pt1]
            pt1 += 1
            pt2 -= 1
        individual.find_distance()
        return individual

    def mutation_on_population(self, prob_of_mutation):  # probability handled
        random_number = random.randint(0, 1)
        for i in range(0, self.size):
            if random_number < prob_of_mutation:
                individual = random.choice(self.current_population.populationList)
                individual = self.mutation_on_individual(individual)
                self.current_population.populationList[i] = individual

    def convergence_reached(self, threshold):
        distance_list = []
        for individual in self.current_population.populationList:
            distance_list.append(individual.distance)
        population_std = statistics.pstdev(distance_list)
        if population_std < threshold:
            return True  # convergence reached

    def generate_subtour_of_new_elites(self, new_elites_set):
        comb = combinations(new_elites_set, 2)
        for pair in comb:
            subtours = find_common_subtours(pair[0], pair[1])
            for sub in subtours:
                if sub not in self.subtour_set:
                    self.subtour_set.append(sub)

    def generate_subtour_of_old_and_new_elites(self, new_elites_set):
        list1 = self.subtour_set
        list2 = new_elites_set
        comb = [(list1[i], list2[j]) for i in range(len(list1)) for j in range(len(list2))]
        for pair in comb:
            subtours = find_common_subtours(pair[0], pair[1])
            for sub in subtours:
                if sub not in self.subtour_set:
                    self.subtour_set.append(sub)

            # output.extend(y for y in list2 if y not in output) - remove duplicate

    def modified_crossover(self, parent1_route, parent2_route):
        offspring_set = []
        routeLength = self.find_routeLength()
        for subtour in self.subtour_set:         # add the subtour directly to the offspring
            off = Individual()
            off.append_sub_route(subtour)
            index = len(off.route)

            while len(off.route) < routeLength:
                off.route.append(0)

            off_2 = Individual()
            off_2.route = copy.deepcopy(off.route)
            in1 = index
            in2 = index
            p = 0
            while in1 < routeLength-1:
                in1, p = self.crossover_from_otherParent(off.route, parent1_route, in1, p)
            while in2 < routeLength-1:
                in2, p = self.crossover_from_otherParent(off_2.route, parent2_route, in2, p)

            # compare and select
            off.find_distance()
            off_2.find_distance()
            if off.distance <= off_2.distance:
                off.find_fitness()
                offspring_set.append(off)
            else:
                off_2.find_fitness()
                offspring_set.append(off_2)
        return offspring_set


    def genetic_algorithm(self):

        no_of_iterations = 500
        no_of_couples = 2
        mutationProbability = 0.05
        elitismPercentage = 0.3
        convergenceThreshold = 0.3
        subtour_flag = False
        elites_learning_freq = 2

        self.current_population.create_starting_population()  # Step 1. Create Starting Population
        for i in range(0, no_of_iterations):  # 1. run GA for given no of iterations
            print("Iteration: ",i)

            self.current_population.rank_population()

            topper = self.current_population.find_topper()
            print("The best route so far is: ", topper.route, "\t with distance: ", topper.distance)

            self.new_population.populationList.append(topper)
            self.new_population.populationList.append(self.current_population.populationList[1])

            # addition in elites_set
            new_elites_set = []                 # should have routes of elites and not individuals itself.
            for j in range(0, elites_learning_freq):
                if self.current_population.populationList[0].route not in self.elites_set:
                    new_elites_set.append(self.current_population.populationList[j].route)
            if len(new_elites_set) != 0:
                subtour_flag = True

            self.generate_subtour_of_new_elites(new_elites_set)
            self.generate_subtour_of_old_and_new_elites(new_elites_set)


            if self.convergence_reached(convergenceThreshold):  # 2. or run till convergence reached
                print("Convergence Reached.")
                break

            # creating new population
            self.perform_natural_selection(elitismPercentage)


            for crossoverIteration in range(0, no_of_couples):
                parent01 = self.roulette_wheel_selection()  # Step 2. Selection
                parent02 = self.roulette_wheel_selection()

                child1, child2 = self.order_crossover(parent01, parent02)  # Step 3. Crossover
                self.new_population.populationList.append(child1)
                self.new_population.populationList.append(child2)

                if subtour_flag:                # new subtours added in this iteration
                    child_set = self.modified_crossover(parent01.route, parent02.route)
                    self.new_population.populationList + child_set

            self.mutation_on_population(mutationProbability)  # Step 5. Mutation

            # add randomly in remaining places - if remained
            while len(self.new_population.populationList) < self.size:
                inv = Individual()
                inv.create_a_member()
                self.new_population.populationList.append(inv)

            self.current_population.clear_population()
            self.current_population = copy.deepcopy(self.new_population)
            self.new_population.clear_population()
            print('-' * 20)

        print("End")


if __name__ == '__main__':
    initialize_the_map()
    gen = Genetic_Algorithm(10)
    gen.genetic_algorithm()

