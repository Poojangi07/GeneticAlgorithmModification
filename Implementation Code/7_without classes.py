# First version

# Genetic Algorithm for TSP.
# import copy
import random
import numpy as np
import statistics
# import seaborn as sns
# import matplotlib.plot as plt


theMap = []


def initialize():
    global theMap
    theMap = [[0]*4]*4
    theMap[0] = [0, 20, 10, 12]
    theMap[1] = [20, 0, 15, 11]
    theMap[2] = [10, 15, 0, 17]
    theMap[3] = [12, 11, 17, 0]

    return theMap


def create_new_member():      # this creates new route/individual
    n = len(theMap)
    route = [0]
    i = 1
    while i < n:
        possible_vertices = np.nonzero(theMap[route[i - 1]])                    # should be accessed as possible_vertices[0], because its 0th element consists of the tuple
        while True:
            proposed_ver_index = random.randint(0, len(possible_vertices)+1)    # proposed index of possible_vertices
            if possible_vertices[0][proposed_ver_index] not in route:           # the next city should not be already in route
                break
        route.append(possible_vertices[0][proposed_ver_index])
        i += 1
    return route


def create_starting_population(size):
    population = []
    for i in range(0, size):
        population.append(create_new_member())
    return population


def individual_fitness(route):
    score = 0
    for cur in range(1, len(route)):
        score += theMap[route[cur - 1]][route[cur]]
    score += theMap[0][route[-1]]
    return score


def population_fitness(population):
    fitness_list = []
    total_fitness = 0
    for individual in population:
        fitness = individual_fitness(individual)
        total_fitness += fitness
        fitness_list.append(fitness)
    return fitness_list, total_fitness


def find_topper(fitness_list, population):
    topper_index = fitness_list[0].index(min(fitness_list[0]))
    return population[topper_index], fitness_list[0][topper_index]


def roulette_wheel_selection(population):
    fitness_list, total_sum = population_fitness(population)
    random_int = random.randint(0, total_sum)
    partial_sum = 0
    for i in range(0, len(fitness_list)):
        partial_sum += fitness_list[i]
        if partial_sum >= random_int:
            parent_index = i
            break
    return population[parent_index]


def crossover_from_otherParent(offspring, otherParent, o, p, routeLength):
    if otherParent[p] not in offspring:
        offspring[o] = otherParent[p]
        o = (o + 1) % routeLength
        p = (p + 1) % routeLength
    else:
        p = (p + 1) % routeLength
    return o, p


def order_crossover(parent1, parent2):              # adding probability left
    routeLength = len(parent1)                                               # routeLength = gene length = no. of cities
    offspring1 = [-1]*routeLength
    offspring2 = [-1]*routeLength
    cut1 = random.randint(0, int(routeLength/2))    # int(routeLength/2)
    cut2 = random.randint(int(routeLength/2), routeLength-1)
    # loop to add crossover section elements
    for i in range(cut1, cut2+1):               # eg. |x x x|a b c|x x x|       Loop to get a,b,c for both offsprings
        offspring1[i] = parent1[i]
        offspring2[i] = parent2[i]
    # Counters:
    o1 = (cut2+1) % routeLength        # o1, o2 are offspring index counters
    o2 = (cut2+1) % routeLength
    p1 = (cut2+1) % routeLength         # p1, p2 are parent index counters
    p2 = (cut2+1) % routeLength
    while o1 != cut1 and o2 != cut1:
        if o1 != cut1:
            o1, p2 = crossover_from_otherParent(offspring1, parent2, o1, p2, routeLength)
        if o2 != cut1:
            o2, p1 = crossover_from_otherParent(offspring2, parent1, o2, p1, routeLength)
    return offspring1, offspring2


def mutation_on_population(population, prob_of_mutation):           # probability handled
    random_number = random.randint(0,1)
    for i in range(0, len(population)):
        if random_number < prob_of_mutation:
            individual = random.choice(population)
            individual = mutation_on_individual(individual)
            population[i] = individual
    return population


def mutation_on_individual(individual):
    pt1 = random.randint(1, int(len(individual)/2))
    pt2 = random.randint(pt1+1, len(individual)-1)
    while pt1 < pt2:
        individual[pt1], individual[pt2] = individual[pt2], individual[pt1]
        pt1 += 1
        pt2 -= 1
    return individual


def convergence_reached(fitness_list, threshold):
    population_std = statistics.pstdev(fitness_list)
    if population_std < threshold:
        return True                                   # convergence reached


if __name__ == '__main__':
    initialize()
    no_of_iterations = 9
    population_size = 6
    no_of_couples = 2
    mutationProbability = 0.05
    elitismNumber = 2
    convergenceThreshold = 0.3
    currentPopulation = create_starting_population(5)

    for iteration in range(0, no_of_iterations):                # or convergence
        fitnessList = population_fitness(currentPopulation)
        topper, score = find_topper(fitnessList, currentPopulation)
        print("The best route so far is: ", topper, "\t with distance: ", score)

        # convergence check
        if convergence_reached(fitnessList[0], convergenceThreshold):              # end if convergence reached
            break

        # create new population
        newPopulation = []
        # crossover
        for crossoverIteration in range(0, no_of_couples):
            parent01 = roulette_wheel_selection(currentPopulation)
            parent02 = roulette_wheel_selection(currentPopulation)

            child1, child2 = order_crossover(parent01, parent02)
            newPopulation.append(child1)
            newPopulation.append(child2)

            # Elitism: the parent are selected by Roulette wheel Selection approach, thus there is always strong possibility of selecting elites as parents
            newPopulation.append(parent01)
            newPopulation.append(parent02)

        # mutation
        mutation_on_population(newPopulation, mutationProbability)

        # add randomly in remaining places - if remained
        while len(newPopulation) < population_size:
            newPopulation.append(create_new_member())

        currentPopulation = newPopulation

    print("End")

