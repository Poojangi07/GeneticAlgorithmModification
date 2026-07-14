# Basic Genetic Algorithm for TSP.
# att48

import copy
import random
import numpy as np
import statistics
import pandas as pd

# import seaborn as sns
# import matplotlib.plot as plt

# contains original code, not with modified crossover

theMap = []

power_const = 0

def initialize_the_map():
    global theMap
    df = pd.read_csv(r"D:\Poojangi\Research Paper\Step 7 - Submitting Paper\Datasets\att48.csv")
    theMap = df.values.tolist()
    return theMap


def count_digits(val):
    count = 0
    while val != 0:
        val //= 10
        count += 1
    return count


class Individual:

    def __init__(self):
        self.route = [0]
        self.distance = -1.0
        self.fitness = -1.0

    def create_gene(self):  # gives gene to the individual - i.e. route
        n = len(theMap)
        i = 0
        while i < n-1:          # 0 is already added in route, hence find n-1 elements.
            ls_all = np.nonzero(theMap[self.route[i]])  # should be accessed as possible_vertices[0],
                                                        # because its 0th element consists of the tuple
            possible_vertices = list(filter(lambda x: x not in self.route, ls_all[0]))
            if len(possible_vertices) == 0:
                break
            while True:
                proposed_vertex = random.choice(possible_vertices)  # proposed index of possible_vertices
                if proposed_vertex not in self.route:  # the next city should not be already in route
                    break
            self.route.append(proposed_vertex)
            i += 1

    def find_distance(self):
        score = 0.0
        for cur in range(1, len(self.route)):
            score += theMap[self.route[cur - 1]][self.route[cur]]
        score += theMap[0][self.route[-1]]
        self.distance = score

    def find_fitness(self):
        fit = 1/self.distance
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

    def genetic_algorithm(self):

        no_of_iterations = 2000
        no_of_couples = 2
        mutationProbability = 0.05
        elitismPercentage = 0.3
        convergenceThreshold = 0.3

        self.current_population.create_starting_population()  # Step 1. Create Starting Population
        for i in range(0, no_of_iterations):  # 1. run GA for given no of iterations

            print("Iteration No: ", i)

            self.current_population.rank_population()

            topper = self.current_population.find_topper()
            print("The best route so far is: ", topper.route, "\t with distance: ", topper.distance)

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
