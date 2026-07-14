# Genetic Algorithm for TSP.
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
    theMap = [[0] * 5] * 5
    theMap[0] = [0,  3,  4,  2,  7]
    theMap[1] = [3,  0,  4,  6,  3]
    theMap[2] = [4,  4,  0,  5,  8]
    theMap[3] = [2,  6,  5,  0,  6]
    theMap[4] = [7,  3,  8,  6,  0]

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
            self.crossover_from_otherParent(off.route, parent1_route, index, 0)
            self.crossover_from_otherParent(off_2.route, parent2_route, index, 0)

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

        no_of_iterations = 9
        no_of_couples = 2
        mutationProbability = 0.05
        elitismPercentage = 0.3
        convergenceThreshold = 0.3
        subtour_flag = False
        elites_learning_freq = 2

        self.current_population.create_starting_population()  # Step 1. Create Starting Population
        for i in range(0, no_of_iterations):  # 1. run GA for given no of iterations

            self.current_population.rank_population()

            topper = self.current_population.find_topper()
            print("The best route so far is: ", topper.route, "\t with distance: ", topper.distance)

            # addition in elites_set
            new_elites_set = []                 # should have routes of elites and not individuals itself.
            for i in range(0, elites_learning_freq):
                if self.current_population.populationList[0].route not in self.elites_set:
                    new_elites_set.append(self.current_population.populationList[i].route)
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

